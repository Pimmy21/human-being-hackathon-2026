from unittest import TestCase
from unittest.mock import patch
from .public_reader import read_fixed_articles, parse_article, ReadFailure, download
from .research_case import SOURCES
from .server import LocalApp


class ReaderTests(TestCase):
    def test_fixed_url_and_script_exclusion(self):
        with self.assertRaises(ReadFailure):
            download('http://127.0.0.1/private')
        text = 'Lucy and kittens need care. '*10
        result = parse_article('<nav>not evidence</nav><div class="single-news"><p>'+text+'</p><script>bad()</script></div><footer>outside</footer>')
        self.assertIn('Lucy', result['text'])
        self.assertNotIn('bad()', result['text'])
        self.assertNotIn('outside', result['text'])

    def test_robots_denial_prevents_article_reads(self):
        calls=[]
        def reader(url):
            calls.append(url)
            return 'User-agent: *\nDisallow: /news/'
        result=read_fixed_articles(reader)
        self.assertEqual(len(calls),1)
        self.assertEqual(result['status'],'read_incomplete')
        self.assertFalse(result['qualified'])

    def test_success_does_not_certify_facts(self):
        def reader(url):
            return 'User-agent: *\nAllow: /' if url.endswith('robots.txt') else '<article>'+('Untrusted page words. '*10)+'</article>'
        result=read_fixed_articles(reader)
        self.assertEqual(result['status'],'read_complete')
        self.assertFalse(result['qualified'])
        self.assertIsNone(result['remaining_minor'])

    def test_failure_has_no_old_text_fallback(self):
        def reader(url):
            if url.endswith('robots.txt'): return ''
            raise ReadFailure('http_429')
        result=read_fixed_articles(reader)
        self.assertTrue(all('text' not in r for r in result['sources']))

    def test_duplicate_click_reuses_recent_attempt(self):
        app=LocalApp()
        with patch('purrpose.server.bounded_read', return_value={'status':'read_incomplete','sources':[]}) as read:
            app.dispatch('/api/research/read',{})
            result=app.dispatch('/api/research/read',{})
            self.assertTrue(result['cached'])
            self.assertEqual(read.call_count,1)
        with self.assertRaises(ValueError):
            app.dispatch('/api/research/read',{'url':SOURCES[0]['url']})
