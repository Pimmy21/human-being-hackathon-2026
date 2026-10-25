from copy import deepcopy
import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main, skipUnless

from .__main__ import load_scenario
from .memory import HMem, MemoryUnavailable
from .updates import UpdateService

LINK = 'https://example.invalid/funding'


class UpdateTests(TestCase):
    def setUp(self):
        self.case = load_scenario('complete')
        self.changed = deepcopy(self.case['sources']['funding'])
        self.changed['facts']['raised_minor'] = 120000
        self.calls = []
        def read(url):
            self.calls.append(url)
            return self.changed
        self.service = UpdateService(self.case, read, {LINK: 'funding'})
        self.service.review()

    def test_unapproved_link_cannot_change_status_or_invoke_reader(self):
        r = self.service.notify('http://127.0.0.1/private', request_id='unknown')
        self.assertEqual(r['status'], 'lead_only')
        self.assertEqual(self.calls, [])
        self.assertEqual(self.service.current_state, 'qualified_synthetic')

    def test_change_within_freshness_window_rechecks_now(self):
        r = self.service.notify(LINK, request_id='changed')
        self.assertEqual(r['review']['remaining_minor'], 50000)
        self.assertEqual(r['affected_gates'], ['funding_evidence', 'positive_disclosed_remainder', 'donation_channel'])
        self.assertTrue(any(e['status'] == 'update_awaiting_review' for e in r['update_events']))
        self.assertFalse(r['representation_authority_verified'])

    def test_unchanged_notice_does_not_claim_new_review(self):
        self.changed = deepcopy(self.case['sources']['funding'])
        old_run = self.service.last_review['run_id']
        r = self.service.notify(LINK, request_id='unchanged')
        self.assertEqual(r['status'], 'no_change_observed')
        self.assertEqual(self.service.last_review['run_id'], old_run)

    def test_unconfirmed_notice_failure_does_not_remove_qualification(self):
        self.service.reader = lambda url: None
        r = self.service.notify(LINK, request_id='unknown-change')
        self.assertEqual(r['status'], 'lead_unconfirmed')
        self.assertFalse(r['latest_information_confirmed'])
        self.assertEqual(self.service.current_state, 'qualified_synthetic')

    def test_explicit_latest_failure_blocks_current_result(self):
        self.service.reader = lambda url: None
        r = self.service.notify(LINK, request_id='refresh', explicit_refresh=True)
        self.assertFalse(r['review']['qualified'])
        self.assertIsNone(r['review']['remaining_minor'])

    def test_idempotency_no_repeated_read_and_no_changed_input(self):
        self.service.notify(LINK, request_id='same')
        r = self.service.notify(LINK, request_id='same')
        self.assertTrue(r['idempotent_replay'])
        self.assertEqual(len(self.calls), 1)
        with self.assertRaises(ValueError):
            self.service.notify(LINK, request_id='same', explicit_refresh=True)

    def test_malformed_updated_fact_does_not_pass(self):
        self.changed['facts']['raised_minor'] = 'unknown'
        r = self.service.notify(LINK, request_id='bad-funding')
        self.assertFalse(r['review']['qualified'])
        self.assertIsNone(r['review']['remaining_minor'])

    def test_wrong_case_material_not_accepted(self):
        self.changed['case_id'] = 'ANOTHER-CAT'
        r = self.service.notify(LINK, request_id='wrong-case', explicit_refresh=True)
        self.assertFalse(r['review']['qualified'])

    def test_optional_failure_disclosed_without_blocking_required_gates(self):
        c = deepcopy(self.case)
        c['sources']['context'] = {'role': 'context', 'case_id': c['case_id'], 'status': 'available'}
        service = UpdateService(c, lambda url: None, {LINK: 'context'}, optional_sources=['context'])
        r = service.notify(LINK, request_id='optional', explicit_refresh=True)
        self.assertTrue(r['review']['qualified'])
        self.assertIsNotNone(r['optional_limitation'])

    def test_required_source_cannot_be_declared_optional(self):
        with self.assertRaises(ValueError):
            UpdateService(self.case, lambda url: None, {LINK: 'funding'}, optional_sources=['funding'])

    def test_memory_failure_keeps_update_waiting_not_old_qualified_output(self):
        class BrokenMemory:
            def call(self, *args):
                raise MemoryUnavailable('offline')
        self.service.memory = BrokenMemory()
        r = self.service.notify(LINK, request_id='memory-failure')
        self.assertEqual(r['status'], 'review_incomplete')
        self.assertFalse(r['current_qualification_confirmed'])
        self.assertEqual(self.service.current_state, 'update_awaiting_review')

    @skipUnless(os.environ.get('PURRPOSE_HMEM_REFERENCE'), 'Actual local H-MEM required')
    def test_real_memory_reuses_unaffected_checks_after_update(self):
        with TemporaryDirectory() as state:
            memory = HMem(os.environ['PURRPOSE_HMEM_REFERENCE'], state)
            service = UpdateService(self.case, lambda url: self.changed, {LINK: 'funding'}, memory)
            first = service.review()
            r = service.notify(LINK, request_id='real-memory')
            self.assertEqual(r['review']['memory']['recalled_memory_id'], first['memory']['saved_memory_id'])
            self.assertEqual(len(r['review']['memory']['reused_fields']), 6)
            self.assertEqual(r['review']['usage']['source_reads'], 1)
            self.assertEqual(r['review']['remaining_minor'], 50000)


if __name__ == '__main__':
    main()
