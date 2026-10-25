"""Real local H-MEM bridge. Uses a new Node process on each operation."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess

from .core import Review, ROLE_FIELDS


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class MemoryUnavailable(RuntimeError):
    pass


class HMem:
    def __init__(self, reference, state_root, *, node='node', workspace='demo', timeout=15):
        self.reference, self.state_root = Path(reference).resolve(), Path(state_root).resolve()
        self.node, self.workspace, self.timeout = str(node), workspace, timeout
        self.bridge = Path(__file__).with_name('hmem-bridge.mjs')
        if not re.fullmatch(r'[a-zA-Z0-9_-]{1,64}', workspace):
            raise ValueError('Invalid memory workspace')
        if not self.reference.is_file():
            raise MemoryUnavailable('Official H-MEM reference is not configured')

    def call(self, op, case_id, payload=None):
        if not re.fullmatch(r'[a-zA-Z0-9_-]{1,64}', case_id):
            raise ValueError('Invalid memory case scope')
        request = {'op': op, 'case_id': case_id, 'workspace': self.workspace,
                   'reference': str(self.reference), 'state_root': str(self.state_root), 'payload': payload}
        try:
            p = subprocess.run([self.node, '--disable-warning=ExperimentalWarning',
                                '--experimental-transform-types', str(self.bridge)],
                               input=json.dumps(request), text=True, encoding='utf-8',
                               capture_output=True, timeout=self.timeout, check=True)
            return json.loads(p.stdout)
        except (OSError, subprocess.SubprocessError, ValueError):
            raise MemoryUnavailable('H-MEM failed; no fallback to pretend memory') from None


def snapshot(case, result):
    return {'schema_version': 1, 'case_id': case['case_id'], 'run_id': result['run_id'],
            'policy_profile': 'synthetic-core-v1', 'scenario_type': 'synthetic',
            'review_date': case['review_date'], 'claims': deepcopy(result['claims']),
            'open_issues': deepcopy(result['gaps']), 'risk_hold': result['risk_hold'],
            'organization': case['organization'], 'case_name': case['case_name'], 'case_city': case['city'],
            'review_summary': {k: deepcopy(result[k]) for k in (
                'qualified', 'disposition', 'remaining_minor', 'currency', 'gates', 'stop_reason', 'funding_notice')},
            'source_metadata': {k: {f: deepcopy(v[f]) for f in ('publisher', 'origin_group', 'date') if f in v}
                                for k, v in case['sources'].items()},
            'source_fingerprints': {k: fingerprint(v) for k, v in case['sources'].items()},
            'source_refs': [f'synthetic://{case["case_id"]}/{k}' for k in case['sources']],
            'previous_disposition': result['disposition']}


def review_with_memory(case, memory, **limits):
    """Recall does not approve facts: revalidate unchanged evidence, reread changes.

    No personal information; memory workspace is a developer/test namespace.
    Sequential local demo only: concurrent store access is not supported.
    """
    engine = Review(case, **limits)
    recalled = memory.call('recall', case['case_id'])
    entries = recalled['entries']
    prior = entries[0] if entries else None
    eligible = (prior and prior['payload'].get('schema_version') == 1
                and prior['payload'].get('policy_profile') == 'synthetic-core-v1'
                and prior['payload'].get('scenario_type') == 'synthetic')
    reused = []
    if eligible:
        previous = prior['payload']
        engine.event('coordinator', 'memory_recall', 'Official H-MEM returned the previous scoped review',
                     memory_id=prior['memory_id'], previous_issues=previous['open_issues'])
        # A real recall result supplies candidates; current fixture sources and
        # existing evaluator still determine validity, dates and case linkage.
        for role in ROLE_FIELDS:
            candidates = [c for c in previous['claims'].values()
                          if c['field'] in ROLE_FIELDS[role]
                          and c['source_id'] in case['sources']
                          and previous['source_fingerprints'].get(c['source_id'])
                          == fingerprint(case['sources'][c['source_id']])]
            if candidates:
                engine.evaluate(candidates, engine.state['version'])
                reused.extend(c['field'] for c in candidates if c['field'] in engine.state['claims'])
        if previous['open_issues']:
            engine.event('coordinator', 'resume_open_questions',
                         'Recheck remembered unresolved questions using current source versions',
                         fields=[i['field'] for i in previous['open_issues']])
    elif prior:
        engine.event('coordinator', 'memory_not_reused', 'Incompatible snapshot; current review starts without reused claims')
    result = engine.run()
    if eligible and prior['payload'].get('risk_hold') and not result['risk_hold']:
        result.update({'risk_hold': True, 'qualified': False,
                       'disposition': 'cancelled' if result['disposition'] == 'cancelled' else 'pending_evidence',
                       'stop_reason': 'established_risk_hold_requires_authorized_review'})
        result['gates']['organization_risk'] = False
        result['gaps'].append({'field': 'risk_hold', 'reason': 'Previously established hold cannot be cleared automatically',
                               'suggested_channel': 'Authorized business review with checkable new evidence'})
        engine.event('coordinator', 'preserve_risk_hold', 'New source cannot automatically erase an established hold')
        result['trace'] = deepcopy(engine.trace)
    # Cancellation must not replace the useful last review with an empty run.
    saved = ({'memory_id': None} if result['disposition'] == 'cancelled'
             else memory.call('save', case['case_id'], snapshot(case, result)))
    result['memory'] = {'engine': 'official_hmem_reference', 'saved_memory_id': saved['memory_id'],
                        'recalled_memory_id': prior['memory_id'] if eligible else None,
                        'reused_fields': sorted(reused), 'retrieval_trace': recalled['trace'],
                        'previous_open_issues': prior['payload']['open_issues'] if eligible else []}
    result['limits'] = [x for x in result['limits'] if 'H-MEM or provider' not in x]
    result['limits'].append('Real local H-MEM persistence/recall; no live source, NVIDIA, Nightshift or Zetaris calls.')
    return result
