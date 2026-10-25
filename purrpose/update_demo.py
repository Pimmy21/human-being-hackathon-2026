import argparse
from copy import deepcopy
import html
import json
from pathlib import Path

from .__main__ import load_scenario
from .memory import HMem
from .updates import UpdateService

LINK = 'https://example.invalid/purrpose/maple/funding'


def main():
    p = argparse.ArgumentParser(description='Screen and review synthetic public updates with optional real H-MEM')
    p.add_argument('--reference', type=Path)
    p.add_argument('--state', type=Path)
    p.add_argument('--workspace', default='update-demo')
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if bool(args.reference) != bool(args.state):
        p.error('Supply both reference and state')
    memory = HMem(args.reference, args.state, workspace=args.workspace) if args.reference else None
    case = load_scenario('complete')
    source = deepcopy(case['sources']['funding'])
    source['facts']['raised_minor'] = 120000
    service = UpdateService(case, lambda url: source, {LINK: 'funding'}, memory)
    first = service.review()
    lead = service.notify('https://unknown.example/accusation', request_id='untrusted-notice')
    changed = service.notify(LINK, request_id='observed-funding-change')
    duplicate = service.notify(LINK, request_id='observed-funding-change')
    def unavailable(url):
        raise TimeoutError('simulated source outage')
    service.reader = unavailable
    failed_refresh = service.notify(LINK, request_id='latest-request', explicit_refresh=True)
    output = {'baseline': first, 'unapproved_notice': lead, 'observed_update': changed,
              'duplicate_request': duplicate, 'failed_explicit_refresh': failed_refresh}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'runs.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    summaries = [('Before update', 'Disclosed gap CAD 1,000; synthetic checks complete.'),
                 ('Unapproved notice', 'Unknown link is a lead only; it cannot directly remove qualification.'),
                 ('Changed public-page fixture', 'Raised total changes to CAD 1,200. Rechecked gap: CAD 500. Unchanged checks may be reused through H-MEM.'),
                 ('Duplicate request', 'Same task result returned, with no repeated source read.'),
                 ('Explicit latest request fails', 'Required source cannot be read. Result stays pending; no silent old-result fallback.')]
    page = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Purrpose public updates</title><style>body{font:16px/1.6 system-ui;background:#f6f5f0;color:#22352d;margin:0}main{max-width:950px;margin:auto;padding:24px}section{background:white;padding:22px;border:1px solid #ccd6cc;border-radius:14px;margin:20px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}.notice{background:#fff0cd;padding:16px}summary{cursor:pointer}</style><main><h1>Purrpose · public information changes</h1><p class="notice">Executed fixture update handling. No URL was fetched over the network. Case and public-page contents are synthetic. H-MEM '+('is real and enabled.' if memory else 'is not enabled.')+' No new model calls.</p>'
    for (title, description), record in zip(summaries, output.values()):
        page += '<section><h2>'+html.escape(title)+'</h2><p>'+html.escape(description)+'</p><details><summary>Actual execution record</summary><pre>'+html.escape(json.dumps(record, indent=2))+'</pre></details></section>'
    (args.output/'index.html').write_text(page+'</main></html>', encoding='utf-8')
    print(json.dumps({'baseline_gap': first['remaining_minor'], 'updated_gap': changed['review']['remaining_minor'],
                      'duplicate_is_replay': duplicate['idempotent_replay'],
                      'failed_refresh_qualified': failed_refresh['review']['qualified'], 'new_model_calls': 0}))


if __name__ == '__main__':
    main()
