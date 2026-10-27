from unittest import TestCase
from .organization_live import organization_gaps
class OrganizationLiveTests(TestCase):
 def test_no_pages_is_unable_not_missing(self):
  r=organization_gaps({'candidates':[]})
  self.assertTrue(all(f['status']=='unable_to_assess' for f in r['fields']));self.assertFalse(r['qualified'])
 def test_mentions_are_not_verified_evidence(self):
  text='Cat surgery in October 22, 2026; $100 suggested donation.'
  r=organization_gaps({'candidates':[{'status':'read','text':text,'url':'https://example.org/a'}]})
  for f in r['fields']:
   self.assertFalse(f['verified'])
   for o in f['observations']:self.assertEqual(text[o['start']:o['end']],o['quote'])
  self.assertEqual(r['fields'][1]['status'],'related_wording_found_needs_case_check')
 def test_unread_text_not_assessed(self):
  r=organization_gaps({'candidates':[{'status':'read_failed','text':'surgery $100','url':'https://example.org'}]})
  self.assertEqual(r['pages_read'],0)
 def test_missing_is_scoped_and_not_fraud(self):
  r=organization_gaps({'candidates':[{'status':'read','text':'A rescue story','url':'https://example.org'}]})
  self.assertTrue(all(f['status']=='not_found_in_read_pages' for f in r['fields']));self.assertFalse(r['website_fully_reviewed']);self.assertFalse(r['representation_authority_verified'])
