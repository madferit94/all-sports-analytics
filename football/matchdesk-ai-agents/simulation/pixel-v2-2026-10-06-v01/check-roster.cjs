'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),sim=require('./pixel-simulation.js');let checks=0;
function test(name,fn){fn();checks++;console.log('PASS '+name);}
const colors=['#cf3340','#4779d5'];
for(const progress of [0,.5,1])test('draws exactly 22 shirts at progress '+progress,()=>{const players=sim.rosterPositions(progress,colors),rects=[];const ctx={fillRect(x,y,w,h){rects.push({x,y,w,h,c:this.fillStyle});}};sim.drawRoster(ctx,players);const shirts=rects.filter(r=>r.w===7&&r.h===6);assert.equal(shirts.length,22);for(let t=0;t<2;t++){assert.equal(players.filter(p=>p.team===t).length,11);assert.equal(players.filter(p=>p.team===t&&p.role==='goalkeeper').length,1);assert.equal(shirts.filter(r=>r.c===colors[t]).length,10);}});
test('full animation sweep stays on pitch without overlapping players',()=>{for(let frame=0;frame<=1080;frame++){const roster=sim.rosterPositions(frame/1080,colors);for(const p of roster){assert.ok(p.x-5>=18&&p.x+6<=302);assert.ok(p.y-5>=35&&p.y+7<=162);}for(let a=0;a<22;a++)for(let b=a+1;b<22;b++){assert.ok(Math.abs(roster[a].x-roster[b].x)>=11||Math.abs(roster[a].y-roster[b].y)>=12,'overlap '+frame);}}});
test('goalkeepers have distinct kits even when team kits match defaults',()=>{const palette=['#F5C542','#BD72E8'];const roster=sim.rosterPositions(.3,palette),keepers=roster.filter(p=>p.role==='goalkeeper');assert.notEqual(keepers[0].shirt,keepers[1].shirt);keepers.forEach(p=>assert.ok(!palette.map(x=>x.toLowerCase()).includes(p.shirt)));});
test('invalid progress rejected',()=>{assert.throws(()=>sim.rosterPositions(-.1));assert.throws(()=>sim.rosterPositions(NaN));});
test('mount drawing at start middle and finish has ten outfield shirts and one keeper per team',()=>{
 let pending=null,shirts=[];const ctx=new Proxy({fillRect(x,y,w,h){if(w===320&&h===180)shirts=[];if(w===7&&h===6)shirts.push(this.fillStyle);}},{get:(t,k)=>t[k]||(()=>{})});
 const win={matchMedia:()=>({matches:false}),requestAnimationFrame:fn=>{pending=fn;return 1;},cancelAnimationFrame(){pending=null;}};
 const doc={defaultView:win,createElement:()=>({ownerDocument:doc,children:[],events:{},appendChild(c){this.children.push(c);},append(...cs){cs.forEach(c=>this.appendChild(c));},setAttribute(){},addEventListener(k,fn){this.events[k]=fn;},getContext:()=>ctx,remove(){}})};
 const container=doc.createElement(),handle=sim.mount(container,{model:'test-fixture',probabilities:[1,0,0]},{homeColor:colors[0],awayColor:colors[1],rng:()=>0});
 function assertShirts(){assert.equal(shirts.length,22);colors.forEach(c=>assert.equal(shirts.filter(x=>x===c).length,10));assert.equal(shirts.filter(x=>x==='#f5c542').length,1);assert.equal(shirts.filter(x=>x==='#bd72e8').length,1);}
 assertShirts();const play=container.children[0].children.find(n=>n.className==='md-sim-controls').children[0];play.events.click();let tick=pending;pending=null;tick(1);
 for(let i=1;i<=180;i++){tick=pending;pending=null;assert.ok(tick);tick(1+i*100);if(i===90||i===180)assertShirts();}handle.destroy();
});
const P=path.resolve(__dirname,'../..');
for(const file of ['index.html','index.en.html'])test(file+' original forecast and record payload unchanged',()=>{const now=fs.readFileSync(path.join(P,file),'utf8'),previous=fs.readFileSync(path.join(P,'visualization-design-2026-10-06-v22',file),'utf8');for(const id of ['data','prematch-predictions-v22']){const re=new RegExp('<script[^>]*id="'+id+'"[^>]*>([\\s\\S]*?)</script>');assert.equal(now.match(re)[1],previous.match(re)[1]);}});
test('DOM stub integration cleans animation on team and league transitions',()=>{
 const html=fs.readFileSync(path.join(P,'index.html'),'utf8'),bundle=JSON.parse(html.match(/<script id="prematch-predictions-v22" type="application\/json">([\s\S]*?)<\/script>/)[1]);
 let mounts=0,destroys=0;const host={appendChild(){},remove(){},textContent:''};const doc={documentElement:{lang:'ko'},createElement:()=>({append(){},appendChild(){},remove(){},className:'',textContent:''}),getElementById:id=>id==='prematch-predictions-v22'?{textContent:JSON.stringify(bundle)}:host};
 const context={document:doc,window:{addEventListener(){}},Map,MatchDeskSimulation:{mount(){mounts++;return{destroy(){destroys++;}};}},V:'matches',L:'EPL',selected:null,T:{},renderMatches(){},render(){}};
 function select(p){context.selected={id:p.match_key,home:p.home_team_key,away:p.away_team_key,date:p.date};context.L=p.league;context.T[p.home_team_key]={name:p.home_team,primary:colors[0]};context.T[p.away_team_key]={name:p.away_team,primary:colors[1]};}
 select(bundle.predictions.find(p=>p.league==='EPL'));vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(__dirname,'integration.js'),'utf8'),context);assert.equal(mounts,1);context.renderMatches();assert.equal(mounts,1);context.V='team';context.render();assert.equal(destroys,1);context.V='matches';select(bundle.predictions.find(p=>p.league==='La_liga'));context.renderMatches();assert.equal(mounts,2);context.selected=null;context.render();assert.equal(destroys,2);
});
console.log(JSON.stringify({checks,passed:checks,realBrowserVerified:false,animationFramesChecked:1081}));
