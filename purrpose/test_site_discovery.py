from unittest import TestCase
from unittest.mock import patch
from .site_discovery import discover, canonical, SITES
class DiscoveryTests(TestCase):
 def test_related_story_medical_claims_are_not_current_article_evidence(self):
  from .site_discovery import parsed_candidate
  html='<main>'+('Lucy needs a safe place. '*10)+' Related news Different cat surgery cost $9000 in 2017.</main>'
  row=parsed_candidate('https://example.org/cat','Cat appeal',html,'https://example.org/')
  self.assertNotIn('9000',row['text'])
  self.assertFalse(any('surgery' in q['quote'] for q in row['excerpts']))
 def test_explicit_entry_honors_delay_without_following_links(self):
  from .site_discovery import discover_pages
  html='<main>'+('This named cat requires surgery. '*8)+'</main><a href="/news/posts/cat-two/">cat surgery</a>'
  reader=self.reader(html,robots='Crawl-delay: 10\nUser-agent: *\nDisallow:\n')
  with patch('purrpose.site_discovery.time.sleep') as sleep:
   r=discover_pages('ottawa',SITES['ottawa'],reader,include_entry=True)
  sleep.assert_called_once_with(10)
  self.assertEqual(len(self.calls),2)
  self.assertEqual(len(r['candidates']),1)
  self.assertEqual(r['status'],'read_complete')
  self.assertTrue(r['access_schedule']['entry_only'])
  self.assertFalse(r['qualified'])

 def test_long_delay_still_stops_without_sleep(self):
  from .site_discovery import discover_pages
  reader=self.reader('',robots='User-agent: *\nCrawl-delay: 60\nDisallow:\n')
  with patch('purrpose.site_discovery.time.sleep') as sleep:
   r=discover_pages('ottawa',SITES['ottawa'],reader,include_entry=True)
  sleep.assert_not_called()
  self.assertEqual(r['error'],'robots_scheduler_required')
 def reader(self,entry,robots='User-agent: *\nDisallow:\n',candidate=None):
  site=SITES['ottawa'];self.calls=[]
  def read(url):
   self.calls.append(url)
   if url.endswith('/robots.txt'):return robots
   if url==site['entry']:return entry
   return candidate or '<html><title>Cat care report</title><main>'+('The cat needs surgery according to this rescue. '*10)+'</main></html>'
  return read
 def test_discovers_non_predefined_url_and_quotes_source(self):
  r=discover('ottawa',self.reader('<a href="/news/posts/new-cat-treatment/">Kitten surgery appeal</a>'))
  self.assertEqual(len(r['candidates']),1);row=r['candidates'][0]
  self.assertIn('/news/posts/new-cat-treatment/',row['url']);self.assertEqual(row['relevance'],'cat_and_medical_terms_present');self.assertFalse(r['qualified']);self.assertIsNone(r['remaining_minor'])
  for x in row['excerpts']:self.assertEqual(row['text'][x['start']:x['end']],x['quote'])
 def test_no_links_is_not_no_needs(self):
  r=discover('ottawa',self.reader('<main>Welcome</main>'));self.assertEqual(r['status'],'no_relevant_links_found_in_entry')
 def test_robots_prevents_read(self):
  r=discover('ottawa',self.reader('',robots='User-agent: *\nDisallow: /'))
  self.assertEqual(r['error'],'robots_disallowed_entry');self.assertEqual(len(self.calls),1)
 def test_candidate_cap_and_no_external_or_query(self):
  html=''.join('<a href="/news/posts/cat-'+str(i)+'/">cat surgery</a>' for i in range(8))+'<a href="http://127.0.0.1/">cat surgery</a><a href="https://evil.com/">cat surgery</a>'
  r=discover('ottawa',self.reader(html));self.assertEqual(len(r['candidates']),3);self.assertEqual(len(self.calls),5)
 def test_userinfo_port_and_media_rejected(self):
  for url in ['https://user@www.ottawahumane.ca/a','https://www.ottawahumane.ca:99/a','https://www.ottawahumane.ca/a.pdf','https://www.ottawahumane.ca/a?q=x']:
   self.assertIsNone(canonical(url,SITES['ottawa']['entry'],SITES['ottawa']['origin']))
 def test_unknown_site_rejected(self):
  with self.assertRaises(ValueError):discover('https://private',lambda x:self.fail())
 def test_delay_requires_scheduler(self):
  r=discover('ottawa',self.reader('',robots='User-agent: *\nCrawl-delay: 10'))
  self.assertEqual(r['error'],'robots_scheduler_required')
