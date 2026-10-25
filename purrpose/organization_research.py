"""Actionable organization gaps for configured real public links; no intake/fetch."""
from copy import deepcopy
from .research_case import SOURCES, assess_saved_research

LINKS = {s['url'] for s in SOURCES}
ITEMS = [
    ('case_location', 'Clarify where Lucy and her kittens are actually receiving care.',
     'The organization address does not establish the treatment location.',
     'A dated public case update; identify city and appropriately shareable provider information.', 'organization'),
    ('clinical_material', 'Link current dated clinical material to this cat family.',
     'A care story is not independent clinical confirmation.',
     'An appropriately redacted public estimate or issuer statement, with case linkage and date.', 'organization'),
    ('cost_and_funding', 'Publish a same-case cost and funding breakdown with an as-of date.',
     'Unknown totals cannot establish a positive remaining need.',
     'Public appeal update: care budget/estimate, received total, grants and whether grants are included.', 'organization'),
    ('allocation', 'Keep the published surplus policy visible and clarify how case funds are counted.',
     'The form already says surplus may help other GHS animals; it does not give current case totals.',
     'The public appeal and official donation page, with consistent allocation and date.', 'organization'),
    ('identity_channel', 'Recheck official identity, recipient linkage and case geography.',
     'A saved manual CRA observation is available, but runtime/current recipient checks are incomplete.',
     'Applicable official registry and permitted organization-to-payment-recipient evidence; no payment test.', 'system'),
    ('risk_coverage', 'Complete the approved regional risk checks.',
     'The system has not completed required coverage. This is not an allegation or an organization-document failure.',
     'Configured permitted official risk sources; regional policy owner resolves missing source policy.', 'system'),
]


def organization_research(public_links, latest_review=None):
    if (not isinstance(public_links, list) or not public_links
            or any(not isinstance(u, str) for u in public_links)):
        raise ValueError('Public links required')
    if not set(public_links).issubset(LINKS):
        raise ValueError('Unsupported real case links')
    dossier = assess_saved_research()
    return {'status': 'gap_review', 'mode': 'real_public_research',
            'organization_full_name': dossier['organization_display_name'],
            'case_id': dossier['case_id'], 'qualified': False,
            'materials_fetched': False, 'representation_authority_verified': False,
            'message': 'Gap review of configured Lucy public links using saved research. No fresh website read; a link does not prove representation authority.',
            'gap_checklist': [{'field': field, 'what_to_add': what, 'why': why,
                               'where_to_obtain_or_publish': where, 'responsible_party': owner,
                               'condition': 'not_established',
                               'next_check': 'After publication, request a permitted source refresh. New URLs require source-access review; changed text is not automatically verified.'}
                              for field, what, why, where, owner in ITEMS],
            'existing_observations': {'official_identity': dossier['official_identity_observation'],
                                      'published_allocation': dossier['external_form_observation']},
            'latest_runtime_review': ({'status': latest_review['status'], 'memory': deepcopy(latest_review['memory']),
                                       'run_id': latest_review['run_id']}
                                      if latest_review else None),
            'privacy_note': 'Publish only appropriate public information on your own channels. Do not submit private documents, donor details or payment credentials here.',
            'guarantee': 'This checklist does not certify the organization, guarantee qualification or promise donations. No payment or outreach is performed.'}
