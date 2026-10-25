from unittest import TestCase
from .research_case import assess_saved_research, SOURCES


class SavedResearchTests(TestCase):
    def test_later_update_changes_reported_state_not_qualification(self):
        before = assess_saved_research(as_of='2026-10-24', sources=SOURCES[:1])
        after = assess_saved_research(as_of='2026-10-24')
        self.assertIn('Pregnant', before['latest_reported_state'])
        self.assertIn('three kittens', after['latest_reported_state'])
        self.assertFalse(after['qualified'])
        self.assertIsNone(after['remaining_minor'])
        self.assertEqual(after['distinct_publisher_count'], 1)
        self.assertEqual(len(after['gates']), 6)

    def test_missing_or_future_observations_cannot_supply_state(self):
        result = assess_saved_research(as_of='2026-10-01')
        self.assertIsNone(result['latest_statement_source_id'])
        self.assertEqual(len(result['date_issues']), 2)
        self.assertFalse(result['qualified'])

    def test_assessment_date_does_not_refresh_source_date(self):
        result = assess_saved_research(as_of='2027-01-01')
        self.assertEqual(result['source_observed_on'], '2026-10-24')
        self.assertIn('not a source update', ' '.join(result['limitations']))
