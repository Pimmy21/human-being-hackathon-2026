from unittest import TestCase
from .source_analysis import analyze_read


class SourceAnalysisTests(TestCase):
    def source(self, text, stamp='2026-10-14T02:06:32+00:00'):
        return {'source_id': 'one', 'status': 'read', 'text': text,
                'published_metadata': stamp, 'url': 'https://example.invalid', 'content_sha256': 'abc'}

    def test_timezone_and_grounded_candidate(self):
        text='Lucy, rescued recently, gave birth and is mama of three beautiful kittens!'
        result=analyze_read({'status':'read_complete','sources':[self.source(text)]})
        self.assertEqual(result['publication_dates'][0]['ontario_calendar_date'],'2026-10-13')
        c=result['candidates'][0]
        self.assertEqual(text[c['start']:c['end']],c['quote'])
        self.assertFalse(result['qualified'])
        self.assertIsNone(result['funding']['remaining_minor'])

    def test_failed_read_and_related_links_do_not_supply_claims(self):
        source=self.source('Other story. Related news Lucy gave birth to three beautiful kittens!')
        self.assertFalse(analyze_read({'sources':[source]})['candidates'])
        source.update(status='read_failed')
        self.assertFalse(analyze_read({'sources':[source]})['candidates'])

    def test_undated_candidate_cannot_be_latest(self):
        source=self.source('Lucy gave birth to three beautiful kittens!', 'unknown')
        result=analyze_read({'sources':[source]})
        self.assertIsNone(result['latest_retrieved_statement'])
        self.assertTrue(result['issues'])

    def test_partial_read_never_claims_latest_world_state(self):
        result=analyze_read({'status':'read_incomplete','sources':[self.source('Lucy gave birth to three beautiful kittens!')]})
        self.assertFalse(result['all_configured_sources_read'])
        self.assertFalse(result['current_real_world_state_confirmed'])
