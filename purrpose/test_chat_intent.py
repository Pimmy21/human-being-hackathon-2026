import json
from unittest import TestCase
from .chat_intent import validate_intent


class ModelIntentBoundaryTests(TestCase):
    def test_narrow_discovery_proposal(self):
        obj = {'intent': 'discover', 'city': None, 'region_wide': True}
        self.assertEqual(validate_intent(json.dumps(obj)), obj)

    def test_tool_or_decision_fields_rejected(self):
        for obj in ({'intent': 'pay', 'city': None, 'region_wide': False},
                    {'intent': 'discover', 'city': 'Ottawa', 'region_wide': True},
                    {'intent': 'amount', 'city': None, 'region_wide': True},
                    {'intent': 'discover', 'city': None, 'region_wide': True, 'qualified': True}):
            with self.assertRaises(ValueError):
                validate_intent(json.dumps(obj))

    def test_bad_or_unbounded_response_rejected(self):
        for candidate in ('[]', 'null', 'not json', 'x'*2049):
            with self.assertRaises(ValueError):
                validate_intent(candidate)
