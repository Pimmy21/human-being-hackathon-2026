"""Two fixed public articles only; no redirects, scripts, media or paid APIs."""
import hashlib
from html.parser import HTMLParser
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.robotparser import RobotFileParser
from .research_case import SOURCES

AGENT = 'PurrposeResearch/0.1'
ROBOTS = 'https://guelphhumane.ca/robots.txt'
URLS = {s['url'] for s in SOURCES} | {ROBOTS}


class ReadFailure(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ReadFailure('redirect_not_followed')


def download(url):
    if url not in URLS:
        raise ReadFailure('url_not_permitted')
    request = Request(url, headers={'User-Agent': AGENT, 'Accept': 'text/html,text/plain', 'Accept-Encoding': 'identity'})
    try:
        with build_opener(NoRedirect).open(request, timeout=6) as response:
            raw = response.read(524289)
            if len(raw) > 524288:
                raise ReadFailure('response_too_large')
            mime = response.headers.get_content_type()
            if mime not in ('text/html', 'text/plain'):
                raise ReadFailure('unsupported_content_type')
            return raw.decode('utf-8', errors='replace')
    except HTTPError as error:
        if url == ROBOTS and error.code == 404:
            return ''  # Standard absent robots file; not a terms/license grant.
        raise ReadFailure('http_'+str(error.code)) from None
    except (URLError, TimeoutError, OSError):
        raise ReadFailure('network_or_timeout') from None


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.ignore = 0
        self.parts = []
        self.published = None
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in ('meta', 'img', 'br', 'hr', 'input', 'link', 'source', 'wbr', 'embed', 'area', 'base', 'col', 'param', 'track'):
            self.stack.append((tag, 'single-news' in attrs.get('class', '').split()))
        if tag == 'meta' and attrs.get('property') == 'article:published_time':
            self.published = attrs.get('content')
        if tag in ('script', 'style', 'noscript'):
            self.ignore += 1
        if tag in ('main', 'article'):
            self.depth += 1

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if tag in ('script', 'style', 'noscript'):
            self.ignore = max(0, self.ignore-1)
        if tag in ('main', 'article'):
            self.depth = max(0, self.depth-1)

    def handle_data(self, data):
        if (self.depth or any(selected for _, selected in self.stack)) and not self.ignore and data.strip():
            self.parts.append(data.strip())


def parse_article(html):
    parser = ArticleParser()
    parser.feed(html)
    text = re.sub(r'\s+', ' ', ' '.join(parser.parts))
    if len(text) < 100:
        raise ReadFailure('article_body_not_identified')
    return {'published_metadata': parser.published, 'text': text[:16000],
            'text_truncated': len(text) > 16000,
            'content_sha256': hashlib.sha256(html.encode()).hexdigest()}


def read_fixed_articles(reader=download):
    observed = datetime.now(timezone.utc).isoformat()
    try:
        robots = reader(ROBOTS)
        if '<html' in robots.casefold() or len(robots) > 100000:
            raise ReadFailure('robots_unreadable')
        policy = RobotFileParser()
        policy.parse(robots.splitlines())
    except ReadFailure as error:
        return {'status': 'read_incomplete', 'stage': 'robots', 'error': str(error),
                'observed_at': observed, 'sources': [], 'qualified': False, 'remaining_minor': None}
    results = []
    for source in SOURCES:
        row = {'source_id': source['source_id'], 'url': source['url'], 'publisher': source['publisher']}
        if not policy.can_fetch(AGENT, source['url']):
            results.append({**row, 'status': 'not_read', 'error': 'robots_disallowed'})
            continue
        # Honor declared delays by declining this minimal reader rather than sleeping/retrying.
        if policy.crawl_delay(AGENT) or policy.request_rate(AGENT):
            results.append({**row, 'status': 'not_read', 'error': 'robots_rate_requires_scheduler'})
            continue
        try:
            parsed = parse_article(reader(source['url']))
            results.append({**row, 'status': 'read', **parsed})
        except ReadFailure as error:
            results.append({**row, 'status': 'read_failed', 'error': str(error)})
    return {'status': 'read_complete' if all(s['status'] == 'read' for s in results) else 'read_incomplete',
            'mode': 'live_fixed_public_read', 'observed_at': observed, 'sources': results,
            'qualified': False, 'remaining_minor': None,
            'limitations': ['Retrieved text is untrusted source content, not verified evidence.',
                            'No medical, funding, identity or risk gate has passed because of this read.',
                            'Robots access is not a copyright license or blanket recurring-use permission.',
                            'No model calls, scripts, media, external forms or links were executed.']}


def bounded_read():
    try:
        result = subprocess.run([sys.executable, '-m', 'purrpose.public_reader'],
                                capture_output=True, timeout=25, check=True)
        return json.loads(result.stdout)
    except (subprocess.SubprocessError, ValueError):
        return {'status': 'read_incomplete', 'stage': 'worker', 'error': 'deadline_or_worker_failure',
                'sources': [], 'qualified': False, 'remaining_minor': None}


if __name__ == '__main__':
    try:
        result = read_fixed_articles()
    except Exception:
        result = {'status': 'read_incomplete', 'stage': 'worker', 'error': 'reader_failure',
                  'sources': [], 'qualified': False, 'remaining_minor': None}
    print(json.dumps(result, ensure_ascii=True))
