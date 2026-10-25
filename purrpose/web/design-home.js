'use strict';
const api=createPurrposeClient();
const form=document.getElementById('prompt'),box=document.getElementById('appeal');
const send=document.getElementById('send'),notice=document.getElementById('notice');
const host=document.getElementById('home-results');
const session=crypto.randomUUID();
let busy=false;
const node=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
const picks=document.querySelectorAll('[data-pick]');
function scheme(value){const warm=value==='warm';document.documentElement.dataset.scheme=warm?'warm':'cool';for(const p of picks)p.setAttribute('aria-pressed',String(p.dataset.pick===(warm?'warm':'cool')));for(const id of ['fav-ico','fav-svg'])document.getElementById(id).href=warm?'/design-favicon-warm.svg':'/design-favicon.svg';try{localStorage.setItem('purrpose-scheme',warm?'warm':'cool');}catch(_){}}
for(const p of picks)p.addEventListener('click',()=>scheme(p.dataset.pick));
try{scheme(localStorage.getItem('purrpose-scheme')||'cool');}catch(_){scheme('cool');}
function sync(){send.disabled=busy||!box.value.trim();box.style.height='auto';box.style.height=Math.min(box.scrollHeight,220)+'px';}
box.addEventListener('input',sync);
box.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();if(!send.disabled)form.requestSubmit();}});
for(const chip of document.querySelectorAll('[data-text]'))chip.addEventListener('click',()=>{box.value=chip.dataset.text;sync();box.focus();});
function link(parent,label,url){try{const u=new URL(url);if(u.protocol!=='https:'||!['guelphhumane.ca','apps.cra-arc.gc.ca'].includes(u.hostname))return;const a=node('a',label);a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';const p=node('p');p.append(a);parent.append(p);}catch(_){}}
function action(parent,label,message){const b=node('button',label);b.type='button';b.addEventListener('click',()=>submit(message));parent.append(b);}
function details(parent,label,value){const d=node('details');d.append(node('summary',label),node('pre',JSON.stringify(value,null,2)));parent.append(d);}
function render(result){
 const a=node('article');a.append(node('p','Purrpose'),node('p',result.reply));
 if(result.results){const r=result.results;
  if(r.status==='needs_preference'){action(a,'Anywhere in Ontario','anywhere in Ontario');action(a,'Ottawa','Ottawa');action(a,'Toronto','Toronto');}
  if(r.status==='no_city_match'||r.expansion_question)action(a,'Include Ontario-context leads','yes');
  for(const group of ['qualified','pending','no_current_gap'])for(const c of r[group]||[]){
   a.append(node('h2',c.organization_full_name+' — '+c.case_name),node('p',c.scenario_type==='synthetic'?'Fictional workflow example':'Real research lead · pending verification'),node('p','Treatment city: '+(c.case_city||'unverified')),node('p','Remaining need: '+(c.remaining_minor===null?'unknown':'CAD '+(c.remaining_minor/100).toFixed(2))));
   a.append(node('p',c.funding_notice));for(const s of c.evidence||[])link(a,s.publisher+' · '+s.source_date,s.reference);
   if(c.scenario_type==='real_public_observations')action(a,'Discuss this case','Tell me about Lucy');
  }
  if(r.coverage)a.append(node('p',r.coverage));
 }
 if(result.research){const d=result.research;a.append(node('h2',d.organization_display_name+' — '+d.case_name),node('p','Pending verification · remaining amount unknown'));
  for(const s of d.sources)link(a,s.publisher+' · '+s.published_on,s.url);
  details(a,'Saved official identity observation',d.official_identity_observation);
  details(a,'Saved published allocation statement',d.external_form_observation);
  details(a,'Unresolved checks',d.gates);
  action(a,'What is still missing?','Lucy what evidence is missing?');action(a,'Refresh the two articles','refresh Lucy');action(a,'Read saved review','Lucy history');
 }
 if(result.live_read){const live=result.live_read;a.append(node('p','Source read: '+live.status+' · '+(live.observed_at||'no confirmed time')+(live.cached?' · cached recent attempt':'')));
  for(const s of live.sources||[])a.append(node('p',s.source_id+': '+s.status+(s.error?' · '+s.error:'')));
  if(live.error)a.append(node('p','Failed at '+live.stage+': '+live.error));
  if(live.review)a.append(node('p','Review: '+live.review.status+' · H-MEM: '+live.review.memory.status));
  if(live.analysis)details(a,'Source-linked candidate statements; not proof',live.analysis);
 }
 if(result.organization_review){for(const g of result.organization_review.gap_checklist){a.append(node('h2',g.what_to_add),node('p','Action for: '+g.responsible_party),node('p',g.why),node('p',g.where_to_obtain_or_publish));}a.append(node('p',result.organization_review.privacy_note),node('p',result.organization_review.guarantee));}
 if(result.research_history)details(a,'Retained review; not a current source check',result.research_history);
 host.append(a);
}
async function submit(raw){
 const message=raw.trim();if(busy||!message)return;busy=true;sync();
 for(const b of document.querySelectorAll('.chip,.results button'))b.disabled=true;
 host.append(node('article','You: '+message));notice.textContent='Checking…';
 try{
  let query=message;
  if(/^https?:\/\//i.test(message)){
   const known=['https://guelphhumane.ca/news/urgent-abandoned-in-a-box-and-pregnant-lucy-needs-your-help/','https://guelphhumane.ca/news/update-lucy-gave-birth-to-her-kittens-at-ghs/'];
   if(!known.includes(message)){render({reply:'This prototype supports only the configured Lucy articles. This URL was not fetched. Try “I want to help a cat” or use the example request.'});notice.textContent='Unsupported URL; no source was fetched.';return;}
   query='Tell me about Lucy';
  }
  const result=await api.chat(session,query);render(result);box.value='';notice.textContent='No payment or new cloud-model call. Source refresh happens only when explicitly requested.';
 }catch(error){notice.textContent=error.code==='timeout_result_unknown'?'The result is uncertain after a timeout. Backend work may still be running; do not automatically retry.':'The request did not complete. No new result is confirmed.';box.value=message;}
 finally{busy=false;for(const b of document.querySelectorAll('.chip,.results button'))b.disabled=false;sync();}
}
form.addEventListener('submit',e=>{e.preventDefault();submit(box.value);});sync();
