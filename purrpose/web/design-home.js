'use strict';
const api=createPurrposeClient();
const form=document.getElementById('prompt'),box=document.getElementById('appeal');
const send=document.getElementById('send'),notice=document.getElementById('notice');
const chatScroll=document.getElementById('chat-scroll');
const chatsBox=document.getElementById('chats'),chatList=document.getElementById('chat-list'),intro=document.getElementById('intro');
const panel=document.getElementById('panel'),panelToggle=document.getElementById('panel-toggle');
const views={review:document.getElementById('view-review'),map:document.getElementById('view-map')};
const tabs={review:document.getElementById('tab-review'),map:document.getElementById('tab-map')};
const chats=[];let current=null,busy=false,mapToken=0;
const node=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
const words=t=>String(t).replace(/_/g,' ');
const SOURCE_NAMES={'lucy-appeal':'Appeal article (13 Oct)','lucy-update':'Update article (14 Oct)'};
function when(iso){const d=iso?new Date(iso):null;return d&&!isNaN(d)?d.toLocaleString([], {day:'numeric',month:'short',hour:'numeric',minute:'2-digit'}):'time not confirmed';}
const picks=document.querySelectorAll('[data-pick]');
function scheme(value){const warm=value==='warm';document.documentElement.dataset.scheme=warm?'warm':'cool';for(const p of picks)p.setAttribute('aria-pressed',String(p.dataset.pick===(warm?'warm':'cool')));for(const id of ['fav-ico','fav-svg'])document.getElementById(id).href=warm?'/design-favicon-warm.svg':'/design-favicon.svg';try{localStorage.setItem('purrpose-scheme',warm?'warm':'cool');}catch(_){}}
for(const p of picks)p.addEventListener('click',()=>scheme(p.dataset.pick));
try{scheme(localStorage.getItem('purrpose-scheme')||'cool');}catch(_){scheme('cool');}
function sync(){send.disabled=busy||!box.value.trim();box.style.height='auto';box.style.height=Math.min(box.scrollHeight,220)+'px';}
box.addEventListener('input',sync);
box.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();if(!send.disabled)form.requestSubmit();}});
for(const chip of document.querySelectorAll('[data-text]'))chip.addEventListener('click',()=>{box.value=chip.dataset.text;sync();box.focus();});
function link(parent,label,url){try{const u=new URL(url);if(u.protocol!=='https:'||u.username||u.password)return;const a=node('a',label);a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';const p=node('p');p.append(a);parent.append(p);}catch(_){}}
function action(parent,label,message){const b=node('button',label);b.type='button';b.addEventListener('click',()=>submit(message));parent.append(b);}
function details(parent,label,value){const d=node('details');d.append(node('summary',label),node('pre',JSON.stringify(value,null,2)));parent.append(d);}
function render(result,host,chat){
 const a=node('article');const who=node('p','Purrpose');who.className='who';a.append(who,node('p',result.reply));
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
  action(a,'What is still missing?','Lucy what evidence is missing?');action(a,'Refresh the two articles','refresh Lucy');action(a,'Read saved review','Lucy history');
 }
 if(result.live_read){const live=result.live_read;const check=node('ul');check.className='source-check';
  const item=(t,ok)=>{const li=node('li',t);li.className=ok?'ok':'warn';check.append(li);};
  item((live.status==='read_complete'?'Source check complete':'Source check incomplete')+' · '+when(live.observed_at)+(live.cached?' · reused a recent read':''),live.status==='read_complete');
  for(const s of live.sources||[])item((SOURCE_NAMES[s.source_id]||words(s.source_id))+': '+(s.status==='read'?'read':words(s.status))+(s.error?' · '+words(s.error):''),s.status==='read');
  if(live.error)item('Stopped at '+words(live.stage)+': '+words(live.error),false);
  if(live.review){const m=live.review.memory.status;item('Review result: '+words(live.review.status)+' · memory (H-MEM): '+(m==='saved'?'saved':words(m)),m==='saved');}
  a.append(check);
  if(live.analysis)details(a,'Source-linked candidate statements; not proof',live.analysis);
 }
 if(result.publication_checklist?.length){
  const list=node('ul');
  for(const f of result.publication_checklist){const item=node('li');
   item.append(node('strong',f.label+': '),document.createTextNode(f.status==='unable_to_assess'?'Not assessed — general guidance. ':f.status==='not_found_in_read_pages'?'Not found in the pages read. ':'Related wording found; still needs verification. '),node('p',f.what_to_publish_or_clarify));
   for(const observation of (f.observations||[]).slice(0,1)){item.append(node('blockquote',observation.quote));link(item,'Source for this observation',observation.url);}
   list.append(item);
  }
  a.append(list,node('p','Update your own public website, then ask for a fresh check. These suggestions do not guarantee trust or donations.'));
 }
 if(result.site_review){const r=result.site_review;
  if(!result.source_summary)a.append(node('p','Website reading finished; open Review for the available information.'));
  for(const page of (r.candidates||[]).filter(c=>c.status==='read'))link(a,page.title||page.url,page.url);
  if(result.memory_note)a.append(node('p',result.memory_note));

 }
 if(result.directory_result){const r=result.directory_result;
  a.append(node('p','2024 government directory · cat-related names only · up to 3 website checks · city/name order'));
  for(const c of r.candidates||[]){a.append(node('h2',c.organization_full_name),node('p','Historical office city: '+c.reported_city+' · Charity number: '+c.organization_number),node('p','Website check: '+words(c.website_status)+' · Current need and remaining amount: unverified'));
   link(a,'Government identity source',c.identity_source);if(c.website_url){link(a,'Historically reported website',c.website_url);action(a,'Investigate this website','As a supporter, check '+c.website_url);}
   const review=c.website_review;if(review){a.append(node('p','Pages read: '+(review.organization_review?.pages_read||0)));details(a,'Website observations and missing information',review.organization_review||review);}}
  if((r.pending_website_candidates||[]).length){a.append(node('h3','Website address still to confirm'));for(const c of r.pending_website_candidates)a.append(node('p',c.organization_full_name+' — '+c.reported_city+' · no unique website in this historical contact source; not a negative finding.'));}
  a.append(node('p','H-MEM: '+words(r.memory?.status||'not configured')));details(a,'Discovery scope and actual tool results',{status:r.status,summary:r.directory_summary,limits:r.limits,tools:r.tools});
 }
 if(result.registry_result){const r=result.registry_result,id=r.identity||r;a.append(node('h2',id.organization_full_name||'Historical registry lookup'),node('p','2024 historical identity only; not current status or case approval.'),node('p','Query: '+words(r.status)),node('p','H-MEM: '+words(r.memory.status)+(r.memory.memory_id?' · '+r.memory.memory_id:'')));link(a,'Government dataset',r.source);}
 if(result.workflow_history){const h=result.workflow_history;a.append(node('p','Retained history: '+(h.entries||[]).length+' records. No new source or SQL request.'));for(const e of h.entries||[])a.append(node('p',e.memory_id+' · '+when(e.system_recorded_at)));}
 if(result.organization_review)a.append(node('p','Here is the public-information checklist. Open the Review tab to see each item.'));
 if(result.research_history)details(a,'Retained review; not a current source check',result.research_history);
 if(typeof buildReviewModel==='function'&&buildReviewModel(result)){const r=node('button','Open review');r.type='button';r.className='run-link';r.addEventListener('click',()=>{if(current!==chat)open(chat);select(chat,result);openPanel('review');});a.append(r);}
 sourcesAndLimits(a,result);
 if(result.agent_run&&result.agent_run.run_id){const b=node('button','See how this was worked out');b.type='button';b.className='run-link';b.addEventListener('click',()=>{if(current!==chat)open(chat);select(chat,result);openPanel('map');});a.append(b);}
 host.append(a);
}
async function submit(raw){
 const message=raw.trim();if(busy||!message)return;busy=true;sync();
 for(const b of document.querySelectorAll('.chip,.results button'))b.disabled=true;
 const chat=current,host=chat.host;if(chat.title==='New chat'){chat.title=message.slice(0,32);drawList();}intro.hidden=true;
 const you=node('article');you.className='you';const said=node('span','You said: ');said.className='sr-only';you.append(said,document.createTextNode(message));host.append(you);
 chatScroll.scrollTop=chatScroll.scrollHeight;notice.textContent='Checking…';
 try{
  let query=message;
  const result=await api.chat(chat.id,query);render(result,host,chat);chat.latest=result;if(current===chat)select(chat,result);chatScroll.scrollTop=chatScroll.scrollHeight;box.value='';const mi=result.model_intent;notice.textContent=(result.new_cloud_calls?`A configured model (${mi&&mi.route}) classified this message; code wrote the answer. `:mi&&mi.status==='cached'?'Reused an earlier model classification; no new cloud-model call. ':'No new cloud-model call. ')+'No payment. Source refresh happens only when explicitly requested.';
 }catch(error){notice.textContent=error.code==='timeout_result_unknown'?'The result is uncertain after a timeout. Backend work may still be running; do not automatically retry.':'The request did not complete. No new result is confirmed.';box.value=message;}
 finally{busy=false;for(const b of document.querySelectorAll('.chip,.results button'))b.disabled=false;sync();}
}
form.addEventListener('submit',e=>{e.preventDefault();submit(box.value);});
function sourcesAndLimits(parent,result){
 const d=node('details');d.className='sources-limits';d.append(node('summary','Sources & limits'));
 const add=t=>{if(t)d.append(node('p',t));};
 add(result.mode==='explicit_public_workflow'?'An explicit user action ran a bounded workflow or used its saved results. No model called for this action.':result.mode==='model_intent_validated'?'Your request was classified by a configured model; code wrote this answer.':'Your request was understood by bounded phrase matching; code wrote this answer.');
 const r=result.research;if(r){for(const s of r.sources||[])link(d,s.publisher+' · '+s.published_on,s.url);for(const t of r.limitations||[])add(t);}
 const q=result.results;if(q){for(const group of ['qualified','pending','no_current_gap'])for(const c of q[group]||[]){for(const s of c.evidence||[])link(d,s.publisher+' · '+s.source_date,s.reference);for(const t of c.limitations||[])add(t);}add(q.coverage);}
 if(result.live_read&&result.live_read.error)add('Source read problem at '+result.live_read.stage+': '+result.live_read.error);
 parent.append(d);
}
function drawList(){
 chatList.replaceChildren();
 for(const c of chats){const li=node('li');const b=node('button',c.title);b.type='button';b.setAttribute('aria-current',String(c===current));b.addEventListener('click',()=>open(c));li.append(b);chatList.append(li);}
}
function open(chat){
 current=chat;for(const c of chats)c.host.hidden=c!==chat;
 intro.hidden=chat.host.childElementCount>0;drawList();select(chat,chat.latest||null);
}
function newChat(){
 const host=node('section');host.className='results';host.setAttribute('role','log');host.setAttribute('aria-live','polite');host.setAttribute('aria-label','Conversation');
 chatsBox.append(host);const chat={id:crypto.randomUUID(),title:'New chat',host,latest:null};chats.push(chat);open(chat);box.focus();
}
document.getElementById('new-chat').addEventListener('click',()=>{if(!busy)newChat();});
/* Right-hand panel */
function openPanel(name){
 for(const k of Object.keys(tabs)){const on=k===name;tabs[k].setAttribute('aria-selected',String(on));tabs[k].tabIndex=on?0:-1;views[k].hidden=!on;}
 panel.classList.add('open');panelToggle.setAttribute('aria-expanded','true');
}
function closePanel(){panel.classList.remove('open');panelToggle.setAttribute('aria-expanded','false');}
for(const k of Object.keys(tabs))tabs[k].addEventListener('click',()=>openPanel(k));
document.querySelector('.tabs').addEventListener('keydown',e=>{
 if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();
 const order=Object.keys(tabs),at=order.findIndex(k=>tabs[k].getAttribute('aria-selected')==='true');
 const next=e.key==='Home'?0:e.key==='End'?order.length-1:(at+(e.key==='ArrowRight'?1:order.length-1))%order.length;
 openPanel(order[next]);tabs[order[next]].focus();
});
panelToggle.addEventListener('click',()=>panel.classList.contains('open')?closePanel():openPanel(tabs.map.getAttribute('aria-selected')==='true'?'map':'review'));
document.getElementById('panel-close').addEventListener('click',closePanel);
async function select(chat,result){
 const token=++mapToken,box=views.map;
 if(!result||!result.agent_run){emptyMap(box);showReview(chat,null);return;}
 showReview(chat,result);
 const agentRun=result.agent_run;let run=null,note=agentRun;
 if(agentRun.run_id){
  try{run=await api.run(agentRun.run_id);}catch(_){run=null;note={...agentRun,note:'Run details could not be loaded.'};}
  if(run&&run.status==='run_not_found'){run=null;note={...agentRun,note:'This run is no longer stored: runs are kept in memory, the last 50 only, and cleared on restart.'};}
 }
 if(token!==mapToken)return;
 renderAgentMap(box,buildMapModel(run,note));
}
function emptyMap(box){
 const p=node('p','Ask a question and the agents that work on it appear here, with what each one decided.');p.className='empty';
 const list=node('ol');list.className='map-cards map-preview';
 for(const name of ['Orchestrator','Evidence Collector','Evidence Evaluator','Dispute Resolver']){const li=node('li');const c=node('div');c.className='map-card state-skipped';const dot=node('span');dot.className='dot';c.append(dot,node('strong',name),node('span','Waiting'));c.lastChild.className='line';li.append(c);list.append(li);}
 box.replaceChildren(p,list);
}
function showReview(chat,result){
 const box=views.review;
 const model=result&&typeof buildReviewModel==='function'?buildReviewModel(result):null;
 if(model&&typeof renderReview==='function'){renderReview(box,model,{link});return;}
 const empty=node('p','Ask about a case, for example “Explore Lucy’s case”. Its evidence, funding and open questions appear here, each with its own status.');empty.className='empty';box.replaceChildren(empty);
}
/* Phone menu: the sidebar slides over the chat */
const sidebar=document.getElementById('sidebar'),scrim=document.getElementById('scrim'),menuBtn=document.getElementById('menu-btn');
function menu(open){sidebar.classList.toggle('open',open);scrim.hidden=!open;menuBtn.setAttribute('aria-expanded',String(open));}
menuBtn.addEventListener('click',()=>menu(true));
document.getElementById('sidebar-close').addEventListener('click',()=>menu(false));
scrim.addEventListener('click',()=>menu(false));
chatList.addEventListener('click',()=>menu(false));
document.addEventListener('keydown',e=>{if(e.key==='Escape'){menu(false);if(panel.classList.contains('open'))closePanel();}});
document.getElementById('new-chat').addEventListener('click',()=>menu(false));
newChat();emptyMap(views.map);sync();
/* A message sent from the home page arrives as ?q=… and is sent once, then removed from the address bar. */
try{const q=new URLSearchParams(location.search).get('q');if(q&&q.trim()){history.replaceState(null,'',location.pathname);submit(q.slice(0,1500));}}catch(_){}
