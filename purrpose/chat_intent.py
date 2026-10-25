"""Model-integration boundary: validates a configured model's intent proposal.

A model proposes only a narrow intent; ordinary conversation text cannot become
SQL, tool calls, source refreshes, evidence or a qualification decision.
"""
import json
import re

INTENTS = ('greet', 'discover', 'amount', 'allocation', 'evidence', 'gaps', 'select_real_case', 'history',
           'organization_checklist', 'fictional_demo', 'confirm_expansion', 'outside_area', 'clarify')
CITY_INTENTS = ('discover', 'fictional_demo')


def validate_intent(candidate):
    """Validate a model's JSON proposal before the coordinator uses it."""
    if not isinstance(candidate, str) or len(candidate) > 2048:
        raise ValueError('Invalid intent response')
    fenced = re.fullmatch(r'\s*```(?:json)?\s*(.*?)\s*```\s*', candidate, re.S)
    try:
        value = json.loads(fenced[1] if fenced else candidate)
    except ValueError:
        raise ValueError('Invalid intent response') from None
    if not isinstance(value, dict) or set(value) != {'intent', 'city', 'region_wide'}:
        raise ValueError('Invalid intent schema')
    if value['intent'] not in INTENTS:
        raise ValueError('Unsupported intent')
    if value['region_wide'] is None:
        value['region_wide'] = False  # Null can only mean "not region-wide"; other non-booleans still fail.
    if value['city'] not in (None, 'Ottawa', 'Toronto') or type(value['region_wide']) is not bool:
        raise ValueError('Unsupported preference')
    if value['city'] and value['region_wide']:
        raise ValueError('Ambiguous preference')
    if value['intent'] not in CITY_INTENTS and (value['city'] or value['region_wide']):
        raise ValueError('Non-discovery cannot change preferences')
    return value
