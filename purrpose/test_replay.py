import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main, skipUnless

from .__main__ import load_scenario
from .journeys import public_record
from .memory import HMem, fingerprint
from .replay import review_replay


def bundle():
    return json.loads((Path(__file__).parent/'fixtures/nvidia-capture.json').read_text())


class ReplayTests(TestCase):
    def run_replay(self, data=None, case=None):
        data = data or bundle()
        return review_replay(case or load_scenario('complete'), data['capture'], data['current_passage'])

    def test_revalidated_capture_cost_reaches_core_and_user_output(self):
        case, r = self.run_replay()
        self.assertTrue(r['qualified'])
        self.assertEqual(r['remaining_minor'], 100000)
        self.assertEqual(r['execution_mode'], 'replay')
        self.assertEqual(r['usage']['model_calls'], 0)
        cost = next(e for e in public_record(case, r)['evidence'] if e['field'] == 'cost_minor')
        self.assertEqual(cost['extraction_provenance']['route'], 'nvidia_recorded_response_replay')
        self.assertEqual(cost['extraction_provenance']['original_capture_usage']['total_tokens'], 281)

    def test_incorrect_number_cannot_hide_behind_prefilled_fixture_cost(self):
        data = bundle()
        data['capture']['candidates'][0]['value'] = 999999
        case, r = self.run_replay(data)
        self.assertNotIn('cost_minor', case['sources']['medical']['facts'])
        self.assertIsNone(r['remaining_minor'])
        self.assertFalse(r['qualified'])

    def test_changed_current_passage_invalidates_recorded_response(self):
        data = bundle()
        data['current_passage']['text'] = 'Synthetic Maple case. Treatment estimate: CAD 3,000.00.'
        _, r = self.run_replay(data)
        self.assertEqual(r['extraction_replay']['reason'], 'capture_source_version_mismatch')
        self.assertIsNone(r['remaining_minor'])

    def test_wrong_case_or_version_cannot_replay(self):
        for change in ({'case_id': 'OTHER'}, {'source_version': 'new'}):
            with self.subTest(change=change):
                data = bundle()
                data['current_passage'].update(change)
                self.assertFalse(self.run_replay(data)[1]['qualified'])

    def test_matching_fingerprint_does_not_prove_medical_cost_meaning(self):
        data = bundle()
        data['current_passage']['text'] = 'A volunteer raised CAD 2,000.00.'
        data['capture']['source_fingerprint'] = fingerprint(data['current_passage'])
        data['capture']['candidates'][0]['quote'] = data['current_passage']['text']
        _, r = self.run_replay(data)
        self.assertEqual(r['extraction_replay']['reason'], 'cost_domain_validation_failed')

    def test_ambiguous_duplicate_cost_not_accepted(self):
        data = bundle()
        data['capture']['candidates'] *= 2
        self.assertFalse(self.run_replay(data)[1]['qualified'])

    def test_status_injection_cannot_change_case_gates(self):
        data = bundle()
        data['capture']['candidates'][0]['qualified'] = True
        self.assertFalse(self.run_replay(data)[1]['qualified'])

    def test_valid_extraction_does_not_bypass_other_checks(self):
        for flag in ('medical_linked', 'risk_complete'):
            with self.subTest(flag=flag):
                case = load_scenario('complete')
                source = 'medical' if flag == 'medical_linked' else 'registry-risk'
                case['sources'][source]['facts'][flag] = False
                self.assertFalse(self.run_replay(case=case)[1]['qualified'])

    def test_grant_ambiguity_still_triggers_existing_dispute_path(self):
        _, r = self.run_replay(case=load_scenario('repair'))
        self.assertEqual(r['usage']['repair_rounds'], 1)
        self.assertEqual(r['remaining_minor'], 100000)
        self.assertTrue(any(e['role'] == 'dispute_resolver' for e in r['trace']))

    @skipUnless(os.environ.get('PURRPOSE_HMEM_REFERENCE'), 'Real local H-MEM reference required')
    def test_saved_cost_cannot_mask_later_invalid_capture(self):
        with TemporaryDirectory() as state:
            memory = HMem(os.environ['PURRPOSE_HMEM_REFERENCE'], state)
            data = bundle()
            _, first = review_replay(load_scenario('complete'), data['capture'], data['current_passage'], memory)
            self.assertTrue(first['qualified'])
            data['capture']['candidates'][0]['value'] = 999999
            _, second = review_replay(load_scenario('complete'), data['capture'], data['current_passage'], memory)
            self.assertFalse(second['qualified'])
            self.assertIsNone(second['remaining_minor'])
            self.assertNotIn('cost_minor', second['memory']['reused_fields'])


if __name__ == '__main__':
    main()
