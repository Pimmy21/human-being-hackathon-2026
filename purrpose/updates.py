"""Screened update intake over an explicit fixture source reader.

No background monitor, arbitrary URL fetch, private upload or paid inference.
The reader is a backend capability, never code supplied by a notification.
"""
from copy import deepcopy

from .core import Review
from .memory import MemoryUnavailable, fingerprint, review_with_memory

IMPACT = {'identity_risk': ['identity_geography', 'organization_risk'],
          'rescue_need': ['medical_need', 'funding_evidence', 'positive_disclosed_remainder'],
          'funding_channel': ['funding_evidence', 'positive_disclosed_remainder', 'donation_channel']}


class UpdateService:
    def __init__(self, case, reader, permitted_links, memory=None, optional_sources=()):
        self.case, self.reader = deepcopy(case), reader
        self.links = dict(permitted_links)
        self.memory = memory
        self.optional = set(optional_sources)
        if not set(self.links.values()).issubset(self.case['sources']):
            raise ValueError('Every approved link must map to an existing configured source')
        mandatory = set(self.case['initial_sources'].values())
        if self.optional & mandatory:
            raise ValueError('A required source cannot be configured optional')
        self.last_review = None
        self.version = 0
        self.events = []
        self.completed = {}
        self.current_state = 'unreviewed'

    def review(self):
        self.last_review = (review_with_memory(self.case, self.memory) if self.memory else Review(self.case).run())
        self.current_state = 'qualified_synthetic' if self.last_review['qualified'] else 'not_qualified'
        return deepcopy(self.last_review)

    def notify(self, url, *, request_id, explicit_refresh=False):
        if not isinstance(url, str) or type(explicit_refresh) is not bool:
            raise ValueError('A URL string and explicit boolean refresh flag are required')
        if not isinstance(request_id, str) or not 1 <= len(request_id) <= 100:
            raise ValueError('A bounded idempotency key is required')
        request = (url, explicit_refresh)
        if request_id in self.completed:
            previous_request, response = self.completed[request_id]
            if request != previous_request:
                raise ValueError('An idempotency key cannot be reused for different inputs')
            return {**deepcopy(response), 'idempotent_replay': True,
                    'current_case_version': self.version,
                    'message': 'Saved task response, not a new source read or a claim of current qualification.'}
        start = len(self.events)
        def finish(status, **extra):
            result = {'status': status, 'case_version': self.version,
                      'request_id': request_id, 'idempotent_replay': False,
                      'update_events': deepcopy(self.events[start:]), **extra}
            self.completed[request_id] = (request, deepcopy(result))
            return result
        source_id = self.links.get(url)
        if source_id is None:
            self.events.append({'stage': 'screen_notice', 'status': 'lead_only', 'reason': 'unapproved_link'})
            return finish('lead_only', source_read=False, qualification_changed=False,
                          message='Unapproved link not read; a notification is not evidence or representation authority.')
        self.events.append({'stage': 'source_read', 'status': 'started', 'source_id': source_id})
        old = self.case['sources'][source_id]
        try:
            new = deepcopy(self.reader(url))
            if (not isinstance(new, dict) or new.get('status') != 'available'
                    or new.get('case_id') != self.case['case_id'] or new.get('role') != old.get('role')):
                raise ValueError('Unreadable or mismatched source')
        except Exception:
            self.events.append({'stage': 'source_read', 'status': 'incomplete', 'source_id': source_id})
            if not explicit_refresh:
                return finish('lead_unconfirmed', source_read=True, qualification_changed=False,
                              latest_information_confirmed=False,
                              message='Update could not be confirmed. Prior review was not silently replaced or claimed current.')
            new = {**deepcopy(old), 'status': 'unavailable'}
        changed = fingerprint(old) != fingerprint(new)
        if not changed and not explicit_refresh:
            self.events.append({'stage': 'change_detection', 'status': 'unchanged', 'source_id': source_id})
            return finish('no_change_observed', source_read=True, qualification_changed=False,
                          message='No source change observed; normal freshness checks still apply on result access.')
        affected = [] if source_id in self.optional else IMPACT.get(old.get('role'))
        if affected is None:
            # The impact is unknown: do not assume it is harmless.
            affected = ['all_six_gates']
            for sid in self.case['initial_sources'].values():
                self.case['sources'][sid]['status'] = 'unavailable'
        if affected:
            self.current_state = 'update_awaiting_review'
            self.events.append({'stage': 'qualification', 'status': 'update_awaiting_review',
                                'affected_gates': affected})
        self.case['sources'][source_id] = new
        self.version += 1
        try:
            reviewed = self.review()
        except MemoryUnavailable:
            self.current_state = 'update_awaiting_review'
            self.events.append({'stage': 'memory_re_review', 'status': 'incomplete'})
            return finish('review_incomplete', current_qualification_confirmed=False,
                          message='Source update observed but memory/review could not complete. Prior result is not presented as current.')
        limitation = None
        if source_id in self.optional and new['status'] != 'available':
            limitation = 'Optional public material could not be checked; required evidence checks remain separate.'
        self.events.append({'stage': 're_review', 'status': 'completed', 'affected_gates': affected,
                            'qualified': reviewed['qualified']})
        return finish('reviewed', source_read=True, review=reviewed, affected_gates=affected,
                      optional_limitation=limitation, representation_authority_verified=False,
                      human_review_created=False)
