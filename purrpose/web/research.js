'use strict';
const button=document.getElementById('assess-research');
button.addEventListener('click',async()=>{
  const host=document.getElementById('research-result');button.disabled=true;
  host.textContent='Assessing saved observations…';
  const add=(tag,text)=>{const node=document.createElement(tag);node.textContent=text;host.append(node);};
  try{
    const response=await fetch('/api/research',{method:'POST',headers:{'Content-Type':'application/json','X-Purrpose-Local':'1'},body:'{}',signal:AbortSignal.timeout(10000)});
    if(!response.ok)throw Error('Assessment did not complete.');const result=await response.json();
    host.replaceChildren();add('h3','Pending verification · remaining amount unknown');
    add('p','Assessment date: '+result.assessment_date+' · saved observations: '+result.source_observed_on);
    add('p','Latest organization-reported state: '+result.latest_reported_state);
    for(const gate of result.gates)add('p',gate.gate+': '+gate.explanation);
    for(const limitation of result.limitations)add('p',limitation);
  }catch(_){host.textContent='Assessment unavailable. No new source check or qualification is confirmed. Please try again manually.';}
  finally{button.disabled=false;}
});
const readButton=document.getElementById('read-public');
readButton.addEventListener('click',async()=>{
 const host=document.getElementById('public-result');readButton.disabled=true;host.textContent='Reading permitted public pages…';
 try{const response=await fetch('/api/research/read',{method:'POST',headers:{'Content-Type':'application/json','X-Purrpose-Local':'1'},body:'{}',signal:AbortSignal.timeout(65000)});if(!response.ok)throw Error();const result=await response.json();host.replaceChildren();const add=t=>{const n=document.createElement('p');n.textContent=t;host.append(n);};add(result.status+' · '+(result.observed_at||'No confirmed read time')+(result.cached?' · cached recent attempt':''));add('Retrieval only. Qualification remains pending; remaining amount is unknown.');if(result.error)add('Failed at '+result.stage+': '+result.error);for(const source of result.sources||[]){add(source.source_id+': '+source.status+(source.error?' · '+source.error:''));if(source.published_metadata)add('Page metadata publication time (not independently verified): '+source.published_metadata);if(source.text)add('Untrusted text preview: '+source.text.slice(0,350));}renderSourceAnalysis(result,host);if(result.review)add('Real review: '+result.review.status+' · H-MEM: '+result.review.memory.status+' · saved record: '+(result.review.memory.saved_memory_id||'none'));add('No model interpreted these pages. Text may include related content; publication metadata may differ from the displayed date. Saved manual findings above have not been silently replaced.');}
 catch(_){host.textContent='Read did not complete. No new evidence is confirmed; no automatic retry.';}
 finally{readButton.disabled=false;}
});
function renderSourceAnalysis(result,host){
 if(!result.analysis)return;const a=result.analysis;const add=t=>{const p=document.createElement('p');p.textContent=t;host.append(p);};
 add('Rule-based source analysis · pending verification');
 for(const d of a.publication_dates)add(d.source_id+' · Ontario publication date: '+d.ontario_calendar_date);
 for(const c of a.candidates)add('Organization statement candidate ('+c.source_id+', text '+c.start+'–'+c.end+'): '+c.quote);
 if(!a.candidates.length)add('No supported statement pattern identified; no fact has been invented.');
 add('Funding: unknown. Same-case cost, raised funds and allocation are not validated.');
 for(const limitation of a.limitations)add(limitation);
}
