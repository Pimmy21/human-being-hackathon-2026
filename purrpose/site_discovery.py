"""Bounded live discovery on three named rescue websites; no arbitrary URL inputs."""
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
import re
import subprocess
import sys
import time
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, build_opener
from urllib.error import HTTPError
from urllib.robotparser import RobotFileParser
from uuid import uuid4
from .public_reader import NoRedirect, ReadFailure, AGENT
from .memory import MemoryUnavailable

SITES={
 'ottawa':{'name':'Ottawa Humane Society','origin':'https://www.ottawahumane.ca','entry':'https://www.ottawahumane.ca/news/blog/'},
 'toronto':{'name':'Toronto Cat Rescue','origin':'https://torontocatrescue.ca','entry':'https://torontocatrescue.ca/'},
 'ava':{'name':'AVA Cat Rescue','origin':'https://www.avacats.org','entry':'https://www.avacats.org/'}}
VOID={'meta','img','br','hr','input','link','source','wbr','embed','area','base','col','param','track'}
WORDS=re.compile(r'\b(cat|cats|kitten|kittens|medical|surgery|treatment|injur\w*|appeal|emergency|rescue|rescued|help|care)\b',re.I)
CLINICAL=re.compile(r'\b(surgery|medical|treatment|injur\w*|fracture|veterinar\w*|dental|hospital\w*)\b',re.I)
CAT=re.compile(r'\b(cat|cats|kitten|kittens)\b',re.I)

