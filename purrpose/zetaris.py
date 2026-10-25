"""Read-only JDBC identity probe; fixed queries, explicit historical limits."""
import argparse
from datetime import datetime
import importlib.util
import html
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys

DATABASE = 'DONATION_FEASIBILITY_20261022'
IDENTITY_SQL = ('SELECT fact.BN, fact.`Legal Name`, fact.City, fact.Province '
                'FROM DONATION_FEASIBILITY_20261022.tcr_identity '
                'LATERAL VIEW explode(result.records) AS fact')
EXPECTED_BN = '720884691RR0001'
SOURCE_URL = 'https://open.canada.ca/data/en/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8'
DRIVER = 'com.zetaris.lightning.jdbc.LightningDriver'
NAMES = ('ZETARIS_JDBC_URL', 'ZETARIS_USERNAME', 'ZETARIS_PASSWORD', 'ZETARIS_JDBC_JAR')


def read_config(env_file):
    values = {}
    if Path(env_file).is_file():
        for line in Path(env_file).read_text(encoding='utf-8-sig').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                if k.strip() in NAMES:
                    values[k.strip()] = v.strip().strip('"\'')
    return {k: os.environ.get(k) or values.get(k, '') for k in NAMES}


def remote_ssl(url):
    match = re.search(r'(?:@|//)([^/:;]+):(\d+)', url)
    return bool(match and match[1].lower() not in ('localhost', '127.0.0.1', '::1')
                and re.search(r'(?:[;?&])ssl=true(?:[;&]|$)', url, re.I)
                and not re.search(r'(?:ssl|usessl)=false', url, re.I))


def preflight(config, jvm):
    checks = {k+'_present': bool(config.get(k)) for k in NAMES}
    checks.update(driver_file_exists=bool(config.get('ZETARIS_JDBC_JAR')) and Path(config['ZETARIS_JDBC_JAR']).is_file(),
                  configured_jvm_exists=Path(jvm).is_file(),
                  remote_ssl_endpoint=remote_ssl(config.get('ZETARIS_JDBC_URL', '')),
                  jpype_available=importlib.util.find_spec('jpype') is not None,
                  jaydebeapi_available=importlib.util.find_spec('jaydebeapi') is not None)
    return {'stage': 'local_preflight', 'checks': checks, 'ready': all(checks.values()),
            'protocol': 'JDBC', 'rest_api_key_required': False,
            'network_queries_executed': 0}


def normalize_identity(rows):
    valid = [r for r in rows if isinstance(r, (list, tuple)) and len(r) == 4
             and str(r[0]) == EXPECTED_BN and all(isinstance(v, str) and v.strip() for v in r)]
    if len(valid) != 1:
        return {'status': 'incomplete', 'reason': 'historical_identity_not_uniquely_matched',
                'current_registration_verified': False, 'case_qualified': False}
    row = valid[0]
    return {'status': 'historical_identity_matched', 'organization_number': row[0],
            'organization_full_name': row[1], 'reported_city': row[2], 'reported_province': row[3],
            'source': SOURCE_URL, 'reporting_year': 2024,
            'year_basis': 'Configured table was created for the 2024 public returns resource; not current status',
            'current_registration_verified': False, 'current_risk_checks_complete': False,
            'medical_need_verified': False, 'case_qualified': False,
            'case_city_inferred_from_headquarters': False}


def error_category(exc):
    message = str(exc).lower()  # Never returned raw.
    if '504' in message or 'gateway timeout' in message:
        return 'upstream_source_504'
    if '401' in message or 'unauthorized' in message or 'authentication' in message:
        return 'authentication_failed'
    if '403' in message or 'permission' in message or 'access denied' in message:
        return 'permission_denied'
    if 'timeout' in message or 'timed out' in message:
        return 'connection_or_query_timeout'
    return 'jdbc_or_source_error'


