import argparse
import html
import json
from pathlib import Path

from .history import history_from_memory
from .memory import HMem, review_with_memory
from .memory_demo import case_for_phase


def main():
    parser = argparse.ArgumentParser(description='Real H-MEM historical-time demonstration with synthetic evidence')
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--workspace', default='history-demo')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    memory = HMem(args.reference, args.state, workspace=args.workspace)
    first = review_with_memory(case_for_phase('first'), memory)
    cutoff = history_from_memory(memory, 'SYN-MAPLE')['system_recorded_at']
    second = review_with_memory(case_for_phase('update'), memory)
    before_update = history_from_memory(memory, 'SYN-MAPLE', cutoff)
    latest = history_from_memory(memory, 'SYN-MAPLE')
    missing = history_from_memory(memory, 'SYN-MAPLE', '2000-01-01T00:00:00Z')
    results = {'before_update': before_update, 'latest_recorded': latest, 'no_record': missing}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'answers.json').write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
    (args.output/'runs.json').write_text(json.dumps([first, second], indent=2)+'\n', encoding='utf-8')
    cards = []
    for name, record in results.items():
        summary = record.get('recorded_result') or {}
        remaining = summary.get('remaining_minor')
        amount = 'Unknown / unavailable' if remaining is None else f'CAD {remaining/100:,.2f}'
        cards.append('<section><h2>'+html.escape(name.replace('_', ' ').title())+'</h2><p>'+html.escape(record['message'])
                     +'</p><p>Known by the system: '+html.escape(record.get('system_recorded_at', 'No record'))
                     +'</p><p><strong>Saved remaining amount: '+amount+'</strong></p><p>Saved status: '
                     +html.escape(summary.get('disposition', 'unavailable'))+'</p><details><summary>Stored evidence and unknowns</summary><pre>'
                     +html.escape(json.dumps(record, indent=2))+'</pre></details></section>')
    page = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Purrpose history</title><style>body{font:16px/1.6 system-ui;background:#f6f5f0;color:#22352d;margin:0}main{max-width:950px;margin:auto;padding:24px}section{background:white;border:1px solid #ccd6cc;border-radius:14px;padding:22px;margin:20px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}.notice{background:#fff0cd;padding:16px}summary{cursor:pointer}</style><main><h1>Purrpose · what did we know then?</h1><p class="notice">Synthetic case evidence, real H-MEM persistence and recorded creation times. Both reviews ran today. Source-review dates 24/25 October are a simulated scenario clock, not the system knowledge timeline. No new model or external-source requests.</p>'+''.join(cards)+'</main></html>'
    (args.output/'index.html').write_text(page, encoding='utf-8')
    print(json.dumps({'before_update_remaining': before_update['recorded_result']['remaining_minor'],
                      'latest_remaining': latest['recorded_result']['remaining_minor'],
                      'missing_record_status': missing['status'], 'new_model_calls': 0}))


if __name__ == '__main__':
    main()
