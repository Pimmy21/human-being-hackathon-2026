"""Offline evidence-driven prototype. No model calls, network or H-MEM claims."""
from copy import deepcopy
from datetime import date, datetime
import time
import uuid


ROLE_FIELDS = {
    'identity_risk': ('identity_active', 'in_region', 'risk_complete', 'risk_hold'),
    'rescue_need': ('medical_linked', 'cost_minor'),
    'funding_channel': ('raised_minor', 'grant_minor', 'grant_inclusion', 'channel_owned'),
}
MONEY = {'cost_minor', 'raised_minor', 'grant_minor'}
GATES = ('identity_geography', 'medical_need', 'funding_evidence',
         'positive_disclosed_remainder', 'donation_channel', 'organization_risk')


def fresh(source, today, days):
    try:
        age = (date.fromisoformat(today) - date.fromisoformat(source['date'])).days
        return 0 <= age <= days
    except (KeyError, TypeError, ValueError):
        return False


class Review:
    """Single-writer synchronous coordinator; specialist/evaluator roles use code.

    Source facts are explicitly authored synthetic fixtures. This demonstrates
    conditional orchestration, not autonomous web research or model extraction.
    """

    def __init__(self, case, *, max_repairs=1, task_cap=20, source_cap=8,
                 timeout_seconds=5, cancelled=None):
        if any(type(x) is not int or x < 0 for x in (max_repairs, task_cap, source_cap)):
            raise ValueError('Non-negative integer limits required')
        if timeout_seconds <= 0:
            raise ValueError('Positive deadline required')
        self.case = deepcopy(case)
        if case.get('scenario_type') != 'synthetic':
            raise ValueError('This fixture engine accepts explicitly synthetic cases only')
        if case.get('currency') != 'CAD':
            raise ValueError('Only the CAD fixture profile is implemented')
        self.run_id = str(uuid.uuid4())
        self.state = {'version': 0, 'claims': {}, 'issues': {}, 'repairs': 0}
        self.trace, self.attempts, self.rejected, self.reads = [], set(), [], 0
        self.tasks, self.task_cap, self.source_cap = 0, task_cap, source_cap
        self.max_repairs = max_repairs
        self.deadline = time.monotonic() + timeout_seconds
        self.cancelled = cancelled or (lambda: False)
        self.stop_reason = None
        self.done = False

    def event(self, role, action, reason, **extra):
        self.trace.append({'sequence': len(self.trace) + 1,
                           'run_id': self.run_id, 'task_id': f'{self.run_id}:{len(self.trace)+1}',
                           'plan_revision': self.state['repairs'],
                           'state_version': self.state['version'],
                           'role': role, 'action': action, 'reason': reason,
                           'decision_method': 'deterministic_code',
                           'recorded_at': datetime.now().astimezone().isoformat(), **extra})

    def allowed(self):
        if self.cancelled():
            self.stop_reason = 'cancelled'
        elif time.monotonic() >= self.deadline:
            self.stop_reason = 'deadline_reached'
        return self.stop_reason is None

    def task(self, role, action, reason, **extra):
        if not self.allowed():
            return False
        if self.tasks >= self.task_cap:
            self.stop_reason = 'task_cap_reached'
            return False
        self.tasks += 1
        self.event(role, action, reason, **extra)
        return True

    def read(self, source_id, role, fields):
        source = self.case['sources'].get(source_id)
        key = (source_id, tuple(fields))
        if key in self.attempts:
            self.event('coordinator', 'skip_duplicate', 'Unchanged source/action already attempted', source_id=source_id)
            return
        if self.reads >= self.source_cap:
            self.stop_reason = 'source_cap_reached'
            return
        if not self.task(role, 'read_source', 'Read permitted fixture evidence for assigned fields', source_id=source_id):
            return
        self.attempts.add(key)
        self.reads += 1
        if not source or source.get('status') != 'available':
            self.event(role, 'source_incomplete', 'Fixture source unavailable; not a negative finding',
                       source_id=source_id, error_category='source_unavailable')
            return
        candidates = [{'field': f, 'value': source['facts'][f], 'source_id': source_id,
                       'case_id': source.get('case_id'), 'location': f'facts.{f}'}
                      for f in fields if f in source.get('facts', {})]
        self.evaluate(candidates, self.state['version'])

    def evaluate(self, candidates, input_version):
        if input_version != self.state['version']:
            self.event('evaluator', 'reject_stale', 'Task depends on an older state version')
            return
        if not self.task('evaluator', 'validate', 'Check source support, scope, type and date'):
            return
        accepted = {}
        for c in candidates:
            source = self.case['sources'].get(c.get('source_id'), {})
            f, value = c.get('field'), c.get('value')
            supported = (source.get('status') == 'available' and source.get('case_id') == self.case['case_id']
                         and c.get('case_id') == self.case['case_id']
                         and c.get('location') == f'facts.{f}'
                         and f in source.get('facts', {}) and source['facts'][f] == value
                         and source.get('origin_group') and source.get('publisher'))
            appropriate = (f in ROLE_FIELDS.get(source.get('role'), ())
                           and c.get('source_id') in set(self.case['initial_sources'].values())
                           | set(self.case.get('repair_sources', [])))
            valid_type = ((type(value) is int and value >= 0) if f in MONEY else
                          value in ('included', 'separate', 'unknown') if f == 'grant_inclusion' else
                          type(value) is bool)
            valid_date = fresh(source, self.case['review_date'],
                               7 if source.get('role') == 'funding_channel' else 30)
            if not (supported and appropriate and valid_type and valid_date):
                self.rejected.append(c)
                self.event('evaluator', 'reject_claim', 'Unsupported, mismatched, expired or malformed claim',
                           field=f, source_id=c.get('source_id'))
                continue
            old = self.state['claims'].get(f)
            # A contradictory replacement requires an explicitly superseding,
            # same-publisher, not-older source; agreement alone proves nothing.
            if old and old['value'] != value:
                previous = self.case['sources'][old['source_id']]
                can_replace = (source.get('supersedes') == old['source_id']
                               and source['publisher'] == previous['publisher']
                               and source['date'] >= previous['date'])
                if not can_replace:
                    self.state['issues'][f] = {'category': 'conflict', 'field': f,
                                               'sources': [old['source_id'], c['source_id']]}
                    self.event('evaluator', 'conflict', 'Conflicting source needs a checkable resolution', field=f)
                    continue
            accepted[f] = deepcopy(c)
            if f in source.get('field_provenance', {}):
                accepted[f]['extraction_provenance'] = deepcopy(source['field_provenance'][f])
        if self.allowed() and accepted:
            self.state['claims'].update(accepted)
            self.state['version'] += 1
            for f in accepted:
                if self.state['issues'].get(f, {}).get('category') == 'missing':
                    del self.state['issues'][f]
            self.event('evaluator', 'accept_claims', 'Validated candidates committed by single state writer',
                       fields=sorted(accepted))

    def inspect(self):
        claims = self.state['claims']
        for f in sum(ROLE_FIELDS.values(), ()):
            if f not in claims:
                self.state['issues'].setdefault(f, {'category': 'missing', 'field': f})
        if claims.get('grant_inclusion', {}).get('value') == 'unknown':
            self.state['issues']['grant_inclusion'] = {
                'category': 'funding_overlap', 'field': 'grant_inclusion',
                'required_resolution': 'Establish whether grant is included in raised total; do not guess remainder'}
        elif self.state['issues'].get('grant_inclusion', {}).get('category') == 'funding_overlap':
            del self.state['issues']['grant_inclusion']

    def run(self):
        if self.done:
            return self.result()
        self.task('coordinator', 'plan', 'Assign only checks not already validated')
        for role, fields in ROLE_FIELDS.items():
            if not self.allowed():
                break
            missing = tuple(f for f in fields if f not in self.state['claims'])
            if missing:
                self.read(self.case['initial_sources'][role], role, missing)
            else:
                self.event('coordinator', 'skip_role', 'Required facts already validated', skipped_role=role)
        self.inspect()
        while self.state['issues'] and self.allowed():
            # This first increment has a grant-overlap resolver only. Other
            # issues remain explicit capability gaps, never guessed repairs.
            issue = self.state['issues'].get('grant_inclusion', {})
            if issue.get('category') != 'funding_overlap':
                self.stop_reason = 'no_implemented_resolution_for_remaining_issues'
                break
            if self.state['repairs'] >= self.max_repairs:
                self.stop_reason = 'repair_cap_reached'
                break
            targets = [s for s in self.case.get('repair_sources', [])
                       if (s, ('grant_inclusion',)) not in self.attempts]
            if not targets:
                self.stop_reason = 'no_useful_permitted_source'
                break
            self.state['repairs'] += 1
            if not self.task('coordinator', 'revise_plan', issue['required_resolution'], issue_id='grant_inclusion'):
                break
            if not self.task('dispute_resolver', 'targeted_lookup', 'Use a new permitted source for the specific inclusion issue'):
                break
            self.read(targets[0], 'funding_channel', ('grant_inclusion',))
            self.inspect()
        self.done = True
        self.event('coordinator', 'finish', self.stop_reason or 'checks_completed',
                   open_issues=sorted(self.state['issues']))
        return self.result()

    def result(self):
        values = {k: c['value'] for k, c in self.state['claims'].items()}
        conflict_fields = {k for k, i in self.state['issues'].items() if i['category'] == 'conflict'}
        def known(*names):
            return all(n in values and n not in conflict_fields for n in names)
        funding = (known('cost_minor', 'raised_minor', 'grant_minor', 'grant_inclusion')
                   and values['grant_inclusion'] in ('included', 'separate'))
        remainder = None
        if funding:
            remainder = max(0, values['cost_minor'] - values['raised_minor']
                            - (values['grant_minor'] if values['grant_inclusion'] == 'separate' else 0))
        flags = [known('identity_active', 'in_region') and values['identity_active'] and values['in_region']
                 and bool((self.case.get('city') or '').strip()),
                 known('medical_linked', 'cost_minor') and values['medical_linked'], bool(funding),
                 remainder is not None and remainder > 0,
                 known('channel_owned') and values['channel_owned'],
                 self.case.get('synthetic_risk_profile_ready') is True
                 and known('risk_complete', 'risk_hold') and values['risk_complete'] and not values['risk_hold']]
        gates = dict(zip(GATES, flags))
        qualified = all(flags) and self.stop_reason != 'cancelled'
        held = values.get('risk_hold') is True
        disposition = ('cancelled' if self.stop_reason == 'cancelled' else
                       'completed' if qualified or held or funding and remainder == 0 else 'pending_evidence')
        gaps = [{'field': i['field'], 'reason': i['category'],
                 'suggested_channel': 'Organization public case page or corresponding issuer public statement'}
                for i in self.state['issues'].values()]
        return {'run_id': self.run_id, 'scenario_type': 'synthetic', 'execution_mode': 'fixture',
                'review_date': self.case['review_date'], 'organization': self.case['organization'],
                'case_id': self.case['case_id'], 'case_name': self.case['case_name'], 'city': self.case['city'],
                'qualified': qualified, 'disposition': disposition,
                'remaining_minor': remainder, 'currency': 'CAD', 'gates': gates, 'gaps': gaps,
                'claims': deepcopy(self.state['claims']), 'stop_reason': self.stop_reason or 'checks_completed',
                'risk_hold': held, 'human_review_created': False,
                'funding_notice': "Calculated from the organization's disclosures as of " + self.case['review_date']
                                  + '; all funding has not been independently confirmed.',
                'limits': ['Synthetic evidence only; not a real donation recommendation.',
                           'No model-driven decisions, live sources, H-MEM or provider integrations in this increment.',
                           'Only grant-inclusion dispute resolution is implemented; other gaps remain pending.'],
                'usage': {'external_requests': 0, 'model_calls': 0, 'source_reads': self.reads,
                          'tasks': self.tasks, 'repair_rounds': self.state['repairs']},
                'trace': deepcopy(self.trace)}
