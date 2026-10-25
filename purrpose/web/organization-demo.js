'use strict';
// Explicit fictional walkthrough. No fetch, API client, upload or persistence.
const sample='https://example.invalid/willow/pip';
const form=document.getElementById('org-demo-form'),input=document.getElementById('org-demo-url');
const host=document.getElementById('org-demo-results');
let updated=false;
const n=(tag,text)=>{const value=document.createElement(tag);if(text!==undefined)value.textContent=text;return value;};
const original={
 organization:'Willow Cat Rescue (fictional)',case:'Pip — fracture treatment (fictional)',
 provided:['A named cat and a story describing a leg injury.','An organization name, contact page and donation link.','A target of CAD 2,000 and a reported CAD 700 raised, without a clear funding date.'],
 gaps:[
  {name:'Dated, corresponding medical material',why:'A rescue story alone does not establish the proposed treatment or its cost.',publish:'Publish a permitted, appropriately redacted estimate or clinical statement with issuer, date and Pip case reference.'},
  {name:'Current funding total and grant inclusion',why:'Without a date and overlap statement, the remaining need cannot be calculated safely.',publish:'Publish the same-case cost, amount received, as-of date, other grants, and whether those grants are already included.'},
  {name:'Treatment location and current case update',why:'A rescue office address is not necessarily where the cat is being treated.',publish:'Publish the treatment city and a dated case update, without private personal information.'}
 ]
};
function step(index){document.querySelectorAll('.org-steps li').forEach((item,i)=>{if(i===index)item.setAttribute('aria-current','step');else item.removeAttribute('aria-current');});}
function panel(title){const a=n('article');a.append(n('p','SIMULATED · Willow Cat Rescue / Pip'),n('h2',title));host.append(a);return a;}
function button(parent,label,fn){const b=n('button',label);b.type='button';b.addEventListener('click',fn);parent.append(b);return b;}
function systemChecks(parent){parent.append(n('h2','Still the system’s responsibility'),n('p','Identity and active registration, corresponding issuer authenticity, donation recipient ownership and approved risk checks have not run in this walkthrough. The organization cannot mark these as passed by adding a statement.'),n('p','No qualified recommendation or trust badge is issued. Missing information does not mean fraud.'));}
function review(){
 host.replaceChildren();step(updated?3:1);
 const a=panel(updated?'Recheck: public information is clearer':'Here is what a supporter can and cannot check');
 a.append(n('p','Website: '+sample),n('p','This is a fixed fictional page snapshot, not a live website read.'));
 const existing=n('div');existing.className='org-found';existing.append(n('h2',updated?'Provided in the updated sample':'Already on the sample website'));
 for(const text of original.provided.slice(0,updated?2:3))existing.append(n('p',text));
 if(updated){existing.append(n('p','Added: dated demo medical estimate linked to Pip; treatment city Ottawa; dated funding total with CAD 300 grant explicitly separate from the CAD 700 raised.'));
  existing.append(n('p','Illustrative disclosed remainder: CAD 2,000 − CAD 700 − CAD 300 = CAD 1,000. This is fictional arithmetic, not verified real funding.'));
 }
 existing.append(n('p','“Provided” describes page contents, not independent verification.'));a.append(existing);
 if(!updated){
  for(const gap of original.gaps){const d=n('div');d.className='org-gap';d.append(n('h2',gap.name),n('p','Why it matters: '+gap.why),n('p','What to publish: '+gap.publish));a.append(d);}
  a.append(n('p','Photos, videos or volunteer comments can provide context when permitted and relevant. Their format or popularity does not automatically establish medical need, funding or trust.'));
  systemChecks(a);button(a,'Help me prepare my website update',suggest);
 }else{
  a.append(n('h2','What changed after rechecking?'),n('p','The three public-information gaps in this example are addressed. The materials now give a supporter clearer context and a checkable explanation of the disclosed gap. They still require independent checks.'));
  systemChecks(a);button(a,'Preview what supporters would see',preview);
 }
 button(a,'Start over',reset);
}
function suggest(){
 host.replaceChildren();step(2);const a=panel('Publish on your own website — not inside Purrpose');
 a.append(n('p','In a real organization journey, you would publish appropriate public information, then give Purrpose the updated public URL. This demo only simulates that step. No document uploads or website editing happen here.'));
 a.append(n('h2','Example public update — all details fictional'));
 a.append(n('pre','Case: Pip, Willow Cat Rescue (fictional)\nUpdated: 24 October 2026\nTreatment city: Ottawa (fictional)\nCare: fracture treatment; dated estimate from Example Veterinary Clinic (fictional), linked to Pip.\nEstimated care cost: CAD 2,000\nReceived for this case as of this date: CAD 700\nOther support: CAD 300 grant, separate from the CAD 700\nDisclosed remainder: CAD 1,000\nSurplus policy: disclose whether extra money can support other animals.\nPublic sources: link the permitted redacted clinical statement and dated funding update.'));
 a.append(n('p','Do not publish private donor details, bank/payment credentials or sensitive unredacted medical information. A public statement is not proof that the underlying document or claim is authentic.'));
 button(a,'Simulate publishing this update',()=>{updated=true;published();});button(a,'Back to gaps',review);
}
function published(){host.replaceChildren();step(2);const a=panel('Updated sample page is ready');
 a.append(n('p','SIMULATION ONLY: the fictional external website now has a second snapshot containing the example update. No real website has changed.'),n('p','The organization now tells Purrpose which public page changed. Qualification does not change merely because someone says an update was published.'));
 button(a,'Recheck updated demo website',review);
}
function preview(){host.replaceChildren();step(4);const a=panel('Supporter view — clearer information, still pending');
 a.append(n('h2',original.organization+' — '+original.case),n('p','Status: pending independent checks'),n('p','What the organization reports: a corresponding estimate, dated funding breakdown and treatment city.'),n('p','Disclosed remaining need: CAD 1,000 (fictional; calculated from simulated organization disclosures, not independently confirmed).'),n('p','Source locations: updated sample appeal, dated demo estimate and funding statement. No live source links exist for this fictional example.'));
 systemChecks(a);a.append(n('p','A small rescue with checkable public information can be easier to discover and assess. Visibility is not a guarantee of donations or a certificate of trust.'));
 button(a,'Back to recheck results',review);button(a,'Start over',reset);
}
function reset(){updated=false;host.replaceChildren();input.value=sample;step(0);}
form.addEventListener('submit',e=>{e.preventDefault();if(input.value.trim()!==sample){host.replaceChildren();const a=panel('Use the fictional example for this walkthrough');a.append(n('p','This link has not been fetched or assessed. The demo only supports its fixed sample; entering a real URL does not produce a review.'));button(a,'Load fictional rescue example',()=>{input.value=sample;updated=false;review();});return;}updated=false;review();});
const picks=document.querySelectorAll('[data-pick]');
function scheme(value){const warm=value==='warm';document.documentElement.dataset.scheme=warm?'warm':'cool';for(const p of picks)p.setAttribute('aria-pressed',String(p.dataset.pick===(warm?'warm':'cool')));for(const id of ['fav-ico','fav-svg'])document.getElementById(id).href=warm?'/design-favicon-warm.svg':'/design-favicon.svg';try{localStorage.setItem('purrpose-scheme',warm?'warm':'cool');}catch(_){}}
for(const p of picks)p.addEventListener('click',()=>scheme(p.dataset.pick));
try{scheme(localStorage.getItem('purrpose-scheme')||'cool');}catch(_){scheme('cool');}reset();
