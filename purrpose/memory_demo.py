"""Run first/update in separate Python processes against real local H-MEM."""
import argparse
import json
from pathlib import Path

from .__main__ import load_scenario, report
from .memory import HMem, review_with_memory


def case_for_phase(phase):
    case = load_scenario('exhausted')
    if phase == 'update':
        case['review_date'] = '2026-10-25'
        case['sources']['funding']['date'] = '2026-10-25'
        case['sources']['funding']['facts']['grant_inclusion'] = 'separate'
    return case


def main():
    p = argparse.ArgumentParser(description='Synthetic case evidence with actual local Meterless memory')
    p.add_argument('--reference', type=Path, required=True, help='Official H-MEM reference/src/index.ts')
    p.add_argument('--state', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--workspace', default='demo')
    p.add_argument('--phase', choices=['first', 'update'], required=True)
    args = p.parse_args()
    memory = HMem(args.reference, args.state, workspace=args.workspace)
    result = review_with_memory(case_for_phase(args.phase), memory)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / f'{args.phase}.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    results = {name: json.loads((args.output / f'{name}.json').read_text())
               for name in ('first', 'update') if (args.output / f'{name}.json').exists()}
    page = report(results).replace(
        'No real rescue, live source, NVIDIA, Nightshift, Zetaris or H-MEM integration is claimed.',
        'Real local Meterless H-MEM is connected. No real rescue, live source, NVIDIA, Nightshift or Zetaris inference is claimed.')
    page = page.replace('The fixture clock is 24 October 2026.',
                        'Fixture review dates: first 24 October 2026; update 25 October 2026 (simulated next day).')
    page = page.replace('Compare three cases below. Only unresolved grant inclusion triggers dispute resolution.',
                        'Compare saved first review with the new review after application restart. Open the traces to see memory reuse.')
    explanation = '<section><h2>Actual H-MEM use</h2>'
    for name, record in results.items():
        m = record['memory']
        explanation += (f'<p>{name}: recalled {m["recalled_memory_id"] or "none"}; '
                        f'reused {len(m["reused_fields"])} validated fields; '
                        f'saved {m["saved_memory_id"]}. Open questions recalled: {len(m["previous_open_issues"])}.</p>')
    page = page.replace('</main>', explanation+'</section></main>')
    (args.output / 'index.html').write_text(page, encoding='utf-8')
    print(json.dumps({'phase': args.phase, 'disposition': result['disposition'],
                      'remaining_minor': result['remaining_minor'], 'memory': result['memory'],
                      'source_reads': result['usage']['source_reads']}, indent=2))


if __name__ == '__main__':
    main()
