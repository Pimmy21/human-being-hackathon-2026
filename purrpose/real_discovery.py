"""One curated real lead, not internet search or verified case matching."""
from .research_case import assess_saved_research


def discover_real(*, city=None, region_wide=False, allow_expansion=False):
    if city is not None and (not isinstance(city,str) or not city.strip()):
        raise ValueError('City required')
    if type(region_wide) is not bool or type(allow_expansion) is not bool:
        raise ValueError('Explicit boolean preferences required')
    if city is None and not region_wide:
        return {'status':'needs_preference', 'collection':'real',
                'question':'Choose a treatment city or anywhere in Ontario.'}
    if city is not None and not allow_expansion:
        return {'status':'no_city_match', 'collection':'real', 'qualified':[], 'pending':[],
                'expanded':False, 'question':'No real lead has a confirmed treatment-city match. Include Ontario-context leads with unverified treatment location?'}
    dossier=assess_saved_research()
    record={'case_id':dossier['case_id'], 'organization_full_name':dossier['organization_display_name'],
            'case_name':dossier['case_name'], 'case_city':None, 'scenario_type':'real_public_observations',
            'qualified':False, 'remaining_minor':None, 'currency':'CAD', 'external_donation_url':None,
            'review_date':dossier['source_observed_on'],
            'funding_notice':'Saved research: no validated case cost or raised total; remaining amount unknown.',
            'unpassed_requirements':[g['explanation'] for g in dossier['gates']],
            'evidence':[{'publisher':s['publisher'], 'source_date':s['published_on'], 'reference':s['url'],
                         'observation_date':s['observed_on'], 'authority':'organization_statement'} for s in dossier['sources']],
            'limitations':dossier['limitations']}
    return {'status':'results', 'collection':'real', 'qualified':[], 'pending':[record], 'no_current_gap':[],
            'region':'Ontario', 'expanded':city is not None,
            'message':'No qualified real recommendation. One curated Ontario-context lead is available for further checks; its treatment location is unverified.',
            'coverage':'One saved curated lead; no new web search or automatic source refresh.'}