def supporter_identity_view(result):
    """Useful live lookup output, explicitly separate from synthetic cat cases."""
    identity = result.get('identity', {})
    if identity.get('status') == 'historical_identity_matched':
        return {'status': 'historical_information_only',
                'organization_full_name': identity['organization_full_name'],
                'organization_number': identity['organization_number'],
                'reported_location': identity['reported_city']+', '+identity['reported_province'],
                'reporting_year': identity['reporting_year'], 'source': identity['source'],
                'message': 'A matching historical filing was read through Zetaris. It does not establish current registration or a current rescue need.',
                'next_checks': ['Current applicable official registration/status',
                                'Case-specific medical and current funding evidence',
                                'Applicable current risk checks and donation-channel ownership'],
                'qualified_recommendation': False}
    return {'status': 'lookup_incomplete', 'message': 'Current lookup could not establish usable identity information.',
            'failed_stage': result.get('failed_stage', 'identity_normalization'),
            'error_category': result.get('error_category', identity.get('reason', 'not_completed')),
            'source_failure_is_fraud': False, 'qualified_recommendation': False,
            'next_action': 'Inspect the failed stage; do not replace it with a clean registry result.'}


def render_identity_report(result):
    esc = lambda value: html.escape(str(value))
    view = result.get('supporter_identity_view') or supporter_identity_view(result)
    text = '<h1>Purrpose · real Zetaris identity lookup</h1>'
    text += '<p class="notice">Real public structured-data lookup. No synthetic cat case is attributed to this organization. No payments or recommendation approval.</p>'
    text += '<section><h2>'+esc(view['status'].replace('_', ' ').title())+'</h2><p>'+esc(view['message'])+'</p>'
    if view['status'] == 'historical_information_only':
        text += '<h3>'+esc(view['organization_full_name'])+'</h3><p>Organization number: '+esc(view['organization_number'])+'</p>'
        text += '<p>Reported location: '+esc(view['reported_location'])+'</p><p>Reporting year: '+esc(view['reporting_year'])+'</p>'
        text += '<a href="'+SOURCE_URL+'">Government dataset source</a><h3>Still needs checking</h3><ul>'
        text += ''.join('<li>'+esc(x)+'</li>' for x in view['next_checks'])+'</ul>'
    else:
        text += '<p>Stage: '+esc(view['failed_stage'])+' · '+esc(view['error_category'])+'</p>'
    text += '</section><section><h2>Technical execution</h2><p>Observed at: '+esc(result.get('observed_at', 'not recorded'))+'</p>'
    text += '<p>Local prerequisites are distinct from live connection/source results. No automatic retry.</p><ul>'
    text += ''.join('<li>'+esc(s['stage'])+': '+esc(s['status'])+'</li>' for s in result.get('steps', []))+'</ul>'
    text += '<p>This report shows the recorded run only. Earlier attempts and limitations are documented separately in the deployment verification notes.</p></section>'
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Purrpose Zetaris lookup</title><style>body{font:16px/1.6 system-ui;background:#f6f5f0;color:#22352d;margin:0}main{max-width:900px;padding:24px;margin:auto}section{background:white;padding:24px;margin:20px 0;border:1px solid #cbd6cc;border-radius:14px}.notice{background:#fff0cd;padding:16px}h1,h2{line-height:1.3}a{color:#215b48}</style><main>'+text+'</main></html>'


def worker(config, jvm):
    steps, connection = [], None
    stage = 'remote_tcp'
    def progress(state):
        print('PURRPOSE_PROGRESS:'+json.dumps({'stage': stage, 'status': state}), flush=True)
    try:
        progress('started')
        target = re.search(r'(?:@|//)([^/:;]+):(\d+)', config['ZETARIS_JDBC_URL'])
        with socket.create_connection((target[1], int(target[2])), timeout=5):
            pass
        progress('completed')
        stage = 'jvm_start'
        progress('started')
        import jpype
        import jaydebeapi
        if not jpype.isJVMStarted():
            jpype.startJVM(str(Path(jvm).resolve()), classpath=[config['ZETARIS_JDBC_JAR']], convertStrings=True)
        progress('completed')
        stage = 'jdbc_connect'
        progress('started')
        connection = jaydebeapi.connect(DRIVER, config['ZETARIS_JDBC_URL'],
                                        [config['ZETARIS_USERNAME'], config['ZETARIS_PASSWORD']],
                                        config['ZETARIS_JDBC_JAR'])
        progress('completed')
        for stage, sql in [('connection_select', 'SELECT 1'), ('database_discovery', 'SHOW LIGHTNING DATABASES'),
                           ('source_query', IDENTITY_SQL)]:
            progress('started')
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
                rows = [list(r) for r in cursor.fetchmany(100 if stage == 'database_discovery' else 3)]
            finally:
                cursor.close()
            if stage == 'connection_select' and (not rows or str(rows[0][0]) != '1'):
                raise ValueError('connection check failed')
            if stage == 'database_discovery' and not any(str(r[0]) == DATABASE for r in rows):
                return {'status': 'incomplete', 'failed_stage': stage, 'error_category': 'approved_database_not_available',
                        'steps': steps, 'case_qualified': False}
            steps.append({'stage': stage, 'status': 'completed', 'statement_type': 'read_only',
                          'row_count_observed': len(rows)})
            progress('completed')
        return {'status': 'completed', 'steps': steps, 'identity': normalize_identity(rows),
                'source_rows': rows, 'case_qualified': False}
    except Exception as exc:
        return {'status': 'incomplete', 'failed_stage': stage, 'error_category': error_category(exc),
                'steps': steps, 'case_qualified': False, 'source_failure_is_fraud': False}
    finally:
        if connection:
            stage = 'jdbc_close'
            progress('started')
            try:
                connection.close()
                progress('completed')
            except Exception:
                progress('failed')


def main():
    p = argparse.ArgumentParser(description='Configured historical identity query, no writes and no fallback')
    p.add_argument('--env-file', type=Path, required=True)
    p.add_argument('--jvm', type=Path, required=True)
    p.add_argument('--output', type=Path)
    p.add_argument('--live', action='store_true')
    p.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = p.parse_args()
    config = read_config(args.env_file)
    check = preflight(config, args.jvm)
    if args.worker:
        result = worker(config, args.jvm) if check['ready'] else check
        print('PURRPOSE_RESULT:'+json.dumps(result, default=str), flush=True)
        return
    result = check
    if args.live and check['ready']:
        command = [sys.executable, '-m', 'purrpose.zetaris', '--worker',
                   '--env-file', str(args.env_file.resolve()), '--jvm', str(args.jvm.resolve())]
        try:
            child = subprocess.run(command, text=True, encoding='utf-8', capture_output=True, timeout=45)
            lines = [s for s in child.stdout.splitlines() if s.startswith('PURRPOSE_RESULT:')]
            result = json.loads(lines[-1].split(':', 1)[1]) if lines else {
                'status': 'incomplete', 'failed_stage': 'jdbc_worker', 'error_category': 'worker_failed', 'case_qualified': False}
        except subprocess.TimeoutExpired as exc:
            partial = exc.stdout or ''
            if isinstance(partial, bytes):
                partial = partial.decode('utf-8', errors='replace')
            progress = [json.loads(s.split(':', 1)[1]) for s in partial.splitlines()
                        if s.startswith('PURRPOSE_PROGRESS:')]
            result = {'status': 'incomplete', 'failed_stage': progress[-1]['stage'] if progress else 'jdbc_worker',
                      'progress': progress, 'error_category': 'worker_deadline_45_seconds',
                      'case_qualified': False, 'limit': 'Client stopped; remote read cancellation is not guaranteed'}
        result['preflight'] = check
        result['automatic_retries'] = 0
        result['supporter_identity_view'] = supporter_identity_view(result)
    result['observed_at'] = datetime.now().astimezone().isoformat()
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output/'result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        if args.live:
            (args.output/'index.html').write_text(render_identity_report(result), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