class Page(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.skip=0;self.parts=[];self.main=[];self.stack=[];self.links=[];self.anchor=None;self.title=[];self.in_title=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag not in VOID:self.stack.append(tag)
  if tag in ('script','style','noscript','svg'):self.skip+=1
  if tag=='title':self.in_title=True
  if tag=='a':self.anchor=[a.get('href',''),[]]
 def handle_endtag(self,tag):
  if tag=='a' and self.anchor:self.links.append((self.anchor[0],' '.join(self.anchor[1])));self.anchor=None
  if tag=='title':self.in_title=False
  if tag in ('script','style','noscript','svg'):self.skip=max(0,self.skip-1)
  if tag in self.stack:del self.stack[len(self.stack)-1-self.stack[::-1].index(tag):]
 def handle_data(self,data):
  if self.skip or not data.strip():return
  s=re.sub(r'\s+',' ',data).strip();self.parts.append(s)
  if 'main' in self.stack or 'article' in self.stack:self.main.append(s)
  if self.anchor:self.anchor[1].append(s)
  if self.in_title:self.title.append(s)
 def text(self):return ' '.join(self.main or self.parts)[:24000]

def canonical(href,base,origin):
 try:
  u=urlsplit(urljoin(base,href))
  if u.scheme!='https' or u.netloc!=urlsplit(origin).netloc or u.username or u.password or u.query:return None
  if re.search(r'\.(pdf|jpg|jpeg|png|zip|xml|mp4|svg)$',u.path,re.I):return None
  return urlunsplit((u.scheme,u.netloc,u.path or '/','',''))
 except ValueError:return None

def fetch(url,origin):
 u=urlsplit(url)
 if u.scheme!='https' or u.netloc!=urlsplit(origin).netloc or u.query or u.username or u.password:raise ReadFailure('url_not_permitted')
 try:
  with build_opener(NoRedirect).open(Request(url,headers={'User-Agent':AGENT,'Accept-Encoding':'identity'}),timeout=7) as r:
   if r.headers.get_content_type() not in ('text/html','text/plain'):raise ReadFailure('unsupported_content_type')
   raw=r.read(524289)
   if len(raw)>524288:raise ReadFailure('response_too_large')
   return raw.decode('utf-8',errors='replace')
 except HTTPError as e:
  if u.path=='/robots.txt' and e.code==404:return ''
  raise ReadFailure('http_'+str(e.code)) from None
 except (OSError,TimeoutError):raise ReadFailure('network_or_timeout') from None

def discover(site_id,reader=None):
 if site_id not in SITES:raise ValueError('Unknown site')
 return discover_pages(site_id,SITES[site_id],reader)

def parsed_candidate(url,label,raw,entry):
 p=Page();p.feed(raw);text=p.text()
 # Related-story cards are separate cases, not evidence for the requested article.
 boundary=re.search(r'\bRelated\s+(?:news|stories|posts|articles)\b',text,re.I)
 if boundary:text=text[:boundary.start()].rstrip()
 if re.search(r'\b(just a moment|access denied|verify (?:that )?you are human|sign in|log in|captcha)\b',' '.join(p.title),re.I):
  raise ReadFailure('login_or_challenge_page_not_supported')
 if len(text)<100:raise ReadFailure('insufficient_readable_text')
 matches=list(CLINICAL.finditer(text));snippets=[]
 for m in matches[:3]:
  start=max(0,m.start()-100);end=min(len(text),m.end()+180)
  snippets.append({'start':start,'end':end,'quote':text[start:end]})
 return {'url':url,'discovered_from':entry,'link_text':label,'status':'read',
   'title':' '.join(p.title)[:300],'content_sha256':hashlib.sha256(raw.encode()).hexdigest(),
   'text':text,'excerpts':snippets or [{'start':0,'end':min(350,len(text)),'quote':text[:350]}],
   'relevance':'cat_and_medical_terms_present' if CAT.search(text) and matches else 'context_only_not_a_confirmed_cat_medical_appeal',
   'verification':'unverified_publisher_account','remaining_minor':None,'qualified':False}

def discover_pages(site_id,site,reader=None,include_entry=False):
 origin=site['origin'];reader=reader or (lambda url:fetch(url,origin))
 result={'site_id':site_id,'organization':site['name'],'entry_url':site['entry'],'observed_at':datetime.now(timezone.utc).isoformat(),
   'mode':'live_site_discovery','status':'incomplete','requests':[],'candidates':[],'qualified':False,'remaining_minor':None,
   'limits':['One approved website, one entry page, up to three discovered pages. No full-site coverage.',
   'Page excerpts are organization claims, not independently verified evidence. Entry-page navigation may be included.',
   'No model, media, login, external donation form, arbitrary URL, or automatic retry. Amount remains unknown.',
   'Matching words establish relevance only, never clinical authenticity, current need or donation qualification.']}
 def read(url,stage):
  began=time.monotonic()
  try:
   data=reader(url);result['requests'].append({'url':url,'stage':stage,'status':'read','duration_ms':int((time.monotonic()-began)*1000)});return data
  except Exception as exc:
   category=str(exc) if isinstance(exc,ReadFailure) else 'reader_failed'
   result['requests'].append({'url':url,'stage':stage,'status':'failed','error':category,'duration_ms':int((time.monotonic()-began)*1000)});raise ReadFailure(category) from None
 try:
  robots=read(origin+'/robots.txt','robots')
  if '<html' in robots.lower():raise ReadFailure('robots_unreadable')
  policy=RobotFileParser();policy.parse(robots.splitlines())
  prefix=re.split(r'(?im)^\s*user-agent\s*:',robots,maxsplit=1)[0]
  # Explicit single-page reads can honor a short delay within the 45s worker budget.
  # Request-rate directives and longer/ambiguous delays remain unsupported.
  paced=False
  prefix_delays=re.findall(r'(?im)^\s*crawl-delay\s*:\s*([^#\r\n]+)',prefix)
  scoped_delay=policy.crawl_delay(AGENT)
  has_delay=bool(scoped_delay or prefix_delays)
  if policy.request_rate(AGENT) or re.search(r'(?im)^\s*request-rate\s*:',prefix):raise ReadFailure('robots_scheduler_required')
  if has_delay:
   try:
    delay=max([float(v.strip()) for v in prefix_delays]+[float(scoped_delay or 0)])
   except ValueError:raise ReadFailure('robots_scheduler_required')
   if not include_entry or not 0<delay<=10:raise ReadFailure('robots_scheduler_required')
   paced=True
  if not policy.can_fetch(AGENT,site['entry']):raise ReadFailure('robots_disallowed_entry')
  if paced:
   time.sleep(delay)
   result['access_schedule']={'delay_seconds':delay,'entry_only':True,'automatic_retry':False}
   result['limits'][0]='One explicitly requested page only; robots delay honored. No linked-page investigation.'
  entry_raw=read(site['entry'],'discovery_entry');entry=Page();entry.feed(entry_raw)
  if include_entry:
   result['candidates'].append(parsed_candidate(site['entry'],'User-supplied page; identity not authenticated',entry_raw,site['entry']))
  candidates={}
  for href,label in entry.links:
   url=canonical(href,site['entry'],origin)
   if not url or url in (site['entry'],origin+'/') or not policy.can_fetch(AGENT,url):continue
   if site_id=='ottawa' and not urlsplit(url).path.startswith('/news/posts/'):continue
   score=len(WORDS.findall(label)) + 2*bool(CLINICAL.search(label))
   if score:candidates[url]=max(candidates.get(url,(0,'')),(score,label))
  selected=[] if paced else sorted(candidates.items(),key=lambda x:(-x[1][0],x[0]))[:3]
  result['discovered_relevant_links']=len(candidates)
  for url,(_,label) in selected:
   row={'url':url,'discovered_from':site['entry'],'link_text':label[:300]}
   try:
    row.update(parsed_candidate(url,label,read(url,'candidate_page'),site['entry']))
   except ReadFailure as exc:row.update(status='read_failed',error=str(exc))
   result['candidates'].append(row)
  result['status']='read_complete' if all(c['status']=='read' for c in result['candidates']) else 'partial_read'
  if not selected and not include_entry:result['status']='no_relevant_links_found_in_entry'
 except ReadFailure as exc:result['error']=str(exc)
 return result

def bounded_discover(site_id):
 if site_id not in SITES:raise ValueError('Unknown site')
 try:
  proc=subprocess.run([sys.executable,'-m','purrpose.site_discovery',site_id],capture_output=True,timeout=45,check=True)
  return json.loads(proc.stdout)
 except (subprocess.SubprocessError,ValueError):return {'status':'incomplete','site_id':site_id,'error':'worker_deadline_or_failure','qualified':False,'remaining_minor':None,'candidates':[]}

def remember_discovery(result,memory):
 result['memory']={'status':'not_configured'}
 if memory and result.get('requests'):
  case='SITE-'+result['site_id'].upper()
  try:
   payload={k:v for k,v in result.items() if k!='memory'}
   saved=memory.call('save',case,{'schema_version':1,'case_id':case,'run_id':str(uuid4()),'scenario_type':'real_public_observations',
     'organization':result['organization'],'case_name':'Bounded public site discovery','source_refs':[r['url'] for r in result['requests']],
     'review_summary':{'qualified':False,'disposition':'pending_evidence'},'discovery':payload})
   result['memory']={'status':'saved','memory_id':saved['memory_id']}
  except (MemoryUnavailable,KeyError):result['memory']={'status':'save_failed'}
 return result

if __name__=='__main__':
 print(json.dumps(discover(sys.argv[1]),ensure_ascii=True))
