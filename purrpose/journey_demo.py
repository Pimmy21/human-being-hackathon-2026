import argparse
import html
import json
from pathlib import Path

from .__main__ import load_scenario
from .journeys import Journeys
from .memory import HMem

FIXTURE_LINK = 'https://example.invalid/purrpose/maple'


def render_journeys(outputs, memory_enabled):
    esc = lambda x: html.escape(str(x))
    supporter = outputs['supporter']
    cards = ['<section><h2>I want to help a cat</h2>']
    if supporter['status'] != 'results':
        cards.append('<p>'+esc(supporter.get('question', supporter['status']))+'</p>')
    else:
        cards.append('<p>'+esc(supporter['message'])+'</p>')
        for group, title in [('qualified', 'Meets the synthetic checks'), ('pending', 'Still needs verification'),
                             ('no_current_gap', 'No current disclosed funding gap')]:
            for row in supporter[group]:
                amount = 'Not yet known' if row['remaining_minor'] is None else f"CAD {row['remaining_minor']/100:,.2f}"
                cards.append('<article><h3>'+esc(row['organization_full_name'])+'</h3><p>'+esc(title)
                             +' · '+esc(row['case_name'])+' · '+esc(row['case_city'] or 'City unknown')+'</p>'
                             +'<p><strong>Remaining need: '+amount+'</strong></p><p>'+esc(row['funding_notice'])+'</p>')
                if row['unpassed_requirements']:
                    cards.append('<h4>What is not yet established</h4><ul>'+''.join('<li>'+esc(x)+'</li>'
                                 for x in row['unpassed_requirements'])+'</ul>')
                cards.append('<details><summary>Evidence used — synthetic sources</summary><ul>'+''.join(
                    '<li>'+esc(e['publisher'])+' · '+esc(e['source_date'])+' · '+esc(e['field'])+': '
                    +esc(e['value'])+'<br><small>'+esc(e['reference'])+' · '+esc(e['location'])+'</small></li>'
                    if not e.get('extraction_provenance') else
                    '<li>'+esc(e['field'])+': '+esc(e['value'])+'<br><small>'+esc(e['reference'])
                    +'<br>Extraction route: '+esc(e['extraction_provenance']['route'])
                    +'<br>Source quote: '+esc(e['extraction_provenance']['quote'])+'</small></li>'
                    for e in row['evidence'])+'</ul></details><p>No donation link: this case is fictional.</p></article>')
        if supporter['expansion_question']:
            cards.append('<p>'+esc(supporter['expansion_question'])+'</p>')
    cards.append('</section><section><h2>Check our public information</h2>')
    organization = outputs['organization']
    cards.append('<p>'+esc(organization['message'])+'</p>')
    for gap in organization.get('gap_checklist', []):
        cards.append('<article><h3>'+esc(gap['what_to_add'])+'</h3><p><strong>Why:</strong> '+esc(gap['why'])
                     +'</p><p><strong>Where:</strong> '+esc(gap['where_to_obtain_or_publish'])
                     +'</p><p><strong>Next check:</strong> '+esc(gap['next_check'])+'</p></article>')
    cards.append('<p>'+esc(organization.get('privacy_note', ''))+'</p><p>'+esc(organization.get('guarantee', ''))+'</p></section>')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Purrpose user journeys</title><style>body{font:16px/1.6 system-ui;background:#f6f5f0;color:#22352d;margin:0}main{max-width:950px;margin:auto;padding:24px}section{background:white;border:1px solid #ccd6cc;border-radius:14px;padding:22px;margin:20px 0}article{border-top:1px solid #ddd;padding:12px 0}small{overflow-wrap:anywhere}summary{cursor:pointer;font-weight:600}.notice{background:#fff0cd;padding:16px}h1,h2,h3{line-height:1.3}</style><main>
<h1>Purrpose · two user journeys</h1><p class="notice">Executed backend output over synthetic case evidence. No supplied URL was fetched. No payments or private uploads. This is a saved report; run the command again to change inputs. Scenario date: 24 October 2026.</p>'''
    return page+'<p>H-MEM: '+('real local reference enabled' if memory_enabled else 'not enabled for this run')+'</p>'+''.join(cards)+'</main></html>'


def main():
    parser = argparse.ArgumentParser(description='Two synthetic Purrpose user journeys; optional real local H-MEM')
    parser.add_argument('--scenario', choices=['complete', 'repair', 'exhausted'], default='exhausted')
    parser.add_argument('--city', default='Ottawa')
    parser.add_argument('--reference', type=Path)
    parser.add_argument('--state', type=Path)
    parser.add_argument('--workspace', default='journeys')
    parser.add_argument('--output', type=Path, default=Path('purrpose/artifacts/journeys'))
    args = parser.parse_args()
    if bool(args.reference) != bool(args.state):
        parser.error('Supply both --reference and --state to enable real H-MEM')
    case = load_scenario(args.scenario)
    case['public_links'] = [FIXTURE_LINK]
    memory = HMem(args.reference, args.state, workspace=args.workspace) if args.reference else None
    app = Journeys([case], memory)
    outputs = {'supporter': app.supporter(city=args.city),
               'organization': app.organization(public_links=[FIXTURE_LINK])}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'results.json').write_text(json.dumps(outputs, indent=2)+'\n', encoding='utf-8')
    (args.output/'developer-runs.json').write_text(json.dumps(app.runs, indent=2)+'\n', encoding='utf-8')
    page = render_journeys(outputs, bool(memory))
    (args.output/'index.html').write_text(page, encoding='utf-8')
    print(f'Generated supporter and organization outputs: {(args.output/"index.html").resolve()}')


if __name__ == '__main__':
    main()
