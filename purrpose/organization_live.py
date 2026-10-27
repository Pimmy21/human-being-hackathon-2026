"""Scoped organization publication guidance from actual current-page observations."""
import re

FIELDS=[
 ('case_medical','Case-specific medical evidence',r'\b(veterinar\w*|surgery|treatment|diagnos\w*|estimate)\b',
  'Publish a dated, appropriately redacted clinical statement or estimate linked to the named animal, with issuer and proposed care. General medical wording does not prove a case.'),
 ('funding','Corresponding funding breakdown',r'(?:\$\s*\d|\bCAD\s*\d|\b(raised|fundraising goal|funding target|grant)\b)',
  'Publish same-case estimated cost, received total, other support, whether grants overlap, currency and as-of date. Explain any surplus allocation. Do not infer a case total from general donation amounts.'),
 ('case_update','Dated case update',r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+\d{1,2},?\s+20\d{2}\b|\b20\d{2}-\d{2}-\d{2}\b',
  'Publish a clear case update date and current status. Article dates, event dates and this retrieval time are different; the system has not established which date applies to the animal.'),
 ('treatment_location','Treatment location',r'\b(treat\w* (?:in|at)|clinic in|hospital in|treatment city)\b',
  'State the treatment city for this case. An office address or the organization name does not establish where the animal is treated.'),
 ('identity','Organization identity information',r'\b\d{9}\s*RR\s*\d{4}\b',
  'Publish the full legal organization name, public contact and applicable registration number or official identity reference. The system must separately check current records and recipient linkage.')]

def organization_gaps(result):
 pages=[p for p in result.get('candidates',[]) if p.get('status')=='read']
 fields=[]
 for key,label,pattern,advice in FIELDS:
  mentions=[]
  for page in pages:
   text=page.get('text','');match=re.search(pattern,text,re.I)
   if match:
    start=max(0,match.start()-70);end=min(len(text),match.end()+130)
    mentions.append({'url':page['url'],'start':start,'end':end,'quote':text[start:end]})
  fields.append({'field':key,'label':label,'status':'related_wording_found_needs_case_check' if mentions else 'not_found_in_read_pages' if pages else 'unable_to_assess',
                 'observations':mentions,'what_to_publish_or_clarify':advice,
                 'verified':False})
 return {'mode':'organization_live_gap_guidance','pages_read':len(pages),'website_fully_reviewed':False,
   'representation_authority_verified':False,'qualified':False,'fields':fields,
   'scope_note':'Only the candidate pages listed above were checked. Not found here does not mean absent from your entire website. Terms and dates are clues, not verified documents or complete evidence.',
   'system_checks':['Current organization identity and donation-recipient linkage','Clinical issuer/document authenticity','Case-specific current funding consistency','Applicable official risk-source coverage'],
   'next_step':'Publish appropriate information on your own website, then run a fresh review. Purrpose does not edit the website or accept private uploads.',
   'privacy':'Do not publish donor details, payment credentials or private unredacted records. Better documentation does not guarantee qualification or donations.'}
