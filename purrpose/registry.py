"""Explicit local-only, read-only historical registry lookup. Never qualifies a case."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
from urllib.parse import urlsplit
from urllib.request import Request, build_opener
from urllib.error import HTTPError
from uuid import uuid4
from .provider import NoRedirect
from .memory import MemoryUnavailable

SOURCE='https://open.canada.ca/data/en/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8'
BN='119236305RR0001'
SQL=('SELECT fact.BN, fact.`Legal Name`, fact.City, fact.Province '
     'FROM CRA_CHARITIES_2024.ontario_animal_identity '
     "LATERAL VIEW explode(result.records) AS fact WHERE fact.BN = '"+BN+"'")
NAMES=('ZETARIS_MODE','ZETARIS_REST_URL','ZETARIS_API_KEY','ZETARIS_ORG_ID')

def settings(path=None):
    result={}
    if path and Path(path).is_file():
        for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
            if '=' in line and not line.strip().startswith('#'):
                key,value=line.split('=',1)
                if key.strip() in NAMES: result[key.strip()]=value.strip().strip('\"\'')
    result.update({k:os.environ[k] for k in NAMES if os.environ.get(k)})
    return result

class Registry:
    case_id='REAL-LUCY-REGISTRY'
    def __init__(self, config=None, transport=None):
        self.config=dict(config or {})
        self.transport=transport or self.request
        self.trace=[]
    def readiness(self):
        c=self.config
        if c.get('ZETARIS_MODE')!='local_rest': return 'local_rest_not_selected'
        try:
            u=urlsplit(c.get('ZETARIS_REST_URL',''))
            if u.scheme!='http' or u.hostname not in ('127.0.0.1','localhost','::1') or not u.port or u.username or u.password or u.path not in ('','/') or u.query or u.fragment:
                return 'invalid_loopback_endpoint'
        except ValueError: return 'invalid_loopback_endpoint'
        if not c.get('ZETARIS_API_KEY'): return 'missing_api_key'
        if not c.get('ZETARIS_ORG_ID','1').isdigit(): return 'invalid_org_id'
        return 'configured_not_live_verified'
    def request(self):
        c=self.config
        req=Request(c['ZETARIS_REST_URL'].rstrip('/')+'/sql-editor/sqls/run',
            data=json.dumps({'queryId':str(uuid4()),'sql':SQL,'source':'SqlEditor','limit':3}).encode(),
            headers={'Authorization':'Bearer '+c['ZETARIS_API_KEY'],'X-Org-ID':c.get('ZETARIS_ORG_ID','1'),
                     'X-Request-ID':str(uuid4()),'Content-Type':'application/json'},method='POST')
        with build_opener(NoRedirect).open(req,timeout=30) as response:
            raw=response.read(65537)
            if len(raw)>65536: raise ValueError('oversize')
            return json.loads(raw)
    def check(self, memory=None):
        started=time.monotonic()
        result={'status':'unavailable','case_id':'REAL-LUCY-GHS','query_name':'lucy_historical_identity',
                'observed_at':datetime.now(timezone.utc).isoformat(),'reporting_year':2024,'source':SOURCE,
                'current_registration_verified':False,'qualified':False,'remaining_minor':None,
                'source_failure_is_fraud':False,'memory':{'status':'not_configured'},
                'note':'2024 annual-return identity only; does not establish current registration, medical need, case funding or safety.'}
        category=self.readiness()
        if category=='configured_not_live_verified':
            try:
                out=self.transport()
                if not isinstance(out,dict) or not isinstance(out.get('data'),list): raise ValueError('shape')
                rows=out['data']
                if len(rows)>3: raise ValueError('rows')
                valid=[r for r in rows if isinstance(r,list) and len(r)==4 and r[0]==BN and all(isinstance(v,str) and 0<len(v.strip())<=500 for v in r)]
                if len(valid)!=1 or len(rows)!=1: raise ValueError('ambiguous')
                row=valid[0]
                result.update(status='historical_identity_matched',organization_number=row[0],organization_full_name=row[1],reported_city=row[2],reported_province=row[3],row_count=1)
                result['comparison']='matches_saved_identity' if row[1].upper()=='THE GUELPH HUMANE SOCIETY INCORPORATED' and row[2].upper()=='GUELPH' and row[3].upper()=='ON' else 'identity_conflict_needs_review'
                category=None
            except HTTPError as exc:
                category={401:'unauthorized',403:'forbidden',429:'rate_limited'}.get(exc.code,'upstream_http_error')
            except (ValueError,TypeError): category='unusable_response_or_no_unique_match'
            except Exception: category='connection_query_or_source_failed'
        result['error_category']=category
        event={'tool':'zetaris','operation':'historical_identity','status':'completed' if result['status']=='historical_identity_matched' else 'failed',
               'duration_ms':int((time.monotonic()-started)*1000),'error_category':category,'row_count':result.get('row_count',0)}
        self.trace=(self.trace+[event])[-50:]
        result['tools']=[event]
        memory_began=time.monotonic()
        if memory:
            try:
                saved=memory.call('save','REAL-LUCY-REGISTRY',{'schema_version':1,'case_id':'REAL-LUCY-REGISTRY',
                    'run_id':str(uuid4()),'scenario_type':'real_public_observations','source_refs':[SOURCE],
                    'organization':'Guelph Humane Society','case_name':'Lucy registry observation',
                    'review_summary':{'qualified':False,'disposition':'pending_evidence'},'registry_observation':dict(result)})
                result['memory']={'status':'saved','memory_id':saved['memory_id']}
            except (MemoryUnavailable,KeyError): result['memory']={'status':'save_failed'}
        result['tools'].append({'tool':'hmem','operation':'save','status':'ok' if result['memory']['status']=='saved' else 'not_configured' if result['memory']['status']=='not_configured' else 'failed','duration_ms':round((time.monotonic()-memory_began)*1000),'memory_id':result['memory'].get('memory_id')})
        return result

class RemoteRegistry:
    """Existing approved AWS JDBC probe in a bounded subprocess; no local fallback."""
    case_id='REAL-TCR-REGISTRY'
    def __init__(self,env_file,python,jvm,runner=None):
        self.env_file,self.python,self.jvm=str(env_file),str(python),str(jvm)
        self.trace=[]
        self.runner=runner
    def readiness(self):
        return 'remote_jdbc_selected_not_live_verified_in_this_server'
    def check(self,memory=None):
        import subprocess
        from .zetaris import normalize_identity, supporter_identity_view
        began=time.monotonic()
        command=[self.python,'-m','purrpose.zetaris','--worker','--env-file',str(Path(self.env_file).resolve()),'--jvm',str(Path(self.jvm).resolve())]
        try:
            completed=(self.runner or subprocess.run)(command,cwd=str(Path(__file__).resolve().parents[1]),text=True,encoding='utf-8',capture_output=True,timeout=45)
            lines=[s for s in completed.stdout.splitlines() if s.startswith('PURRPOSE_RESULT:')]
            raw=json.loads(lines[-1].split(':',1)[1]) if lines else {}
            identity=normalize_identity(raw.get('source_rows',[]))
            result={'status':identity['status'],'identity':identity,'steps':raw.get('steps',[]),
                    'error_category':raw.get('error_category') if raw.get('status')!='completed' else None,
                    'failed_stage':raw.get('failed_stage'),'view':supporter_identity_view({'identity':identity,**{k:raw[k] for k in ('error_category','failed_stage') if k in raw}})}
            if raw.get('status')!='completed': result['status']='unavailable'
        except subprocess.TimeoutExpired:
            result={'status':'unavailable','failed_stage':'jdbc_worker','error_category':'worker_deadline_45_seconds'}
        except Exception:
            result={'status':'unavailable','failed_stage':'jdbc_worker','error_category':'worker_or_config_failed'}
        result.update(case_id=self.case_id,observed_at=datetime.now(timezone.utc).isoformat(),
                      source=SOURCE,reporting_year=2024,qualified=False,current_registration_verified=False,
                      source_failure_is_fraud=False,memory={'status':'not_configured'},
                      note='Separate Toronto Cat Rescue historical identity lookup; not Lucy evidence, current registration or case need.')
        event={'tool':'zetaris','operation':'aws_tcr_historical_identity','status':'completed' if result['status']=='historical_identity_matched' else 'failed',
               'duration_ms':int((time.monotonic()-began)*1000),'error_category':result.get('error_category')}
        result['tools']=[event];self.trace=(self.trace+[event])[-50:]
        memory_began=time.monotonic()
        if memory:
            try:
                saved=memory.call('save',self.case_id,{'schema_version':1,'case_id':self.case_id,'run_id':str(uuid4()),
                    'scenario_type':'real_public_observations','source_refs':[SOURCE],
                    'organization':'TORONTO CAT RESCUE','case_name':'Historical organization identity',
                    'review_summary':{'qualified':False,'disposition':'pending_evidence'},'registry_observation':dict(result)})
                result['memory']={'status':'saved','memory_id':saved['memory_id']}
            except (MemoryUnavailable,KeyError): result['memory']={'status':'save_failed'}
        result['tools'].append({'tool':'hmem','operation':'save','status':'ok' if result['memory']['status']=='saved' else 'not_configured' if result['memory']['status']=='not_configured' else 'failed','duration_ms':round((time.monotonic()-memory_began)*1000),'memory_id':result['memory'].get('memory_id')})
        return result
