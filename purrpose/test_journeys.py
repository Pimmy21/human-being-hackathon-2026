from unittest import TestCase, main

from .__main__ import load_scenario
from .journeys import Journeys
from .journey_demo import FIXTURE_LINK, render_journeys


def case(scenario='complete', *, city='Ottawa', name='Example Ontario Cat Care', case_id='SYN-MAPLE'):
    c = load_scenario(scenario)
    c.update(city=city, organization=name, case_id=case_id, public_links=[FIXTURE_LINK])
    for source in c['sources'].values():
        source['case_id'] = case_id
    return c


class JourneyTests(TestCase):
    def test_asks_city_without_personal_information_or_review(self):
        app = Journeys([case()])
        result = app.supporter()
        self.assertEqual(result['status'], 'needs_preference')
        self.assertEqual(result['required_personal_information'], [])
        self.assertEqual(app.runs, {})

    def test_case_city_not_headquarters_and_no_silent_expansion(self):
        c = case()
        c['headquarters_city'] = 'Toronto'
        app = Journeys([c])
        self.assertEqual(app.supporter(city='Toronto')['status'], 'no_city_match')
        self.assertEqual(app.runs, {})
        expanded = app.supporter(city='Toronto', allow_expansion=True)
        self.assertTrue(expanded['expanded'])
        self.assertEqual(expanded['qualified'][0]['case_city'], 'Ottawa')

    def test_city_with_pending_case_offers_expansion_but_keeps_pending(self):
        c = case('exhausted')
        app = Journeys([c, case(city='Toronto', case_id='SYN-OTHER')])
        result = app.supporter(city='Ottawa')
        self.assertEqual(result['qualified'], [])
        self.assertEqual(len(result['pending']), 1)
        self.assertFalse(result['expanded'])
        self.assertIsNotNone(result['expansion_question'])
        result = app.supporter(city='Ottawa', allow_expansion=True)
        self.assertEqual(len(result['qualified']), 1)
        self.assertTrue(result['expanded'])

    def test_neutral_sort_and_separate_lists(self):
        app = Journeys([case(city='Toronto', case_id='SYN-T'),
                        case(name='Z Rescue', case_id='SYN-Z'),
                        case(name='a Rescue', case_id='SYN-A'),
                        case('exhausted', name='0 Rescue', case_id='SYN-P')])
        result = app.supporter(region_wide=True)
        self.assertEqual([r['case_id'] for r in result['qualified']], ['SYN-A', 'SYN-Z', 'SYN-T'])
        self.assertEqual([r['case_id'] for r in result['pending']], ['SYN-P'])

    def test_default_view_has_sources_and_no_internal_trace(self):
        result = Journeys([case()]).supporter(city='ottawa')
        row = result['qualified'][0]
        self.assertNotIn('trace', row)
        self.assertTrue(row['evidence'])
        self.assertIn('publisher', row['evidence'][0])
        self.assertIsNone(row['external_donation_url'])

    def test_unknown_city_is_pending_regionwide_only(self):
        app = Journeys([case(city=None)])
        result = app.supporter(region_wide=True)
        self.assertEqual(result['qualified'], [])
        self.assertEqual(len(result['pending']), 1)
        self.assertEqual(app.supporter(city='Toronto')['status'], 'no_city_match')

    def test_organization_receives_actionable_funding_gap(self):
        result = Journeys([case('exhausted')]).organization(public_links=[FIXTURE_LINK])
        gap = next(x for x in result['gap_checklist'] if x['field'] == 'grant_inclusion')
        self.assertIn('already included', gap['what_to_add'])
        self.assertTrue(gap['why'])
        self.assertTrue(gap['where_to_obtain_or_publish'])
        self.assertFalse(result['representation_authority_verified'])
        self.assertFalse(result['materials_fetched'])

    def test_failed_gate_not_just_missing_fields_is_explained(self):
        c = case()
        c['synthetic_risk_profile_ready'] = False
        result = Journeys([c]).organization(public_links=[FIXTURE_LINK])
        self.assertIn('organization_risk', [g['field'] for g in result['gap_checklist']])

    def test_unapproved_private_or_unknown_url_never_read(self):
        app = Journeys([case()])
        for url in ['http://127.0.0.1/secret', 'https://unknown.example/test', 'file:///private']:
            with self.subTest(url=url):
                result = app.organization(public_links=[url])
                self.assertEqual(result['status'], 'unsupported_links')
        self.assertEqual(app.runs, {})

    def test_fully_funded_not_qualified_or_missing_evidence(self):
        c = case()
        c['sources']['funding']['facts']['raised_minor'] = 200000
        result = Journeys([c]).supporter(region_wide=True)
        self.assertEqual(result['qualified'], [])
        self.assertEqual(result['pending'], [])
        self.assertEqual(len(result['no_current_gap']), 1)

    def test_readable_page_escapes_names_and_hides_internal_trace(self):
        app = Journeys([case('exhausted', name='<script>bad()</script>')])
        outputs = {'supporter': app.supporter(city='Ottawa'),
                   'organization': app.organization(public_links=[FIXTURE_LINK])}
        page = render_journeys(outputs, False)
        self.assertNotIn('<script>', page)
        self.assertIn('&lt;script&gt;', page)
        self.assertIn('Not yet known', page)
        self.assertNotIn('plan_revision', page)

    def test_mixed_known_unknown_links_does_not_fetch_anything(self):
        app = Journeys([case()])
        r = app.organization(public_links=[FIXTURE_LINK, 'http://localhost/private'])
        self.assertEqual(r['status'], 'unsupported_links')
        self.assertEqual(app.runs, {})


if __name__ == '__main__':
    main()
