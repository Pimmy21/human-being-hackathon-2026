const byId = id => document.getElementById(id);
const el = (tag, text) => {const n=document.createElement(tag); if(text!==undefined)n.textContent=text; return n;};
let busy=false;
const api=createPurrposeClient();
function view(id){document.querySelectorAll('.view').forEach(n=>n.hidden=n.id!==id); document.querySelectorAll('[data-view]').forEach(n=>n.classList.toggle('active',n.dataset.view===id));}
document.querySelectorAll('[data-view]').forEach(n=>n.addEventListener('click',()=>view(n.dataset.view)));
async function post(path,data){
  if(busy)throw Error('Please wait for the current operation.');
  busy=true;document.querySelectorAll('button').forEach(n=>n.disabled=true);byId('activity').textContent='Checking…';
  try{const operations={
    '/api/supporter':()=>api.supporter(data),
    '/api/organization':()=>api.organization(data.public_links),
    '/api/chat':()=>api.chat(data.session_id,data.message),
    '/api/feedback':()=>api.feedback(data),
    '/api/history':()=>api.history(data.cutoff??null),
    '/api/update':()=>api.demoUpdate(data.action,data.request_id),
    '/api/debug':()=>api.debug()
  };if(!operations[path])throw Error('Unsupported operation');return await operations[path]();}
  finally{busy=false;document.querySelectorAll('button').forEach(n=>n.disabled=false);byId('activity').textContent='';}
}
function error(e){byId('activity').textContent=e.message||'The operation did not complete.';}
function details(parent,label,value){const d=el('details');d.append(el('summary',label),el('pre',JSON.stringify(value,null,2)));parent.append(d);}
function renderCases(result){const host=byId('supporter-result');host.replaceChildren();host.append(el('p',result.message||result.question||result.status));
  for(const [group,title]of [['qualified','Meets synthetic checks'],['pending','Still needs verification'],['no_current_gap','No current disclosed gap']])for(const c of result[group]||[]){const a=el('article');a.append(el('h3',c.organization_full_name),el('p',`${title} · ${c.case_name} · ${c.case_city||'City unknown'}`),el('p',`Remaining need: ${c.remaining_minor===null?'Not yet known':'CAD '+(c.remaining_minor/100).toFixed(2)}`),el('p',c.funding_notice));for(const x of c.unpassed_requirements||[])a.append(el('p',x));details(a,'Evidence and source locations',c.evidence);a.append(el('p',c.scenario_type==='synthetic'?'No donation link: fictional case.':'Pending real lead; no verified payment action.'));if(c.scenario_type==='real_public_observations'){const b=el('button','Discuss this real lead');b.addEventListener('click',()=>{view('chat');byId('chat-input').value='Tell me about Lucy';byId('chat-form').requestSubmit();});a.append(b);}host.append(a);}
  const question=result.expansion_question||(result.status==='no_city_match'?result.question:null);if(question){host.append(el('p',question));const b=el('button','Yes, search other supported cities');b.addEventListener('click',()=>find(true));host.append(b);}}
