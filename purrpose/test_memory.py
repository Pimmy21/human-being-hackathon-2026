"""Integration tests call the real official H-MEM reference, not a fake store."""
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main, skipUnless

from .memory import HMem, MemoryUnavailable, review_with_memory
from .memory_demo import case_for_phase

REFERENCE = os.environ.get('PURRPOSE_HMEM_REFERENCE')


@skipUnless(REFERENCE, 'Set PURRPOSE_HMEM_REFERENCE for real local H-MEM integration tests')
class HMemIntegrationTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.memory = HMem(REFERENCE, self.root)

    def test_restart_recall_drives_incremental_update(self):
        first = review_with_memory(case_for_phase('first'), self.memory)
        self.assertIsNone(first['remaining_minor'])
        restarted = HMem(REFERENCE, self.root)
        second = review_with_memory(case_for_phase('update'), restarted)
        self.assertEqual(second['remaining_minor'], 100000)
        self.assertEqual(second['memory']['recalled_memory_id'], first['memory']['saved_memory_id'])
        self.assertEqual(len(second['memory']['previous_open_issues']), 1)
        self.assertEqual(second['usage']['source_reads'], 1)
        self.assertEqual(len(second['memory']['reused_fields']), 6)
        self.assertFalse(any(e['role'] == 'identity_risk' for e in second['trace']))
        recalled = restarted.call('recall', 'SYN-MAPLE')
        self.assertEqual(len(recalled['entries']), 2)
        self.assertEqual(recalled['entries'][-1]['payload']['previous_disposition'], 'pending_evidence')
        self.assertTrue((self.root/'demo/SYN-MAPLE/ledger.jsonl').is_file())

    def test_workspace_and_case_isolation(self):
        review_with_memory(case_for_phase('first'), self.memory)
        self.assertEqual(HMem(REFERENCE, self.root, workspace='other').call('recall', 'SYN-MAPLE')['entries'], [])
        self.assertEqual(self.memory.call('recall', 'OTHER-CASE')['entries'], [])
        with self.assertRaises(ValueError):
            self.memory.call('recall', '../escape')

    def test_unchanged_but_expired_evidence_not_reused(self):
        review_with_memory(case_for_phase('first'), self.memory)
        c = case_for_phase('update')
        c['review_date'] = '2026-12-01'
        second = review_with_memory(c, self.memory)
        self.assertFalse(second['qualified'])
        self.assertEqual(second['memory']['reused_fields'], [])
        self.assertIsNone(second['remaining_minor'])

    def test_stored_hold_survives_current_source_removal(self):
        c = case_for_phase('first')
        c['sources']['registry-risk']['facts']['risk_hold'] = True
        review_with_memory(c, self.memory)
        second = review_with_memory(case_for_phase('update'), self.memory)
        self.assertTrue(second['risk_hold'])
        self.assertFalse(second['qualified'])
        self.assertEqual(second['stop_reason'], 'established_risk_hold_requires_authorized_review')

    def test_save_idempotency_and_missing_runtime(self):
        result = review_with_memory(case_for_phase('first'), self.memory)
        previous = self.memory.call('recall', 'SYN-MAPLE')['entries'][0]['payload']
        saved = self.memory.call('save', 'SYN-MAPLE', previous)
        self.assertTrue(saved['reused'])
        self.assertEqual(saved['memory_id'], result['memory']['saved_memory_id'])
        broken = HMem(REFERENCE, self.root, node=str(self.root/'missing-node'))
        with self.assertRaises(MemoryUnavailable):
            broken.call('recall', 'SYN-MAPLE')

    def test_cancelled_review_does_not_replace_last_snapshot(self):
        first = review_with_memory(case_for_phase('first'), self.memory)
        cancelled = review_with_memory(case_for_phase('update'), self.memory, cancelled=lambda: True)
        self.assertEqual(cancelled['disposition'], 'cancelled')
        self.assertIsNone(cancelled['memory']['saved_memory_id'])
        entries = self.memory.call('recall', 'SYN-MAPLE')['entries']
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['memory_id'], first['memory']['saved_memory_id'])


if __name__ == '__main__':
    main()
