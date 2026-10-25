import argparse
import json
from pathlib import Path

from .__main__ import load_scenario
from .journeys import public_record
from .journey_demo import render_journeys
from .memory import HMem
from .replay import review_replay


def main():
    p = argparse.ArgumentParser(description='Recorded NVIDIA candidate -> code validation -> case gates -> supporter result')
    p.add_argument('--output', type=Path, default=Path('purrpose/artifacts/replay'))
    p.add_argument('--reference', type=Path)
    p.add_argument('--state', type=Path)
    p.add_argument('--workspace', default='replay-demo')
    args = p.parse_args()
    if bool(args.reference) != bool(args.state):
        p.error('Supply both reference and state for real H-MEM')
    memory = HMem(args.reference, args.state, workspace=args.workspace) if args.reference else None
    bundle = json.loads((Path(__file__).parent/'fixtures/nvidia-capture.json').read_text(encoding='utf-8'))
    case, result = review_replay(load_scenario('complete'), bundle['capture'], bundle['current_passage'], memory)
    row = public_record(case, result)
    outputs = {'supporter': {'status': 'results', 'qualified': [row] if row['qualified'] else [],
                            'pending': [] if row['qualified'] else [row], 'no_current_gap': [],
                            'expansion_question': None,
                            'message': 'Recorded NVIDIA cost revalidated and used in synthetic case checks. No new API call.'},
               'organization': {'message': 'This report demonstrates case ingestion, not a new organization submission.',
                                'gap_checklist': [], 'privacy_note': 'Evidence and case remain synthetic.',
                                'guarantee': 'No real rescue or veterinary document has been authenticated.'}}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'run.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    (args.output/'supporter.json').write_text(json.dumps(row, indent=2)+'\n', encoding='utf-8')
    page = render_journeys(outputs, bool(memory))
    page = page.replace('<h1>Purrpose · two user journeys</h1>',
                        '<h1>Purrpose · validated extraction enters the case workflow</h1><p><strong>NVIDIA replay, not a new live inference.</strong> Original request: 281 tokens. New inference calls: zero. Core gates and H-MEM below run now.</p>')
    (args.output/'index.html').write_text(page, encoding='utf-8')
    print(json.dumps({'qualified': result['qualified'], 'scenario_type': result['scenario_type'],
                      'remaining_minor': result['remaining_minor'], 'replay': result['extraction_replay'],
                      'memory_enabled': bool(memory)}))


if __name__ == '__main__':
    main()
