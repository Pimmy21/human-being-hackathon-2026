"""Explicit single-request integration proof over a synthetic cost passage."""
import argparse
from decimal import Decimal
import html
import json
import os
from pathlib import Path
import re

from .extraction import Budget, ExtractionError, Limits, extract


def validate_cost(candidate, passage):
    """Narrow code rule for this labelled cost format, not general authentication."""
    if candidate['field'] != 'cost_minor':
        return None
    match = re.search(r'Treatment estimate: CAD ([0-9,]+\.[0-9]{2})\.', candidate['quote'])
    if not match:
        return None
    expected = int(Decimal(match[1].replace(',', ''))*100)
    return expected if candidate['value'] == expected and candidate['quote'] in passage['text'] else None


def main():
    p = argparse.ArgumentParser(description='One authorized NVIDIA request, synthetic data only, no retries')
    p.add_argument('--env-file', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--allow-one-live-request', action='store_true', required=True)
    p.add_argument('--disable-thinking', action='store_true')
    args = p.parse_args()
    local = {}
    if args.env_file and args.env_file.is_file():
        for line in args.env_file.read_text(encoding='utf-8-sig').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                if k.strip() in ('NVIDIA_API_KEY', 'NVIDIA_MODEL'):
                    local[k.strip()] = v.strip().strip('"\'')
    key = os.environ.get('NVIDIA_API_KEY') or local.get('NVIDIA_API_KEY')
    model = os.environ.get('NVIDIA_MODEL') or local.get('NVIDIA_MODEL')
    passage = {'source_id': 'SYN-MED-COST', 'case_id': 'SYN-MAPLE', 'passage_id': 'cost-line',
               'source_version': 'synthetic-v1',
               'text': 'Synthetic Maple case. Treatment estimate: CAD 2,000.00.'}
    budget = Budget(Limits(max_calls=1, token_cap=4000, reservation_tokens=4000,
                           input_chars=4000, output_tokens=512, timeout_seconds=30))
    result = {'scenario_type': 'synthetic', 'attempt_limit': 1, 'automatic_retries': 0,
              'maximum_output_tokens': 512, 'timeout_seconds': 30,
              'case_qualified': False, 'real_medical_authentication': False}
    try:
        extracted = extract([passage], budget=budget, key=key, model=model, disable_thinking=args.disable_thinking)
        costs = {cost for c in extracted['candidates'] if (cost := validate_cost(c, passage)) is not None}
        cost = next(iter(costs)) if len(costs) == 1 else None
        result.update({'status': 'validated_cost_used' if cost is not None else 'candidate_held',
                       'extraction': extracted, 'validated_cost_minor': cost,
                       'fixture_raised_minor': 70000, 'fixture_separate_grant_minor': 30000,
                       'illustrative_remaining_minor': max(0, cost-70000-30000) if cost is not None else None,
                       'consumption': 'Code-validated model cost consumed in synthetic arithmetic preview; not a qualified rescue'})
    except ExtractionError as exc:
        result.update({'status': 'failed', 'error_category': exc.category})
    result['budget'] = budget.status()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    page = '<!doctype html><meta charset="utf-8"><title>Purrpose NVIDIA check</title><main style="max-width:900px;margin:32px auto;font:16px/1.6 system-ui"><h1>Purrpose · NVIDIA integration check</h1><p>Synthetic material only. One request at most; no retries. A validated cost can support an arithmetic preview, not real medical authentication or case qualification.</p><pre style="white-space:pre-wrap;overflow-wrap:anywhere">'+html.escape(json.dumps(result, indent=2))+'</pre></main>'
    (args.output/'index.html').write_text(page, encoding='utf-8')
    print(json.dumps({'status': result['status'], 'error_category': result.get('error_category'),
                      'remaining_minor': result.get('illustrative_remaining_minor'), 'budget': result['budget']}))


if __name__ == '__main__':
    main()
