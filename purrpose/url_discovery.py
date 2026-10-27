"""User-supplied public page onboarding. Validation is part of the workflow."""
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
from urllib.parse import urlsplit
from .safe_web import PublicReader, normalize_url
from .public_reader import ReadFailure
from .site_discovery import discover_pages


def inspect_url(value,reader_factory=PublicReader):
    checks=[]
    try:
        url=normalize_url(value)
        checks.append({'stage':'url_policy','status':'passed','meaning':'HTTPS public-domain candidate only; not organization verification'})
        reader=reader_factory(url)
        scope='custom-'+hashlib.sha256(url.encode()).hexdigest()[:20]
        site={'origin':reader.origin,'entry':url,'name':'User-supplied website: '+urlsplit(url).hostname}
        result=discover_pages(scope,site,reader,include_entry=True)
        checks.extend({'stage':r['stage'],'status':r['status'],'url':r['url'],**({'error':r['error']} if r.get('error') else {})} for r in result.get('requests',[]))
        for page in result.get('candidates',[]):
            checks.append({'stage':'page_structure','status':'readable' if page['status']=='read' else 'not_assessed',
                           'url':page['url'],'meaning':'Readable text only, not evidence authenticity'})
        if result.get('error'):
            checks.append({'stage':'access_or_structure','status':'incomplete','error':result['error']})
        result.update(mode='live_user_url_discovery',admission={'checks':checks,
            'network_checks':reader.network_checks,'organization_identity_verified':False,
            'ontario_location_verified':False,'website_ownership_verified':False,
            'site_terms_permission_assessed':False,
            'meaning':'Technical access checks only. User supplied an unverified website; public access is not credibility.'})
        if not result.get('access_schedule'):
            result['limits'][0]='User-supplied entry page plus up to three dynamically discovered same-host HTML pages. No full-site coverage.'
        result['limits'][2]='No model, media, login, external forms, cross-host links or automatic retry. Amount unknown.'
        return result
    except ReadFailure as exc:
        return {'mode':'live_user_url_discovery','status':'blocked','error':str(exc),
            'observed_at':datetime.now(timezone.utc).isoformat(),'requests':[],'candidates':[],
            'qualified':False,'remaining_minor':None,'admission':{'checks':checks+[{'stage':'url_policy','status':'blocked','error':str(exc)}],
            'organization_identity_verified':False,'ontario_location_verified':False,'website_ownership_verified':False}}


def bounded_inspect(value):
    # Structural failures are rejected before worker launch or DNS/network access.
    try:
        url=normalize_url(value)
    except ReadFailure:
        return inspect_url(value)
    try:
        proc=subprocess.run([sys.executable,'-m','purrpose.url_discovery'],input=json.dumps({'url':url}).encode(),
                            capture_output=True,timeout=45,check=True)
        return json.loads(proc.stdout)
    except (subprocess.SubprocessError,ValueError):
        return {'mode':'live_user_url_discovery','status':'incomplete','error':'worker_deadline_or_failure',
            'requests':[],'candidates':[],'qualified':False,'remaining_minor':None,
            'admission':{'organization_identity_verified':False,'ontario_location_verified':False,
                         'checks':[{'stage':'worker','status':'incomplete','error':'45_second_deadline_or_worker_failure'}]}}


if __name__=='__main__':
    try:
        request=json.loads(sys.stdin.buffer.read(8192))
        result=inspect_url(request.get('url'))
    except Exception:
        result={'status':'incomplete','error':'reader_failure','requests':[],'candidates':[],
                'qualified':False,'remaining_minor':None}
    print(json.dumps(result,ensure_ascii=True))
