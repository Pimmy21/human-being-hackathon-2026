"""Narrow sourced text candidates; no general semantic or medical verification."""
from datetime import datetime
import re
from zoneinfo import ZoneInfo


def analyze_read(result):
    candidates, dates, issues = [], [], []
    for source in result.get('sources', []):
        if source.get('status') != 'read':
            continue
        text = source.get('text', '')
        # The configured HTML container includes related links. Never extract
        # candidates from those links or treat them as the article itself.
        body = re.split(r'Related news', text, maxsplit=1, flags=re.I)[0]
        sid = source['source_id']
        local_day = None
        try:
            stamp = datetime.fromisoformat(source['published_metadata'].replace('Z', '+00:00'))
            if stamp.tzinfo is None:
                raise ValueError
            local_day = stamp.astimezone(ZoneInfo('America/Toronto')).date().isoformat()
            dates.append({'source_id': sid, 'raw_metadata': source['published_metadata'],
                          'ontario_calendar_date': local_day, 'authority': 'page_metadata_only'})
        except (ValueError, TypeError, KeyError):
            issues.append({'source_id': sid, 'issue': 'publication_date_not_established'})
        # Exact narrow statement patterns. Missing matches remain unknown.
        patterns = [
            ('reported_birth', r'Lucy.{0,350}?gave birth.{0,130}?three beautiful kittens[!.]?'),
            ('reported_pregnancy', r'Lucy is only.{0,100}?pregnant.{0,100}?moment[!.]?'),
        ]
        for field, pattern in patterns:
            match = re.search(pattern, body, re.I)
            if match:
                candidates.append({'field': field, 'source_id': sid, 'url': source['url'],
                                   'quote': match.group(), 'start': match.start(), 'end': match.end(),
                                   'source_sha256': source.get('content_sha256'),
                                   'published_ontario_date': local_day,
                                   'authority': 'organization_statement_candidate',
                                   'independently_verified': False})
    dated = [c for c in candidates if c['published_ontario_date']]
    latest = max(dated, key=lambda c: c['published_ontario_date']) if dated else None
    # A partial fetch cannot claim the latest of all configured sources.
    complete = result.get('status') == 'read_complete'
    return {'mode': 'narrow_rule_candidates', 'candidates': candidates,
            'publication_dates': dates, 'issues': issues,
            'latest_retrieved_statement': latest,
            'all_configured_sources_read': complete,
            'current_real_world_state_confirmed': False,
            'funding': {'cost_minor': None, 'raised_minor': None, 'remaining_minor': None,
                        'reason': 'No validated same-case cost/funding/allocation inputs. No amount inferred from prose.'},
            'qualified': False, 'status': 'pending_verification',
            'limitations': ['Exact text matches are candidates, not proof of clinical need or authenticity.',
                            'Latest retrieved statement is not proof that no later public update exists.',
                            'No automatic financial extraction, model call or independent corroboration.',
                            'Unknowns remain unknown; this does not change the synthetic demo case.']}
