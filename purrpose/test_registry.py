from unittest import TestCase
from .registry import Registry, SQL, BN
class RegistryTests(TestCase):
 def configured(self,transport):
  return Registry({'ZETARIS_MODE':'local_rest','ZETARIS_REST_URL':'http://127.0.0.1:18888','ZETARIS_API_KEY':'test-only'},transport)
 def test_no_config_no_call(self):
  r=Registry(transport=lambda:self.fail('no call')).check()
  self.assertEqual(r['status'],'unavailable');self.assertFalse(r['qualified'])
 def test_reject_remote_or_credential_urls(self):
  for url in ['http://remote:18888','http://user:pass@localhost:18888','http://localhost:18888/?key=x']:
   r=Registry({'ZETARIS_MODE':'local_rest','ZETARIS_REST_URL':url,'ZETARIS_API_KEY':'x'})
   self.assertEqual(r.readiness(),'invalid_loopback_endpoint')
 def test_historical_only(self):
  r=self.configured(lambda:{'data':[[BN,'THE GUELPH HUMANE SOCIETY INCORPORATED','Guelph','ON']]}).check()
  self.assertEqual(r['status'],'historical_identity_matched');self.assertFalse(r['qualified']);self.assertFalse(r['current_registration_verified']);self.assertEqual(r['comparison'],'matches_saved_identity')
 def test_unusable_rows_do_not_pass(self):
  for rows in [[],[['wrong','A','Guelph','ON']],[[BN,'A','Guelph','ON']]*2]:
   r=self.configured(lambda:{'data':rows}).check();self.assertEqual(r['status'],'unavailable')
 def test_conflict_is_visible(self):
  r=self.configured(lambda:{'data':[[BN,'Different organization','Toronto','ON']]}).check()
  self.assertEqual(r['comparison'],'identity_conflict_needs_review');self.assertFalse(r['qualified'])
 def test_errors_sanitized_no_retry(self):
  calls=[]
  def fail(): calls.append(1);raise RuntimeError('SECRET TEST VALUE')
  r=self.configured(fail).check();self.assertNotIn('SECRET',str(r));self.assertEqual(len(calls),1)
 def test_fixed_sql_not_user_input(self):
  self.assertTrue(SQL.startswith('SELECT '));self.assertNotIn(';',SQL);self.assertIn(BN,SQL)

class RemoteRegistryTests(TestCase):
 def test_success_uses_tcr_scope_not_lucy(self):
  import json
  from types import SimpleNamespace
  from .registry import RemoteRegistry
  calls=[]
  def run(command,**kwargs):
   calls.append((command,kwargs))
   return SimpleNamespace(stdout='PURRPOSE_RESULT:'+json.dumps({'status':'completed','source_rows':[['720884691RR0001','TORONTO CAT RESCUE','ETOBICOKE','ON']],'steps':[]}))
  r=RemoteRegistry('env','python','jvm',runner=run).check()
  self.assertEqual(r['case_id'],'REAL-TCR-REGISTRY');self.assertEqual(r['status'],'historical_identity_matched');self.assertFalse(r['qualified']);self.assertEqual(len(calls),1);self.assertEqual(calls[0][1]['timeout'],45)
 def test_failure_is_sanitized_and_not_retried(self):
  from .registry import RemoteRegistry
  calls=[]
  def run(*a,**k): calls.append(1);raise RuntimeError('PRIVATE')
  r=RemoteRegistry('env','python','jvm',runner=run).check()
  self.assertEqual(r['status'],'unavailable');self.assertNotIn('PRIVATE',str(r));self.assertEqual(len(calls),1)
