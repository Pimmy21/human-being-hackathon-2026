from unittest import TestCase
from unittest.mock import patch
from .organization_research import organization_research, LINKS
from .server import LocalApp


class OrganizationResearchTests(TestCase):
    def test_real_public_link_returns_actionable_gaps_without_network(self):
        app=LocalApp()
        with patch('purrpose.server.bounded_read',side_effect=AssertionError('No fetching')):
            result=app.dispatch('/api/organization',{'public_links':[sorted(LINKS)[0]]})
        self.assertEqual(result['mode'],'real_public_research')
        self.assertFalse(result['qualified'])
        self.assertFalse(result['materials_fetched'])
        self.assertFalse(result['representation_authority_verified'])
        self.assertIsNone(app.latest_run)
        for gap in result['gap_checklist']:
            self.assertTrue(gap['what_to_add'])
            self.assertTrue(gap['where_to_obtain_or_publish'])
            self.assertIn(gap['responsible_party'],('system','organization'))

    def test_existing_allocation_not_called_absent(self):
        result=organization_research(list(LINKS))
        allocation=next(g for g in result['gap_checklist'] if g['field']=='allocation')
        self.assertIn('already says',allocation['why'])
        self.assertIn('not an allegation',next(g for g in result['gap_checklist'] if g['field']=='risk_coverage')['why'])

    def test_unknown_mixed_and_private_urls_not_fetched(self):
        app=LocalApp()
        for links in ([sorted(LINKS)[0],'http://localhost/private'],['https://unknown.example/']):
            result=app.dispatch('/api/organization',{'public_links':links})
            self.assertEqual(result['status'],'unsupported_links')
            self.assertFalse(result['materials_fetched'])

    def test_chat_real_organization_checklist(self):
        result=LocalApp().dispatch('/api/chat',{'session_id':'one','message':'Lucy organization checklist'})
        self.assertIn('organization_review',result)
        self.assertEqual(result['new_cloud_calls'],0)

    def test_invalid_input_rejected(self):
        for links in ([],None,['https://unknown.example/']):
            with self.assertRaises(ValueError):
                organization_research(links)
