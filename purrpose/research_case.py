"""Saved manual observations. Never certifies a real case or fetches sources."""
from datetime import date

SOURCES = [
    {'source_id': 'lucy-appeal', 'publisher': 'Guelph Humane Society', 'published_on': '2026-10-13',
     'observed_on': '2026-10-24', 'url': 'https://guelphhumane.ca/news/urgent-abandoned-in-a-box-and-pregnant-lucy-needs-your-help/',
     'reported_state': 'Pregnant; organization describes intended care.', 'kind': 'organization_statement'},
    {'source_id': 'lucy-update', 'publisher': 'Guelph Humane Society', 'published_on': '2026-10-14',
     'observed_on': '2026-10-24', 'url': 'https://guelphhumane.ca/news/update-lucy-gave-birth-to-her-kittens-at-ghs/',
     'reported_state': 'Organization reports Lucy gave birth to three kittens at GHS.', 'kind': 'organization_statement'},
]


def assess_saved_research(*, as_of=None, sources=None):
    """Assess source metadata and expose unresolved gates, not medical truth.

    as_of is for tests; HTTP callers cannot supply it or replacement sources.
    Publication-order selection does not establish truth or global freshness.
    """
    today = date.fromisoformat(as_of) if as_of else date.today()
    records = [dict(s) for s in (SOURCES if sources is None else sources)]
    usable, issues = [], []
    for source in records:
        try:
            published = date.fromisoformat(source['published_on'])
            observed = date.fromisoformat(source['observed_on'])
            if published > observed or observed > today:
                raise ValueError
        except (ValueError, KeyError, TypeError):
            issues.append({'source_id': source.get('source_id'), 'issue': 'date_needs_clarification'})
            continue
        usable.append(source)
    latest = max(usable, key=lambda s: s['published_on']) if usable else None
    gaps = [
        ('identity_geography', 'CRA identity/status was manually observed on 24 October 2026; actual case treatment location remains unverified. This is not a live registry recheck.'),
        ('medical_need', 'A current corresponding clinical statement or estimate has not been checked.'),
        ('funding_evidence', 'Case cost, funds raised, grants and allocation are not established.'),
        ('positive_disclosed_remainder', 'No supported remaining amount can be calculated.'),
        ('donation_channel', 'Official-page linked Lucy form was manually read; payment recipient/settlement ownership has not been independently verified.'),
        ('organization_risk', 'Approved current regional risk checks have not been completed.'),
    ]
    return {'case_id': 'research-lucy-ghs', 'organization_display_name': 'Guelph Humane Society',
            'legal_name_verified': False, 'case_name': 'Lucy and her kittens',
            'external_form_observation': {
                'title': 'Lucy - Emergency Appeal - October 2026',
                'observed_on': '2026-10-24', 'method': 'manual_browser_read_only',
                'allocation_reported': 'If appeal donations exceed care costs, surplus supports other animals arriving at GHS.',
                'case_cost_minor': None, 'raised_minor': None, 'remaining_minor': None,
                'recipient_settlement_verified': False, 'payment_submitted': False,
                'note': 'Visible gift options are donation choices, not a cost, target or funding gap. Earlier research-tool cache miss is retained as attempt history, not current page availability.'},
            'official_identity_observation': {
                'legal_name': 'THE GUELPH HUMANE SOCIETY INCORPORATED',
                'registration_number': '119236305RR0001', 'status_displayed': 'Registered',
                'website_displayed': 'https://guelphhumane.ca', 'observed_on': '2026-10-24',
                'source_url': 'https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/dsplyRprtngPrd/119236305RR0001',
                'method': 'manual_official_browser_review', 'rechecked_now': False,
                'note': 'Saved official observation; legal_name_verified above remains false for runtime verification. Case geography and full identity gate are incomplete.'},
            'mode': 'saved_manual_research', 'status': 'pending_verification',
            'qualified': False, 'remaining_minor': None, 'currency': 'CAD',
            'assessment_date': today.isoformat(), 'source_observed_on': '2026-10-24',
            'latest_reported_state': latest['reported_state'] if latest else 'No usable dated observation.',
            'latest_statement_source_id': latest['source_id'] if latest else None,
            'sources': records, 'date_issues': issues,
            'distinct_publisher_count': len({s['publisher'] for s in usable}),
            'independent_medical_verification': False,
            'gates': [{'gate': key, 'status': 'not_established', 'explanation': why} for key, why in gaps],
            'next_evidence': ['Current case update and actual treatment city.',
                              'Appropriately redacted dated corresponding clinical material.',
                              'Same-case cost, funding total, dates, grants and allocation.',
                              'Official identity, recipient linkage and approved risk checks.'],
            'limitations': ['Saved manual observations; sources were not fetched again.',
                            'Assessment date is not a source update or freshness guarantee.',
                            'Same-publisher articles are not independent corroboration.',
                            'No autonomous discovery, model call or H-MEM ingestion.',
                            'Missing information does not imply wrongdoing.']}
