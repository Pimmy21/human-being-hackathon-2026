import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch

from .zetaris import EXPECTED_BN, IDENTITY_SQL, error_category, normalize_identity, read_config, remote_ssl, supporter_identity_view, render_identity_report


class ZetarisTests(TestCase):
    def test_historical_match_never_establishes_current_qualification(self):
        result = normalize_identity([[EXPECTED_BN, 'TORONTO CAT RESCUE', 'ETOBICOKE', 'ON']])
        self.assertEqual(result['status'], 'historical_identity_matched')
        self.assertEqual(result['reporting_year'], 2024)
        self.assertFalse(result['current_registration_verified'])
        self.assertFalse(result['case_qualified'])

    def test_absent_mismatched_or_duplicate_records_not_passed(self):
        for rows in ([], [['OTHER', 'Name', 'City', 'ON']], [[EXPECTED_BN, 'Name', None, 'ON']],
                     [[EXPECTED_BN, 'Name', 'City', 'ON']]*2):
            with self.subTest(rows=rows):
                self.assertEqual(normalize_identity(rows)['status'], 'incomplete')

    def test_ssl_required_and_localhost_rejected(self):
        self.assertTrue(remote_ssl('jdbc:zetaris:lightning@cluster.example:10000/default;ssl=true'))
        for url in ('jdbc:hive2://localhost:10000/default;ssl=true',
                    'jdbc:zetaris:lightning@cluster.example:10000/default',
                    'jdbc:hive2://cluster.example:10000/default;ssl=false',
                    'jdbc:hive2://cluster.example:10000/default;ssl=true;useSSL=false'):
            with self.subTest(url=url):
                self.assertFalse(remote_ssl(url))

    def test_source_error_sanitized_and_not_registry_finding(self):
        secret = 'sensitive-key'
        category = error_category(RuntimeError('HTTP 504 '+secret))
        self.assertEqual(category, 'upstream_source_504')
        view = supporter_identity_view({'failed_stage': 'source_query', 'error_category': category})
        self.assertFalse(view['source_failure_is_fraud'])
        self.assertNotIn(secret, str(view))

    def test_identity_view_consumes_actual_returned_name_not_synthetic_cat(self):
        identity = normalize_identity([[EXPECTED_BN, 'TORONTO CAT RESCUE', 'ETOBICOKE', 'ON']])
        view = supporter_identity_view({'identity': identity})
        self.assertEqual(view['organization_full_name'], 'TORONTO CAT RESCUE')
        self.assertFalse(view['qualified_recommendation'])
        self.assertNotIn('Maple', str(view))
        identity['organization_full_name'] = '<script>untrusted name</script>'
        page = render_identity_report({'identity': identity})
        self.assertNotIn('<script>', page)
        self.assertIn('&lt;script&gt;', page)

    def test_fixed_query_is_single_read_only_statement(self):
        self.assertTrue(IDENTITY_SQL.startswith('SELECT '))
        self.assertNotIn(';', IDENTITY_SQL)
        self.assertNotIn('CREATE', IDENTITY_SQL)

    def test_configuration_reads_only_required_names(self):
        with TemporaryDirectory() as d, patch.dict(os.environ, {}, clear=True):
            f = Path(d)/'.env.local'
            f.write_text('ZETARIS_USERNAME=test\nUNRELATED_SECRET=hidden\nZETARIS_JDBC_URL=a=b\n')
            values = read_config(f)
            self.assertEqual(values['ZETARIS_JDBC_URL'], 'a=b')
            self.assertNotIn('UNRELATED_SECRET', values)

    def test_auth_error_classified_without_raw_exception(self):
        self.assertEqual(error_category(RuntimeError('401 unauthorized private-token')), 'authentication_failed')
        self.assertEqual(error_category(RuntimeError('403 access denied private-token')), 'permission_denied')


if __name__ == '__main__':
    main()
