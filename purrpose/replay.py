"""Consume a recorded NVIDIA candidate after independent current-source checks.

Replay never makes a network request. A saved response is not current evidence.
The application supplies the current passage separately; fingerprints and quote
validation must match before this narrow labelled-cost adapter supplies a fact.
"""
from copy import deepcopy
import json

from .core import Review
from .extraction import ExtractionError, validate_candidates
from .memory import fingerprint, review_with_memory
from .nvidia_demo import validate_cost

RAW_FIELDS = {'field', 'value', 'source_id', 'case_id', 'passage_id', 'quote'}
META_FIELDS = {'source_version', 'authority', 'requires_domain_validation'}


def prepare_cost(case, capture, passage):
    prepared = deepcopy(case)
    medical = prepared['sources'][prepared['initial_sources']['rescue_need']]
    # No prefilled cost may mask failure of the extraction under test.
    medical['facts'].pop('cost_minor', None)
    info = {'mode': 'recorded_response_replay', 'stage': 'candidate_replay_validation', 'new_model_calls': 0,
            'status': 'held', 'reason': 'capture_not_usable'}
    try:
        if (capture.get('provider') != 'nvidia' or capture.get('scenario_type') != 'synthetic'
                or passage['case_id'] != case['case_id']
                or capture.get('source_fingerprint') != fingerprint(passage)):
            raise ExtractionError('capture_source_version_mismatch')
        candidates = capture['candidates']
        if not isinstance(candidates, list) or not candidates:
            raise ExtractionError('missing_recorded_candidates')
        raw = []
        for c in candidates:
            if not isinstance(c, dict) or not RAW_FIELDS.issubset(c) or set(c)-RAW_FIELDS-META_FIELDS:
                raise ExtractionError('recorded_candidate_schema_invalid')
            if c.get('source_version') != passage['source_version']:
                raise ExtractionError('capture_source_version_mismatch')
            raw.append({k: c[k] for k in RAW_FIELDS})
        checked = validate_candidates(json.dumps({'claims': raw}), [passage])
        costs = [c for c in checked['candidates'] if c['field'] == 'cost_minor']
        if checked['held'] or len(costs) != 1:
            raise ExtractionError('recorded_candidate_not_uniquely_grounded')
        candidate = costs[0]
        amount = validate_cost(candidate, passage)
        if amount is None:
            raise ExtractionError('cost_domain_validation_failed')
        # This code result, not the model's assertion, supplies the core field.
        medical['facts']['cost_minor'] = amount
        medical['field_provenance'] = {'cost_minor': {
            'route': 'nvidia_recorded_response_replay', 'model': capture.get('model'),
            'original_source_id': passage['source_id'], 'passage_id': passage['passage_id'],
            'source_version': passage['source_version'], 'source_fingerprint': fingerprint(passage),
            'quote': candidate['quote'], 'validation': 'exact_quote_and_labelled_CAD_cost',
            'original_capture_usage': capture.get('original_usage'), 'new_model_calls': 0}}
        info.update(status='validated_cost_attached', reason='Current passage and code-validated amount match capture',
                    validated_cost_minor=amount)
    except (ExtractionError, KeyError, TypeError) as exc:
        info['reason'] = exc.category if isinstance(exc, ExtractionError) else 'invalid_capture_or_passage'
    return prepared, info


def review_replay(case, capture, passage, memory=None):
    prepared, info = prepare_cost(case, capture, passage)
    result = review_with_memory(prepared, memory) if memory else Review(prepared).run()
    result['extraction_replay'] = info
    result['execution_mode'] = 'replay'
    result['limits'].append('NVIDIA candidate came from a recorded earlier request, not a new live call.')
    return prepared, result
