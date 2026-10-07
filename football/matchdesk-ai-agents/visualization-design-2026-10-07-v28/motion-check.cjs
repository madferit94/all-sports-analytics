const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const p=path.resolve(__dirname,'..'),api=require(path.join(p,'simulation/pixel-v2-2026-10-06-v01/pixel-simulation.js'));
const evidence=[];
for(const goals of [[],[0],[1],[0,1,0,0],Array.from({length:12},(_,i)=>i%2)]){
 let previous,maxBallStep=0,maxPlayerStep=0;const xs=Array.from({length:22},()=>[]),phases=new Set();let goalFrames=0;
 for(let i=0;i<=12000;i++){
  const scene=api.matchFrame(i/12000,['#cf3340','#4779d5'],goals);assert.equal(scene.players.length,22);assert.equal(scene.players.filter(p=>p.team===0).length,11);assert.equal(scene.players.filter(p=>p.role==='goalkeeper').length,2);
  assert(Number.isFinite(scene.ball.x)&&Number.isFinite(scene.ball.y));assert(scene.ball.x>=14&&scene.ball.x<=306);assert(scene.ball.y>=35&&scene.ball.y<=163);
  scene.players.forEach((p,j)=>{assert(p.x>=23&&p.x<=297&&p.y>=43&&p.y<=153);xs[j].push(p.x);});
  if(previous){maxBallStep=Math.max(maxBallStep,Math.hypot(scene.ball.x-previous.ball.x,scene.ball.y-previous.ball.y));scene.players.forEach((p,j)=>{maxPlayerStep=Math.max(maxPlayerStep,Math.hypot(p.x-previous.players[j].x,p.y-previous.players[j].y));});}
  phases.add(scene.phase);if(scene.goal)goalFrames++;previous=scene;
 }
 assert(maxBallStep<3,`ball teleport ${maxBallStep}`);assert(maxPlayerStep<3,`player teleport ${maxPlayerStep}`);
 const travel=xs.map(x=>Math.max(...x)-Math.min(...x));assert(travel.filter((_,i)=>i%11!==0).every(x=>x>25));
 assert.deepEqual(previous.score,[goals.filter(x=>x===0).length,goals.filter(x=>x===1).length]);assert(goals.length?goalFrames>0:goalFrames===0);
 evidence.push({goals,frames:12001,maxBallStep,maxPlayerStep,minOutfieldTravel:Math.min(...travel.filter((_,i)=>i%11!==0)),phases:[...phases],goalFrames});
}
assert.throws(()=>api.matchFrame(.5,null,[2]));assert.throws(()=>api.matchFrame(2,null,[]));
for(const f of ['index.html','index.en.html']){
 const h=fs.readFileSync(path.join(p,f),'utf8'),old=fs.readFileSync(path.join(__dirname,'previous-0.11.1',f),'utf8');
 for(const id of ['data','prematch-predictions-v22']){const pattern=new RegExp('<script[^>]*id="'+id+'"[^>]*>([\\s\\S]*?)<\\/script>');assert.deepEqual(JSON.parse(h.match(pattern)[1]),JSON.parse(old.match(pattern)[1]));}
 assert(!h.includes('Score sampled from a learned goal distribution; not a guaranteed result.'));assert(!h.includes('학습한 득점 분포에서 뽑은 점수이며, 확정 결과가 아닙니다.'));assert(!h.includes('foot.textContent'));
 const scripts=[...h.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)];for(const m of scripts){if(m[0].startsWith('<script type="application/json"')||m[0].includes('type="application/json"'))continue;new (require('node:vm').Script)(m[1]);}
}
fs.writeFileSync(path.join(__dirname,'motion-verification.json'),JSON.stringify({status:'PASS',evidence,checks:['22 players','11 per team','continuous ground ball','continuous players','20 outfield players travel >25px','goal overlay','final scores','invalid inputs','KO/EN footer removed','model and data unchanged','inline syntax']},null,2));console.log(JSON.stringify({status:'PASS',evidence}));