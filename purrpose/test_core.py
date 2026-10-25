from unittest import TestCase, main

from .__main__ import load_scenario, report
from .core import Review


class AdaptiveReviewTests(TestCase):
    def run_case(self, name='complete', **limits):
        return Review(load_scenario(name), **limits).run()

    def test_complete_skips_dispute_and_paid_work(self):
        r = self.run_case()
        self.assertTrue(r['qualified'])
        self.assertEqual(r['remaining_minor'], 100000)
        self.assertFalse(any(e['role'] == 'dispute_resolver' for e in r['trace']))
        self.assertEqual(r['usage']['model_calls'], 0)

    def test_specific_issue_changes_plan_and_resolves(self):
        r = self.run_case('repair')
        self.assertTrue(r['qualified'])
        self.assertEqual(r['remaining_minor'], 100000)
        self.assertEqual(r['usage']['repair_rounds'], 1)
        self.assertEqual(r['claims']['grant_inclusion']['source_id'], 'funding-update')
        self.assertEqual(sum(e['action'] == 'revise_plan' for e in r['trace']), 1)
        self.assertEqual(sum(e['role'] == 'identity_risk' for e in r['trace']), 1)

    def test_unresolved_is_unknown_without_human_ticket(self):
        r = self.run_case('exhausted')
        self.assertFalse(r['qualified'])
        self.assertIsNone(r['remaining_minor'])
        self.assertFalse(r['human_review_created'])
        self.assertEqual(r['stop_reason'], 'repair_cap_reached')
        self.assertEqual(r['disposition'], 'pending_evidence')

    def test_included_grant_not_subtracted_twice(self):
        c = load_scenario('complete')
        c['sources']['funding']['facts']['grant_inclusion'] = 'included'
        self.assertEqual(Review(c).run()['remaining_minor'], 130000)

    def test_source_outage_is_not_finding_against_organization(self):
        c = load_scenario('repair')
        c['sources']['funding-update']['status'] = 'unavailable'
        r = Review(c).run()
        self.assertIsNone(r['remaining_minor'])
        self.assertFalse(r['risk_hold'])
        self.assertEqual(sum(e['action'] == 'source_incomplete' for e in r['trace']), 1)

    def test_wrong_cat_invoice_cannot_pass_medical_gate(self):
        c = load_scenario('complete')
        c['sources']['medical']['case_id'] = 'ANOTHER-CAT'
        r = Review(c).run()
        self.assertFalse(r['gates']['medical_need'])
        self.assertNotIn('cost_minor', r['claims'])

    def test_invalid_money_types_cannot_become_authority(self):
        for value in (True, '200000', -1, None):
            with self.subTest(value=value):
                c = load_scenario('complete')
                c['sources']['medical']['facts']['cost_minor'] = value
                self.assertIsNone(Review(c).run()['remaining_minor'])

    def test_funding_age_boundary_and_future_date(self):
        for date, expected in [('2026-10-17', True), ('2026-10-16', False), ('2026-10-25', False)]:
            with self.subTest(date=date):
                c = load_scenario('complete')
                c['sources']['funding']['date'] = date
                self.assertEqual(Review(c).run()['gates']['funding_evidence'], expected)

    def test_incomplete_risk_profile_blocks_qualification(self):
        c = load_scenario('complete')
        c['synthetic_risk_profile_ready'] = False
        self.assertFalse(Review(c).run()['qualified'])

    def test_established_hold_cannot_be_repaired_away(self):
        c = load_scenario('repair')
        c['sources']['registry-risk']['facts']['risk_hold'] = True
        r = Review(c).run()
        self.assertTrue(r['risk_hold'])
        self.assertFalse(r['qualified'])

    def test_task_source_and_repair_caps_stop(self):
        for limits in ({'task_cap': 1}, {'source_cap': 1}, {'max_repairs': 0}):
            with self.subTest(limits=limits):
                r = self.run_case('repair', **limits)
                self.assertFalse(r['qualified'])
                self.assertLessEqual(r['usage']['tasks'], limits.get('task_cap', 20))
                self.assertLessEqual(r['usage']['source_reads'], limits.get('source_cap', 8))

    def test_cancellation_does_not_publish_qualification(self):
        r = self.run_case(cancelled=lambda: True)
        self.assertEqual(r['disposition'], 'cancelled')
        self.assertEqual(r['usage']['source_reads'], 0)

    def test_stale_result_and_unsupported_citation_rejected(self):
        engine = Review(load_scenario('complete'))
        engine.evaluate([{'field': 'cost_minor', 'value': 10, 'source_id': 'invented'}], 0)
        self.assertNotIn('cost_minor', engine.state['claims'])
        engine.evaluate([], 123)
        self.assertEqual(engine.trace[-1]['action'], 'reject_stale')

    def test_unsourced_conflicting_update_does_not_replace_claim(self):
        c = load_scenario('repair')
        del c['sources']['funding-update']['supersedes']
        r = Review(c).run()
        self.assertIsNone(r['remaining_minor'])
        self.assertEqual(r['claims']['grant_inclusion']['value'], 'unknown')

    def test_fully_funded_is_not_misconduct(self):
        c = load_scenario('complete')
        c['sources']['funding']['facts']['raised_minor'] = 250000
        r = Review(c).run()
        self.assertEqual(r['remaining_minor'], 0)
        self.assertFalse(r['qualified'])
        self.assertFalse(r['risk_hold'])

    def test_repeat_same_review_does_not_duplicate_work(self):
        engine = Review(load_scenario('repair'))
        first, second = engine.run(), engine.run()
        self.assertEqual(first, second)

    def test_live_material_cannot_be_mislabelled_as_fixture(self):
        c = load_scenario('complete')
        c['scenario_type'] = 'public_real'
        with self.assertRaises(ValueError):
            Review(c)

    def test_report_escapes_source_text(self):
        r = self.run_case()
        r['organization'] = '<script>bad()</script>'
        page = report({'complete': r})
        self.assertNotIn('<script>', page)
        self.assertIn('&lt;script&gt;', page)


if __name__ == '__main__':
    main()
