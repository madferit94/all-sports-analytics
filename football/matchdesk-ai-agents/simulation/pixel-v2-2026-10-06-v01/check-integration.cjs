'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict'),sim=require('./pixel-simulation.js');
const P=path.resolve(__dirname,'../..');let checks=0;function test(name,fn){fn();checks++;console.log('PASS '+name);}
for(const file of ['index.html','index.en.html']){
 const html=fs.readFileSync(path.join(P,file),'utf8');
 const embedded=id=>JSON.parse(html.match(new RegExp('<script[^>]*id="'+id+'"[^>]*>([\\s\\S]*?)</script>'))[1]);
 const D=embedded('data'),bundle=embedded('prematch-predictions-v22');
 test(file+' 641 forecasts',()=>assert.equal(bundle.predictions.length,641));
 test(file+' all forecasts model validated and identity matched',()=>{const rows=new Map(D.scheduled.map(m=>[m.id,m]));for(const p of bundle.predictions){sim.validate({model:p.model_id,status:p.status,probabilities:[p.probabilities.home,p.probabilities.draw,p.probabilities.away]});const m=rows.get(p.match_key);assert.ok(m,p.match_key);assert.equal(m.home,p.home_team_key);assert.equal(m.away,p.away_team_key);assert.equal(m.date,p.date);assert.equal(m.league,p.league);}});
 test(file+' executable scripts parse',()=>{for(const match of html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)){if(!/application\/json/.test(match[1]))new vm.Script(match[2]);}});
 test(file+' canonical equals new snapshot',()=>assert.equal(html,fs.readFileSync(path.join(P,'visualization-design-2026-10-06-v23',file),'utf8')));
}
function fakeDOM(reduced){
 let callback=null,cancelled=0;const win={matchMedia:()=>({matches:reduced}),requestAnimationFrame:fn=>{callback=fn;return 1;},cancelAnimationFrame:()=>{cancelled++;}};
 const ctx=new Proxy({},{get:(target,key)=>target[key]||(()=>{})});
 const doc={defaultView:win,createElement:tag=>{const n={tag,children:[],events:{},attributes:{},ownerDocument:doc,textContent:'',appendChild(child){this.children.push(child);return child;},append(...nodes){nodes.forEach(c=>this.appendChild(c));},setAttribute(k,v){this.attributes[k]=v;},addEventListener(k,fn){this.events[k]=fn;},remove(){this.removed=true;},getContext:()=>ctx};return n;}};
 return {container:doc.createElement('div'),tick:t=>{if(callback){const f=callback;callback=null;f(t);}},get cancelled(){return cancelled;}};
}
const p={model:'deterministic-test-fixture',status:'EXPERIMENTAL_NOT_ADOPTED',home:'A',away:'B',probabilities:[1,0,0]};
test('DOM stub controls and cleanup (not browser)',()=>{const f=fakeDOM(false),handle=sim.mount(f.container,p,{locale:'en',rng:()=>0});const section=f.container.children[0],controls=section.children.find(n=>n.className==='md-sim-controls'),play=controls.children[0];play.events.click();assert.equal(play.textContent,'Pause');f.tick(10);f.tick(100);play.events.click();assert.equal(play.textContent,'Play');handle.destroy();assert.equal(section.removed,true);assert.ok(f.cancelled>=2);});
test('DOM stub reduced motion final result (not browser)',()=>{const f=fakeDOM(true),handle=sim.mount(f.container,p,{locale:'ko',rng:()=>0});assert.deepEqual(handle.sample().score,[1,0]);const section=f.container.children[0],result=section.children.find(n=>n.className==='md-sim-result');assert.match(result.textContent,/1 : 0/);assert.match(result.textContent,/종료/);handle.destroy();});
console.log(JSON.stringify({checks,passed:checks,realBrowserVerified:false,domStubChecks:2}));
