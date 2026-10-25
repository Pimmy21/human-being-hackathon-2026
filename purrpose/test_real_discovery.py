from unittest import TestCase
from .server import LocalApp


class RealDiscoveryTests(TestCase):
    def test_real_without_case_name_is_pending(self):
        app=LocalApp()
        result=app.dispatch('/api/supporter',{'collection':'real','region_wide':True})
        self.assertEqual(result['qualified'],[])
        self.assertEqual(result['pending'][0]['case_name'],'Lucy and her kittens')
        self.assertIsNone(result['pending'][0]['remaining_minor'])
        self.assertIsNone(app.latest_run)

    def test_city_never_inferred_from_office_address(self):
        app=LocalApp()
        result=app.dispatch('/api/supporter',{'collection':'real','city':'Guelph'})
        self.assertEqual(result['status'],'no_city_match')
        self.assertEqual(result['pending'],[])
        expanded=app.dispatch('/api/supporter',{'collection':'real','city':'Guelph','allow_expansion':True})
        self.assertTrue(expanded['expanded'])
        self.assertIsNone(expanded['pending'][0]['case_city'])

    def test_preference_and_invalid_collection(self):
        app=LocalApp()
        self.assertEqual(app.dispatch('/api/supporter',{'collection':'real'})['status'],'needs_preference')
        with self.assertRaises(ValueError):app.dispatch('/api/supporter',{'collection':'all'})
