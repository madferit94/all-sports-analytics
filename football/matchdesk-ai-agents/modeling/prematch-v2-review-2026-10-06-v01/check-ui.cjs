'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),vm=require('node:vm');
const P=path.resolve(__dirname,'../..'),S=path.join(P,'simulation/pixel-v1-2026-10-06-v01'),simulation=require(path.join(S,'pixel-simulation.js'));
const checks=[];function check(name,expected,fn){try{const actual=fn();checks.push({name,expected,actual,status:'PASS'});}catch(e){checks.push({name,expected,actual:e.message,status:'FAIL'});}}
const actualBundle=JSON.parse(fs.readFileSync(path.join(P,'modeling/prematch-v2-2026-10-06-v01/future-predictions.json'),'utf8'));
check('Each stored probability reproduces outcome frequency on deterministic uniform grid','each class count within 1 / 10000',()=>{let largest=0;for(const p of actualBundle.predictions){const probs=['home','draw','away'].map(k=>p.probabilities[k]);const counts=[0,0,0];for(let i=0;i<10000;i++)counts[simulation.sample({model:p.model_id,status:p.status,probabilities:probs},()=>(i+.5)/10000).outcome]++;largest=Math.max(largest,...counts.map((n,i)=>Math.abs(n/10000-probs[i])));}assert.ok(largest<=.0001);return {fixtures:641,maxProbabilityDifference:largest};});
function dom(reduced){
 const queue=new Map();let next=0,cancels=0,requests=0;
 const win={matchMedia:()=>({matches:reduced}),requestAnimationFrame:fn=>{queue.set(++next,fn);requests++;return next;},cancelAnimationFrame:id=>{queue.delete(id);cancels++;}};
 const ctx=new Proxy({},{get:(obj,key)=>obj[key]||(()=>{})});
 const doc={defaultView:win,createElement(tag){return {tag,ownerDocument:doc,children:[],events:{},attributes:{},textContent:'',appendChild(n){this.children.push(n);return n;},append(...ns){ns.forEach(n=>this.appendChild(n));},remove(){this.removed=true;},setAttribute(k,v){this.attributes[k]=v;},addEventListener(k,fn){this.events[k]=fn;},getContext(){return ctx;}};}};
 return {doc,win,queue,tick(t){const list=[...queue.values()];queue.clear();list.forEach(f=>f(t));},counts(){return {requests,cancels,pending:queue.size};}};
}
for(const locale of ['ko','en'])check('18-second animation lifecycle and fictional label '+locale,'finished sample, zero queued frames, destroy remains inert',()=>{
 const d=dom(false),container=d.doc.createElement('div'),p={model:'independent-fixture',status:'EXPERIMENTAL_NOT_ADOPTED',probabilities:[0,1,0]};
 const handle=simulation.mount(container,p,{locale,rng:()=>.5}),section=container.children[0],controls=section.children.find(n=>n.className==='md-sim-controls');
 const text=section.children.map(n=>n.textContent).join(' ');assert.match(text,locale==='ko'?/가상 경기.*실제 경기 재현이 아닙니다/:/fictional sample.*not a real match replay/);assert.match(text,locale==='ko'?/연출용 점수/:/Illustrative score/);
 controls.children[0].events.click();for(let t=1;t<=18101;t+=100)d.tick(t);
 const result=section.children.find(n=>n.className==='md-sim-result');assert.match(result.textContent,/1 : 1/);assert.match(result.textContent,locale==='ko'?/종료/:/Finished/);assert.equal(d.queue.size,0);
 handle.destroy();d.tick(20000);assert.equal(section.removed,true);assert.equal(d.queue.size,0);return {result:result.textContent,counts:d.counts(),browserVerified:false};
});
check('Destroy a running animation cancels callbacks','no pending frames after destroy',()=>{const d=dom(false),container=d.doc.createElement('div'),h=simulation.mount(container,{model:'independent',probabilities:[1,0,0]},{rng:()=>0});container.children[0].children.find(n=>n.className==='md-sim-controls').children[0].events.click();assert.equal(d.queue.size,1);h.destroy();assert.equal(d.queue.size,0);d.tick(1000);assert.equal(d.queue.size,0);return d.counts();});
check('Reduced motion avoids scheduling frames including replay','zero requested animation frames',()=>{const d=dom(true),container=d.doc.createElement('div'),h=simulation.mount(container,{model:'independent',probabilities:[1,0,0]},{rng:()=>0});const section=container.children[0],buttons=section.children.find(n=>n.className==='md-sim-controls').children;buttons.forEach(b=>b.events.click());assert.equal(d.counts().requests,0);assert.match(section.children.find(n=>n.className==='md-sim-result').textContent,/1 : 0/);h.destroy();return d.counts();});
for(const filename of ['index.html','index.en.html'])check('Integration routing identity and cleanup '+filename,'641 keys consistent; match switch/team route/pagehide clean; same match preserves run',()=>{
 const html=fs.readFileSync(path.join(P,filename),'utf8'),extract=id=>JSON.parse(html.match(new RegExp('<script[^>]*id="'+id+'"[^>]*>([\\s\\S]*?)</script>'))[1]);
 const D=extract('data'),bundle=extract('prematch-predictions-v22');const fixtureMap=new Map(D.scheduled.map(m=>[m.id,m]));
 for(const p of bundle.predictions){const m=fixtureMap.get(p.match_key);assert.ok(m);assert.equal(m.home,p.home_team_key);assert.equal(m.away,p.away_team_key);assert.equal(m.date,p.date);assert.equal(m.league,p.league);}
 const d=dom(false),pane=d.doc.createElement('div');d.doc.documentElement={lang:filename.includes('.en.')?'en':'ko'};d.doc.getElementById=id=>id==='prematch-predictions-v22'?{textContent:JSON.stringify(bundle)}:pane;
 const events={},mounts=[];let destroyed=0;const chosen=fixtureMap.get(bundle.predictions[0].match_key);
 const context={document:d.doc,window:{addEventListener:(k,f)=>events[k]=f},V:'matches',L:chosen.league,selected:chosen,T:D.teams,renderMatches(){},render(){},MatchDeskSimulation:{mount(host,p,opts){mounts.push({p,opts});return {destroy(){destroyed++;}};}}};
 vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(S,'integration.js'),'utf8'),context);assert.equal(mounts.length,1);
 context.renderMatches();assert.equal(mounts.length,1);assert.equal(destroyed,0);
 context.V='team';context.render();assert.equal(destroyed,1);
 context.V='matches';context.selected={...chosen,id:chosen.id,date:'1900-01-01'};context.render();assert.equal(mounts.length,1);
 context.selected=chosen;context.render();assert.equal(mounts.length,2);
 const next=bundle.predictions.find(p=>p.match_key!==chosen.id&&p.league===chosen.league);context.selected=fixtureMap.get(next.match_key);context.renderMatches();assert.equal(mounts.length,3);assert.equal(destroyed,2);
 events.pagehide();assert.equal(destroyed,3);
 assert.deepEqual(Array.from(mounts[0].p.probabilities),[bundle.predictions[0].probabilities.home,bundle.predictions[0].probabilities.draw,bundle.predictions[0].probabilities.away]);
 return {matchedFixtures:bundle.predictions.length,mounts:mounts.length,destroyed,browserVerified:false};
});
const result={producer_id:'/root/independent_model_review',independent:true,browserVerified:false,passed:checks.filter(c=>c.status==='PASS').length,failed:checks.filter(c=>c.status==='FAIL').length,checks};
fs.writeFileSync(path.join(__dirname,'independent-ui-checks.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({passed:result.passed,failed:result.failed}));process.exitCode=result.failed?1:0;
