"""Inactive model-integration boundary. No network transport or provider enabled.

A future configured model proposes only a narrow intent; ordinary conversation
text cannot become SQL, tool calls, evidence or a qualification decision.
"""
import json


def validate_intent(candidate):
    """Validate a future model's JSON proposal before a coordinator uses it."""
    if not isinstance(candidate, str) or len(candidate) > 2048:
        raise ValueError('Invalid intent response')
    try:
        value = json.loads(candidate)
    except ValueError:
        raise ValueError('Invalid intent response') from None
    if not isinstance(value, dict) or set(value) != {'intent', 'city', 'region_wide'}:
        raise ValueError('Invalid intent schema')
    if value['intent'] not in ('discover', 'amount', 'evidence', 'gaps', 'clarify'):
        raise ValueError('Unsupported intent')
    if value['city'] not in (None, 'Ottawa', 'Toronto') or type(value['region_wide']) is not bool:
        raise ValueError('Unsupported preference')
    if value['city'] and value['region_wide']:
        raise ValueError('Ambiguous preference')
    if value['intent'] != 'discover' and (value['city'] or value['region_wide']):
        raise ValueError('Non-discovery cannot change preferences')
    return value
