from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch
import socket
import ssl
from .safe_web import normalize_url, public_addresses, PublicReader, PinnedHTTPSConnection
from .public_reader import ReadFailure
from .url_discovery import inspect_url, bounded_inspect


def dns(*addresses):
 return [(socket.AF_INET,socket.SOCK_STREAM,6,'',(a,443)) for a in addresses]

class Response:
 status=200
 headers={'Content-Type':'text/html'}
 body=b'<html><main>A public cat surgery story. Enough readable public content to assess as context, not proof of an actual current funding need.</main></html>'
 def getheader(self,name,default=None):return self.headers.get(name,default)
 def read(self,n):return self.body[:n]

class Connection:
 def __init__(self,response=None):self.response=response or Response();self.requests=[];self.closed=False
 def request(self,*a,**k):self.requests.append((a,k))
 def getresponse(self):return self.response
 def close(self):self.closed=True

class SafeWebTests(TestCase):
 def test_url_rejections_before_dns(self):
  bad=['http://rescue.org/','https://localhost/','https://127.0.0.1/','https://[::1]/','https://169.254.169.254/latest/',
    'https://user:pass@rescue.org/','https://rescue.org:8443/','https://rescue.org/?token=private','https://rescue.org/#secret',
    'file:///private','https://rescue.org/\\a','https://rescue.org/\n','https://0177.0.0.1/',
    'https://2130706433/','https://a.local/','https://a.internal/','https://rescue.org./','https://rescue.org/%0d%0aHost:x']
  for url in bad:
   with self.subTest(url=url),self.assertRaises(ReadFailure):normalize_url(url)
 def test_url_normalization(self):
  self.assertEqual(normalize_url('https://Rescue.ORG:443/cat/'),'https://rescue.org/cat/')
  self.assertEqual(normalize_url('https://rescue.org/'),'https://rescue.org/')
 def test_private_and_mixed_dns_all_rejected(self):
  for address in ['127.0.0.1','10.0.0.1','192.168.1.5','169.254.169.254','0.0.0.0','224.0.0.1','::1','fc00::1','fe80::1','::ffff:8.8.8.8','192.0.2.1','2002:a00:1::1','2001:0000:4136:e378:8000:63bf:3fff:fdd2']:
   with self.subTest(ip=address),self.assertRaises(ReadFailure):public_addresses('rescue.org',lambda *a,**k:dns('8.8.8.8',address))
 def test_dns_errors_and_empty_rejected(self):
  with self.assertRaises(ReadFailure):public_addresses('rescue.org',lambda *a,**k:[])
  def fail(*a,**k):raise socket.gaierror()
  with self.assertRaises(ReadFailure):public_addresses('rescue.org',fail)
 def test_socket_target_is_checked_ip_and_host_is_hostname(self):
  conn=Connection();constructed=[]
  def factory(host,ip,timeout):constructed.append((host,ip,timeout));return conn
  reader=PublicReader('https://rescue.org/cat/',lambda *a,**k:dns('8.8.8.8'),factory)
  self.assertIn('surgery',reader(reader.entry));self.assertEqual(constructed,[('rescue.org','8.8.8.8',7)])
  self.assertEqual(conn.requests[0][1]['headers']['Host'],'rescue.org');self.assertTrue(conn.closed)
 def test_rebinding_is_checked_before_each_connection(self):
  responses=iter([dns('8.8.8.8'),dns('127.0.0.1')]);connections=[]
  def factory(*a):connections.append(a);return Connection()
  reader=PublicReader('https://rescue.org/',lambda *a,**k:next(responses),factory)
  reader(reader.entry)
  with self.assertRaises(ReadFailure):reader(reader.entry)
  self.assertEqual(len(connections),1)
 def test_redirect_never_followed(self):
  response=Response();response.status=302;response.headers={'Location':'http://127.0.0.1/private'}
  conn=Connection(response);reader=PublicReader('https://rescue.org/',lambda *a,**k:dns('8.8.8.8'),lambda *a:conn)
  with self.assertRaisesRegex(ReadFailure,'redirect_not_followed'):reader(reader.entry)
  self.assertEqual(len(conn.requests),1)
 def test_foreign_host_rejected_before_dns(self):
  reader=PublicReader('https://rescue.org/',lambda *a,**k:self.fail('no DNS'))
  with self.assertRaises(ReadFailure):reader('https://other.org/')
 def test_response_limits(self):
  for headers,body in [({'Content-Type':'application/pdf'},b'pdf'),({'Content-Type':'text/html','Content-Encoding':'gzip'},b'compressed'),
    ({'Content-Type':'text/html','Content-Length':'999999'},b'x'),({'Content-Type':'text/html'},b'x'*524289)]:
   response=Response();response.headers=headers;response.body=body;conn=Connection(response)
   reader=PublicReader('https://rescue.org/',lambda *a,**k:dns('8.8.8.8'),lambda *a:conn)
   with self.assertRaises(ReadFailure):reader(reader.entry)
   self.assertTrue(conn.closed)
 def test_tls_errors_never_bypassed(self):
  conn=Connection()
  def fail(*a,**k):raise ssl.SSLCertVerificationError('certificate problem')
  conn.request=fail
  reader=PublicReader('https://rescue.org/',lambda *a,**k:dns('8.8.8.8'),lambda *a:conn)
  with self.assertRaisesRegex(ReadFailure,'tls_verification_failed'):reader(reader.entry)
 def test_connection_tls_defaults(self):
  conn=PinnedHTTPSConnection('rescue.org','8.8.8.8')
  self.assertTrue(conn._context.check_hostname);self.assertEqual(conn._context.verify_mode,ssl.CERT_REQUIRED)
 def test_actual_connect_pins_and_preserves_sni(self):
  raw=SimpleNamespace(close=lambda:None);wrapped=object()
  conn=PinnedHTTPSConnection('rescue.org','8.8.8.8');context=SimpleNamespace(wrap_socket=lambda sock,server_hostname:wrapped if sock is raw and server_hostname=='rescue.org' else None);conn._context=context
  with patch('purrpose.safe_web.socket.create_connection',return_value=raw) as connect:
   conn.connect();connect.assert_called_once_with(('8.8.8.8',443),7)
  self.assertIs(conn.sock,wrapped)

