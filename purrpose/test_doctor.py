from unittest import TestCase
from unittest.mock import patch
from .doctor import inspect_environment


class DoctorTests(TestCase):
    def test_missing_node_does_not_claim_memory_or_block_offline(self):
        with patch('purrpose.doctor.subprocess.run',side_effect=FileNotFoundError):
            result=inspect_environment()
        self.assertTrue(result['offline_ready'])
        self.assertFalse(result['node24_for_hmem'])
        self.assertEqual(result['hmem_reference'],'not_configured')
        self.assertFalse(result['live_integration_verified_by_this_check'])

    def test_nonexistent_reference_remains_missing(self):
        result=inspect_environment(reference='nonexistent-purrpose-test-reference.ts')
        self.assertEqual(result['hmem_reference'],'reference_missing')
        self.assertEqual(result['network_requests'],0)
