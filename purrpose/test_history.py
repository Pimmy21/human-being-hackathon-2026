from copy import deepcopy
import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main, skipUnless

from .history import historical_answer, history_from_memory, parse_cutoff
from .memory import HMem, review_with_memory
from .memory_demo import case_for_phase


def entry(number, recorded, remaining, *, source_date='2026-10-01'):
    return {'memory_id': f'mem-{number}', 'system_recorded_at': recorded,
            'payload': {'case_id': 'SYN-MAPLE', 'review_date': source_date, 'scenario_type': 'synthetic',
                        'review_summary': {'remaining_minor': remaining, 'disposition': 'pending_evidence' if remaining is None else 'completed'},
                        'open_issues': [{'field': 'grant_inclusion'}] if remaining is None else [],
                        'claims': {}, 'source_refs': ['synthetic://test']}}


class HistoryTests(TestCase):
    def setUp(self):
        self.first = entry(1, '2026-10-24T14:00:00Z', None)
        self.second = entry(2, '2026-10-24T15:00:00Z', 100000)

    def test_cutoff_preserves_old_unknown_not_later_amount(self):
        result = historical_answer([self.first, self.second], 'SYN-MAPLE', '2026-10-24T14:30:00Z')
        self.assertEqual(result['memory_id'], 'mem-1')
        self.assertIsNone(result['recorded_result']['remaining_minor'])

    def test_exact_cutoff_is_inclusive(self):
        result = historical_answer([self.first, self.second], 'SYN-MAPLE', '2026-10-24T15:00:00Z')
        self.assertEqual(result['memory_id'], 'mem-2')

    def test_before_any_record_explicitly_unavailable(self):
        result = historical_answer([self.first], 'SYN-MAPLE', '2020-01-01T00:00:00Z')
        self.assertEqual(result['status'], 'history_unavailable')
        self.assertIsNone(result['historical_qualification'])

    def test_no_recorded_time_cannot_be_inferred_from_source_date(self):
        del self.first['system_recorded_at']
        result = historical_answer([self.first], 'SYN-MAPLE')
        self.assertEqual(result['status'], 'history_unavailable')
        self.assertEqual(result['records_with_unknown_system_time'], 1)

    def test_legacy_summary_not_reconstructed_from_current_logic(self):
        del self.first['payload']['review_summary']
        result = historical_answer([self.first], 'SYN-MAPLE')
        self.assertEqual(result['status'], 'partial_legacy_record')
        self.assertIsNone(result['recorded_result'])

    def test_wrong_case_ignored(self):
        result = historical_answer([self.first], 'ANOTHER-CASE')
        self.assertEqual(result['status'], 'history_unavailable')

    def test_timezone_offsets_compare_same_instants(self):
        result = historical_answer([self.first, self.second], 'SYN-MAPLE', '2026-10-24T10:00:00-04:00')
        self.assertEqual(result['memory_id'], 'mem-1')

    def test_ambiguous_or_malformed_cutoff_rejected(self):
        for value in ('2026-10-24', '2026-10-24T14:00:00', 'not-time', 123):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_cutoff(value)

    def test_later_discovered_old_source_not_used_in_past(self):
        self.second['payload']['review_date'] = '2020-01-01'
        result = historical_answer([self.first, self.second], 'SYN-MAPLE', '2026-10-24T14:10:00Z')
        self.assertEqual(result['memory_id'], 'mem-1')

    def test_returned_data_does_not_mutate_saved_records(self):
        original = deepcopy(self.first)
        result = historical_answer([self.first], 'SYN-MAPLE')
        result['recorded_result']['remaining_minor'] = 123
        self.assertEqual(self.first, original)
        self.assertFalse(result['source_urls_rechecked_now'])
        self.assertFalse(result['current_qualification_implied'])

    @skipUnless(os.environ.get('PURRPOSE_HMEM_REFERENCE'), 'Actual H-MEM reference required')
    def test_actual_memory_creation_times_drive_history_after_update(self):
        with TemporaryDirectory() as root:
            memory = HMem(os.environ['PURRPOSE_HMEM_REFERENCE'], root)
            review_with_memory(case_for_phase('first'), memory)
            cutoff = history_from_memory(memory, 'SYN-MAPLE')['system_recorded_at']
            review_with_memory(case_for_phase('update'), memory)
            old = history_from_memory(memory, 'SYN-MAPLE', cutoff)
            latest = history_from_memory(memory, 'SYN-MAPLE')
            self.assertIsNone(old['recorded_result']['remaining_minor'])
            self.assertEqual(old['recorded_unknowns'][0]['field'], 'grant_inclusion')
            self.assertEqual(latest['recorded_result']['remaining_minor'], 100000)
            self.assertEqual(old['system_recorded_at'], cutoff)


if __name__ == '__main__':
    main()
