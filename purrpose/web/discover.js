'use strict';
const host=document.getElementById('output');
const button=document.getElementById('go');
const notice=document.getElementById('notice');
function el(tag,text){const value=document.createElement(tag);if(text!==undefined)value.textContent=text;return value;}
function link(parent,url,label){
  try{const u=new URL(url);if(u.protocol!=='https:')return;const a=el('a',label||url);a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';parent.append(a);}catch(_){}
}
function disclosure(parent,label){const details=el('details');details.append(el('summary',label));parent.append(details);return details;}
function accessChecks(result){
  if(!result.admission)return;
  const card=el('article');card.append(el('h3','Access checks — not trust verification'),el('p','Ontario location, official organization identity and your authority to represent it have not been verified.'));
  const details=disclosure(card,'Show the access and page-reading checks');
  for(const step of result.admission.checks||[])details.append(el('p',step.stage+' — '+step.status+(step.error?' / '+step.error:'')));
  for(const step of result.admission.network_checks||[])details.append(el('p','Public DNS checked before connection; HTTPS hostname verification required; redirects not followed. '+step.url));
  host.append(card);
}
function renderOrganization(review){
  if(!review)return;
  const section=el('section');section.append(el('h2','What should our organization add or clarify?'),el('p',review.scope_note),el('p','Pages assessed: '+review.pages_read+' · identity/representation not authenticated.'));
  for(const field of review.fields){
    const card=el('article');
    const status=field.status==='unable_to_assess'?'Unable to assess because no candidate page was read.':field.status==='not_found_in_read_pages'?'Not found in the pages read.':'Related wording found; not yet established for a specific case.';
    card.append(el('h3',field.label),el('p',status),el('p','What to publish or clarify: '+field.what_to_publish_or_clarify));
    if(field.observations.length){const details=disclosure(card,'Read the source wording');for(const observation of field.observations){details.append(el('blockquote',observation.quote));link(details,observation.url,'Source of this wording');}}
    section.append(card);
  }
  const checks=disclosure(section,'Independent checks the system still owes you');
  for(const check of review.system_checks)checks.append(el('p',check));
  section.append(el('p',review.next_step),el('p',review.privacy));host.append(section);
}
function render(result){
  const statuses={read_complete:'Reading completed',partial_read:'Some pages read; others unavailable',blocked:'Access blocked',incomplete:'Could not complete the read',no_relevant_links_found_in_entry:'No relevant links found in this entry page'};
  host.append(el('h2',result.organization||'Discovery result'),el('p','Result: '+(statuses[result.status]||result.status)+' · read at '+(result.observed_at?new Date(result.observed_at).toLocaleString():'not recorded')),el('p','Memory: '+(result.memory?.status||'unavailable')+(result.memory?.memory_id?' · '+result.memory.memory_id:'')));
  if(result.error)host.append(el('p','Stopped: '+result.error));
  accessChecks(result);
  if(document.getElementById('org-mode').checked)renderOrganization(result.organization_review);
  const requests=disclosure(host,'Actual requests ('+(result.requests||[]).length+')');
  const list=el('ol');
  for(const request of result.requests||[]){const item=el('li',request.stage+' — '+request.status+(request.error?' / '+request.error:'')+' · ');link(item,request.url);list.append(item);}requests.append(list);
  if(result.candidates?.length)host.append(el('h2','Pages read and source excerpts'));
  for(const row of result.candidates||[]){
    const card=el('article');card.append(el('h3',row.title||row.link_text||'Candidate'));link(card,row.url);
    card.append(el('p',row.status==='read'?'Read as unverified publisher content.':'Could not read: '+(row.error||'unavailable')));
    const details=disclosure(card,'Show discovery source and excerpts');details.append(el('p','Found on: '+row.discovered_from));
    for(const excerpt of row.excerpts||[])details.append(el('blockquote',excerpt.quote));
    card.append(el('p','A relevant word is not proof of a current appeal. Medical authenticity, need and funding remain unverified. Remaining amount: unknown.'));host.append(card);
  }
  if(!result.candidates?.length)host.append(el('p','No candidate page was returned. This does not mean the organization has no needs.'));
}
document.getElementById('discovery').addEventListener('submit',async event=>{
  event.preventDefault();button.disabled=true;host.replaceChildren();
  notice.textContent='Checking access and reading public pages… up to 45 seconds plus memory save.';
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),65000);
  try{
    const custom=document.getElementById('source-mode').value==='custom';
    if(custom&&!document.getElementById('public-confirm').checked)throw Error('Public confirmation required');
    const body=custom?{url:document.getElementById('public-url').value.trim()}:{site_id:document.getElementById('site').value};
    const response=await fetch(custom?'/api/discover-url':'/api/discover-site',{method:'POST',headers:{'Content-Type':'application/json','X-Purrpose-Local':'1'},body:JSON.stringify(body),signal:controller.signal});
    if(!response.ok)throw Error('Request failed');
    render(await response.json());notice.textContent='Finished. No model calls and no qualification issued.';
  }catch(_){notice.textContent='Request failed or timed out; no automatic retry. Check the backend before repeating.';}
  finally{clearTimeout(timer);button.disabled=false;}
});
if(new URLSearchParams(location.search).get('role')==='organization')document.getElementById('org-mode').checked=true;
const sourceMode=document.getElementById('source-mode');
sourceMode.addEventListener('change',()=>{
  const custom=sourceMode.value==='custom';document.getElementById('custom-source').hidden=!custom;document.getElementById('listed-source').hidden=custom;document.getElementById('public-url').required=custom;document.getElementById('public-confirm').required=custom;
});