class URLDiscoveryTests(TestCase):
 def factory(self,url):
  class Reader:
   origin='https://rescue.org';network_checks=[]
   def __call__(self,target):
    if target.endswith('/robots.txt'):return 'User-agent: *\nDisallow:\n'
    return '<html><title>New kitten appeal</title><main>'+('Our kitten needs surgery, with an estimate to be published. '*5)+'<a href="/case-two/">Cat medical update</a><a href="https://private.local/">cat surgery</a></main></html>'
  return Reader()
 def test_new_url_entry_itself_and_discovered_page_assessed(self):
  r=inspect_url('https://rescue.org/new-case/',self.factory)
  self.assertEqual(r['status'],'read_complete');self.assertEqual(len(r['candidates']),2)
  self.assertEqual(r['candidates'][0]['url'],'https://rescue.org/new-case/')
  self.assertFalse(r['admission']['organization_identity_verified']);self.assertFalse(r['admission']['ontario_location_verified']);self.assertFalse(r['qualified'])
 def test_invalid_url_no_reader_called(self):
  r=inspect_url('http://localhost/',lambda url:self.fail('not called'))
  self.assertEqual(r['status'],'blocked');self.assertEqual(r['requests'],[])
 def test_bad_page_reports_structure_failure(self):
  reader=self.factory('')
  reader.__class__.__call__=lambda self,url:'User-agent: *\nDisallow:\n' if url.endswith('/robots.txt') else '<html>short</html>'
  r=inspect_url('https://rescue.org/',lambda url:reader)
  self.assertEqual(r['error'],'insufficient_readable_text');self.assertEqual(r['candidates'],[])
 def test_robots_denial_never_reads_page(self):
  reader=self.factory('');calls=[]
  def read(self,url):calls.append(url);return 'User-agent: *\nDisallow: /'
  reader.__class__.__call__=read
  r=inspect_url('https://rescue.org/',lambda url:reader)
  self.assertEqual(r['error'],'robots_disallowed_entry');self.assertEqual(len(calls),1)
 def test_challenge_is_not_an_assessment(self):
  reader=self.factory('')
  reader.__class__.__call__=lambda self,url:'User-agent: *\nDisallow:\n' if url.endswith('/robots.txt') else '<html><title>Just a moment</title><main>'+('please wait '*30)+'</main></html>'
  r=inspect_url('https://rescue.org/',lambda url:reader)
  self.assertEqual(r['error'],'login_or_challenge_page_not_supported')
 def test_wall_deadline(self):
  import subprocess
  with patch('purrpose.url_discovery.subprocess.run',side_effect=subprocess.TimeoutExpired('x',45)) as run:
   r=bounded_inspect('https://rescue.org/');self.assertEqual(r['status'],'incomplete');self.assertEqual(run.call_args.kwargs['timeout'],45)
 def test_url_is_stdin_not_command_line(self):
  import json
  with patch('purrpose.url_discovery.subprocess.run',return_value=SimpleNamespace(stdout=b'{"status":"test"}')) as run:
   bounded_inspect('https://rescue.org/cat/')
   self.assertNotIn('https://rescue.org/cat/',str(run.call_args.args));self.assertEqual(json.loads(run.call_args.kwargs['input'])['url'],'https://rescue.org/cat/')

class UserURLServerTests(TestCase):
 def setUp(self):
  from .server import LocalApp
  self.app=LocalApp()
 def test_private_url_is_blocked_without_read_or_fake_review(self):
  r=self.app.dispatch('/api/discover-url',{'url':'https://127.0.0.1/private'})
  self.assertEqual(r['status'],'blocked');self.assertEqual(r['requests'],[])
  self.assertTrue(all(f['status']=='unable_to_assess' for f in r['organization_review']['fields']))
 def test_url_must_be_only_input(self):
  with self.assertRaises(ValueError):self.app.dispatch('/api/discover-url',{'url':'https://rescue.org/','sql':'SELECT 1'})
  for value in [None,[],123,'x'*2049]:
   with self.assertRaises(ValueError):self.app.dispatch('/api/discover-url',{'url':value})
 def test_current_read_drives_organization_guidance(self):
  sample={'site_id':'custom-test','organization':'Unverified website','requests':[],
          'candidates':[{'status':'read','url':'https://rescue.org/case','text':'A newly found kitten needs surgery.'}],
          'status':'read_complete','qualified':False}
  with patch('purrpose.server.bounded_inspect',return_value=sample):
   r=self.app.dispatch('/api/discover-url',{'url':'https://rescue.org/case'})
  self.assertEqual(r['organization_review']['pages_read'],1)
  self.assertEqual(r['organization_review']['fields'][0]['status'],'related_wording_found_needs_case_check')
  self.assertEqual(r['memory']['status'],'not_configured')

class ConservativeRobotsTests(TestCase):
 def test_unscoped_delay_requires_scheduler(self):
  from .site_discovery import discover
  calls=[]
  def reader(url):calls.append(url);return 'Crawl-delay: 10\nUser-agent: *\nDisallow:\n'
  r=discover('ottawa',reader)
  self.assertEqual(r['error'],'robots_scheduler_required');self.assertEqual(len(calls),1)