async function find(expand=false){const city=byId('city').value;try{renderCases(await post('/api/supporter',{city:city||null,region_wide:!city,allow_expansion:expand,collection:byId('collection').value}));}catch(e){error(e);}}
byId('find-form').addEventListener('submit',e=>{e.preventDefault();find();});
byId('org-form').addEventListener('submit',async e=>{e.preventDefault();try{const r=await post('/api/organization',{public_links:[byId('public-link').value]});const h=byId('organization-result');h.replaceChildren(el('p',r.message));for(const g of r.gap_checklist||[]){const a=el('article');a.append(el('h3',g.what_to_add),el('p','Action for: '+(g.responsible_party||'organization')),el('p','Why: '+g.why),el('p','Where: '+g.where_to_obtain_or_publish),el('p','Next check: '+g.next_check));h.append(a);}h.append(el('p',r.privacy_note||''),el('p',r.guarantee||''));}catch(x){error(x);}});
document.querySelectorAll('[data-action]').forEach(b=>b.addEventListener('click',async()=>{try{const r=await post('/api/update',{action:b.dataset.action,request_id:crypto.randomUUID()});const h=byId('update-result');h.replaceChildren(el('p',`Update: ${r.status}. ${r.review?(r.review.qualified?'Synthetic checks passed.':'Not qualified; inspect missing evidence.'):'Review incomplete.'}`));if(r.review)h.append(el('p',`Remaining amount: ${r.review.remaining_minor===null?'unknown':'CAD '+(r.review.remaining_minor/100).toFixed(2)}`));details(h,'Update steps',r.update_events);}catch(e){error(e);}}));
byId('history-form').addEventListener('submit',async e=>{e.preventDefault();try{const r=await post('/api/history',{cutoff:byId('cutoff').value.trim()||null});const h=byId('history-result');h.replaceChildren(el('p',r.message));if(r.system_recorded_at)h.append(el('p','Known by: '+r.system_recorded_at));details(h,'Saved result and evidence',r);}catch(x){error(x);}});
byId('debug-button').addEventListener('click',async()=>{try{const r=await post('/api/debug',{});const h=byId('debug-result');h.replaceChildren();details(h,'Actual backend record',r);}catch(e){error(e);}});
fetch('/api/status').then(r=>r.json()).then(r=>{byId('connection').textContent=`Backend connected · H-MEM: ${r.memory} · Nightshift: ${r.nightshift} · New cloud calls: 0`;}).catch(error);view('supporter');
let chatSession=crypto.randomUUID();
byId('new-chat').addEventListener('click',()=>{chatSession=crypto.randomUUID();byId('messages').replaceChildren();});
byId('chat-form').addEventListener('submit',async e=>{
  e.preventDefault();const input=byId('chat-input');const message=input.value.trim();if(!message||busy)return;
  const host=byId('messages');host.append(el('p','You: '+message));input.value='';
  try{const r=await post('/api/chat',{session_id:chatSession,message});host.append(el('p','Purrpose: '+r.reply));
    if(r.organization_review){for(const gap of r.organization_review.gap_checklist){const a=el('article');a.append(el('h3',gap.what_to_add),el('p','Action for: '+gap.responsible_party),el('p',gap.why),el('p',gap.where_to_obtain_or_publish));host.append(a);}host.append(el('p',r.organization_review.guarantee));}
    if(r.research_history)details(host,'Saved Lucy review (not current verification)',r.research_history);
    if(r.live_read){const live=r.live_read;const a=el('article');a.append(el('h3','Requested source refresh: '+live.status),el('p','Observed: '+(live.observed_at||'No confirmed observation time')+(live.cached?' · recent cached attempt':'')));if(live.error)a.append(el('p','Failed stage: '+live.stage+' · '+live.error));for(const s of live.sources||[])a.append(el('p',s.source_id+': '+s.status+(s.error?' · '+s.error:'')));if(live.analysis)details(a,'Sourced statement candidates; not independent verification',live.analysis);host.append(a);}
    if(r.live_read?.review){const v=r.live_read.review;host.append(el('p','Real review: '+v.status+' · H-MEM: '+v.memory.status+' · saved record: '+(v.memory.saved_memory_id||'none')));}
    if(r.research){const d=r.research;const a=el('article');a.append(el('h3',d.organization_display_name+' · '+d.case_name),el('p','Saved real-source research · pending verification · remaining amount unknown'));for(const source of d.sources){const p=el('p');const link=el('a',source.publisher+' · '+source.published_on);link.href=source.url;link.target='_blank';link.rel='noopener noreferrer';p.append(link);a.append(p);}details(a,'Official identity observation (manual; not rechecked now)',d.official_identity_observation);details(a,'Published allocation observation (manual)',d.external_form_observation);details(a,'Unresolved evidence checks',d.gates);host.append(a);}
    if(r.results){renderCases(r.results);const copy=byId('supporter-result').cloneNode(true);copy.removeAttribute('id');copy.querySelectorAll('button').forEach(n=>n.remove());host.append(copy);}
  }catch(x){host.append(el('p','Message could not complete; please try again.'));error(x);}
});
view('chat');
byId('use-lucy-link').addEventListener('click',()=>{byId('public-link').value='https://guelphhumane.ca/news/update-lucy-gave-birth-to-her-kittens-at-ghs/';});


let feedbackAttempt=null;
byId('feedback-kind').addEventListener('change',()=>{byId('feedback-city-label').hidden=byId('feedback-kind').value!=='preference';});
byId('feedback-form').addEventListener('submit',async e=>{
 e.preventDefault();const kind=byId('feedback-kind').value;const payload={session_id:chatSession,kind,message:byId('feedback-note').value.trim(),city:kind==='preference'?byId('feedback-city').value:null};const signature=JSON.stringify(payload);if(!feedbackAttempt||feedbackAttempt.signature!==signature)feedbackAttempt={signature,id:crypto.randomUUID()};
 try{const result=await post('/api/feedback',{...payload,request_id:feedbackAttempt.id});const host=byId('feedback-result');host.replaceChildren(el('p',result.status),el('p',result.notice),el('p','Storage: '+result.storage),el('p','Facts, policy and qualification were not changed.'));feedbackAttempt=null;byId('feedback-note').value='';}catch(x){error(x);}
});

if(['chat','supporter','organization','feedback','history','demo'].includes(location.hash.slice(1)))view(location.hash.slice(1));
