"""Historical answers use stored reviews and H-MEM creation times, never current facts."""
from copy import deepcopy
from datetime import datetime, timezone


def parse_cutoff(value):
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError
        return parsed.astimezone(timezone.utc)
    except (AttributeError, ValueError, TypeError):
        raise ValueError('Use an ISO timestamp with explicit timezone, for example 2026-10-24T14:00:00-04:00') from None


def historical_answer(entries, case_id, cutoff=None):
    limit = parse_cutoff(cutoff) if cutoff is not None else None
    eligible, missing_times = [], 0
    for entry in entries:
        p = entry.get('payload', {})
        if p.get('case_id') != case_id:
            continue
        try:
            recorded = parse_cutoff(entry['system_recorded_at'])
        except (ValueError, KeyError):
            missing_times += 1
            continue
        if limit is None or recorded <= limit:
            # Source date and fixture review clock never select historical state.
            eligible.append((recorded, int(entry['memory_id'].removeprefix('mem-')), entry))
    if not eligible:
        return {'status': 'history_unavailable', 'case_id': case_id, 'cutoff': cutoff,
                'message': 'No retained review with a known system-recorded time exists at or before this cutoff.',
                'records_with_unknown_system_time': missing_times, 'historical_qualification': None}
    _, _, entry = max(eligible, key=lambda item: item[:2])
    p = entry['payload']
    summary = p.get('review_summary')
    return {'status': 'recorded_review' if summary is not None else 'partial_legacy_record',
            'case_id': case_id, 'cutoff': cutoff, 'memory_id': entry['memory_id'],
            'system_recorded_at': entry['system_recorded_at'],
            'source_review_date': p.get('review_date'), 'scenario_type': p.get('scenario_type'),
            'organization_full_name': p.get('organization'), 'case_name': p.get('case_name'),
            'recorded_result': deepcopy(summary), 'recorded_unknowns': deepcopy(p.get('open_issues', [])),
            'recorded_claims': deepcopy(p.get('claims', {})),
            'source_metadata': deepcopy(p.get('source_metadata', {})),
            'source_refs': deepcopy(p.get('source_refs', [])),
            'message': ('This is the saved result known by the selected time, not a current re-evaluation.'
                        if summary is not None else 'Legacy record lacks a complete saved result; no exact decision was reconstructed.'),
            'source_urls_rechecked_now': False, 'current_qualification_implied': False,
            'records_with_unknown_system_time': missing_times}


def history_from_memory(memory, case_id, cutoff=None):
    # Parse before touching memory: invalid user input does not cause a read.
    if cutoff is not None:
        parse_cutoff(cutoff)
    recalled = memory.call('recall', case_id)
    return historical_answer(recalled['entries'], case_id, cutoff)


def main():
    import argparse
    import json
    from pathlib import Path
    from .memory import HMem
    parser = argparse.ArgumentParser(description='Read a retained case review; never reconstruct it using current facts')
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--case-id', required=True)
    parser.add_argument('--cutoff', help='ISO timestamp including timezone; omit for latest recorded review')
    args = parser.parse_args()
    result = history_from_memory(HMem(args.reference, args.state, workspace=args.workspace), args.case_id, args.cutoff)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
