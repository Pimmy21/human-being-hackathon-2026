"""User-facing contracts over the synthetic review engine; no web fetching."""
from .core import Review


GAP_HELP = {
    'grant_inclusion': ('Clarify whether the grant is already included in the raised total.',
                        'The remainder cannot be calculated without avoiding double counting.',
                        'Publish a dated same-case funding statement identifying grant inclusion.'),
    'medical_linked': ('Provide public medical material linked to this cat or group.',
                       'A general rescue story cannot establish this medical request.',
                       'A corresponding issuer statement or appropriately redacted estimate.'),
    'cost_minor': ('Provide a dated case-specific treatment cost.', 'A gap requires a supported cost.',
                   'A corresponding public estimate or issuer statement.'),
    'raised_minor': ('Provide a dated same-case funding total.', 'Unknown funding is not zero.',
                     'The organization public case funding update.'),
}
GATE_HELP = {
    'identity_geography': 'Applicable official identity, active status and case location need verification.',
    'medical_need': 'Corresponding current medical material must be linked to this case.',
    'funding_evidence': 'Current compatible cost and funding records must support the calculation.',
    'positive_disclosed_remainder': 'A positive disclosed funding gap must be established; fully funded is not misconduct.',
    'donation_channel': 'An external donation channel must be linked to the checked organization.',
    'organization_risk': 'Applicable risk checks must be complete and relevant holds resolved under policy.',
}


def public_record(case, result):
    """Default view excludes internal traces; returns necessary uncertainty."""
    evidence = []
    for field, claim in result['claims'].items():
        source = case['sources'][claim['source_id']]
        evidence.append({'field': field, 'value': claim['value'], 'source_id': claim['source_id'],
                         'reference': f'synthetic://{case["case_id"]}/{claim["source_id"]}',
                         'publisher': source['publisher'], 'source_date': source['date'],
                         'location': claim['location'], 'scenario_type': 'synthetic',
                         'extraction_provenance': claim.get('extraction_provenance')})
    reasons = [GATE_HELP[g] for g, passed in result['gates'].items() if not passed]
    return {'organization_full_name': result['organization'],
            'registration_category': 'Synthetic registered rescue organization; no real status verified',
            'case_id': result['case_id'], 'case_name': result['case_name'], 'case_city': result['city'],
            'scenario_type': 'synthetic', 'qualified': result['qualified'],
            'remaining_minor': result['remaining_minor'], 'currency': result['currency'],
            'funding_notice': result['funding_notice'], 'review_date': result['review_date'],
            'evidence': evidence, 'unknowns': result['gaps'], 'unpassed_requirements': reasons,
            'risk_hold': result['risk_hold'], 'external_donation_url': None,
            'limitations': ['This is a fictional case, not a donation recommendation.',
                            'No real registration, veterinary issuer or payment channel has been checked.']}


class Journeys:
    def __init__(self, cases, memory=None):
        self.cases = cases
        self.memory = memory
        self.runs = {}

    def review(self, case):
        if self.memory:
            from .memory import review_with_memory
            result = review_with_memory(case, self.memory)
        else:
            result = Review(case).run()
        self.runs[result['run_id']] = result
        return result

    def supporter(self, *, city=None, region_wide=False, allow_expansion=False):
        if city is None and not region_wide:
            return {'status': 'needs_preference', 'question': 'Do you prefer a city in Ontario, or anywhere in Ontario?',
                    'required_personal_information': []}
        if city is not None and (not isinstance(city, str) or not city.strip()):
            raise ValueError('City must be a nonempty name, or explicitly choose region-wide')
        matches = [c for c in self.cases if city is None or (c.get('city') or '').casefold() == city.strip().casefold()]
        expanded = False
        if not matches and city is not None:
            if not allow_expansion:
                return {'status': 'no_city_match', 'qualified': [], 'pending': [],
                        'question': 'No case matches that treatment city. Search other supported Ontario cities?',
                        'expanded': False}
            matches, expanded = self.cases, True
        records = [public_record(c, self.review(c)) for c in matches]
        if city is not None and allow_expansion and not any(r['qualified'] for r in records):
            extra = [c for c in self.cases if c not in matches]
            records.extend(public_record(c, self.review(c)) for c in extra)
            expanded = expanded or bool(extra)
        key = lambda r: ((r['case_city'] is None), (r['case_city'] or '').casefold(),
                         r['organization_full_name'].casefold(), r['case_name'].casefold(), r['case_id'])
        qualified = sorted([r for r in records if r['qualified']], key=key)
        # A resolved zero gap is distinct from incomplete verification.
        no_gap = sorted([r for r in records if not r['qualified'] and r['remaining_minor'] == 0], key=key)
        pending = sorted([r for r in records if not r['qualified'] and r['remaining_minor'] != 0], key=key)
        return {'status': 'results', 'region': 'Ontario', 'expanded': expanded,
                'qualified': qualified, 'pending': pending, 'no_current_gap': no_gap,
                'message': 'Synthetic results only.' if qualified else 'No case meets all requirements in this collection.',
                'expansion_question': ('No qualifying case in that city. Search other supported Ontario cities?'
                                       if city is not None and not qualified and not allow_expansion else None),
                'coverage': 'Small synthetic curated collection; not an internet search.'}

    def organization(self, *, public_links):
        if not isinstance(public_links, list) or not public_links or any(not isinstance(x, str) for x in public_links):
            raise ValueError('Provide public links, not uploaded files')
        cases = [c for c in self.cases if set(public_links).intersection(c.get('public_links', []))]
        if len(cases) != 1 or not set(public_links).issubset(cases[0].get('public_links', [])):
            return {'status': 'unsupported_links', 'materials_fetched': False,
                    'message': 'This offline demo reads only explicitly mapped fixture pages. No supplied URL was fetched.',
                    'next_action': 'Use the displayed synthetic fixture link; real public-source retrieval remains unconnected.'}
        case = cases[0]
        result = self.review(case)
        record = public_record(case, result)
        gaps = []
        for gap in result['gaps']:
            what, why, where = GAP_HELP.get(gap['field'], (
                'Provide checkable public information for '+gap['field']+'.',
                'The corresponding required evidence check is incomplete.',
                gap['suggested_channel']))
            gaps.append({'field': gap['field'], 'condition': gap['reason'], 'what_to_add': what,
                         'why': why, 'where_to_obtain_or_publish': where,
                         'next_check': 'Re-read the current permitted source and rerun affected checks.'})
        for gate, passed in result['gates'].items():
            if not passed:
                gaps.append({'field': gate, 'condition': 'not_passed', 'what_to_add': GATE_HELP[gate],
                             'why': 'This requirement has not passed; adding unrelated materials cannot replace it.',
                             'where_to_obtain_or_publish': 'Applicable official channel or relevant public issuer/organization statement.',
                             'next_check': 'Re-evaluate this requirement after checkable public information changes.'})
        return {'status': 'gap_review', 'organization_full_name': result['organization'],
                'case': record, 'gap_checklist': gaps, 'materials_fetched': False,
                'fixture_pages_read': result['usage']['source_reads'],
                'representation_authority_verified': False,
                'message': 'Mapped synthetic public-page fixture reviewed. Anyone may supply a link; that does not prove representation authority.',
                'privacy_note': 'Do not publish donor details, payment credentials or sensitive unredacted medical data.',
                'guarantee': 'Following suggestions does not guarantee qualification or donations.'}
