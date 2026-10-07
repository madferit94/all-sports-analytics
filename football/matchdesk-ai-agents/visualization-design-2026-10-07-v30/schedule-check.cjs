const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..');
for(const f of ['index.html','index.en.html']){
 const h=fs.readFileSync(path.join(root,f),'utf8'),old=fs.readFileSync(path.join(__dirname,'previous-0.11.3',f),'utf8');
 const get=(s,id)=>JSON.parse(s.match(new RegExp('<script[^>]*id="'+id+'"[^>]*>([\\s\\S]*?)<\\/script>'))[1]);
 for(const id of ['data','prematch-predictions-v22'])assert.deepEqual(get(h,id),get(old,id));
 for(const m of h.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)){if(!m[0].includes('type="application/json"'))new vm.Script(m[1]);}
 const D=get(h,'data'),context=vm.createContext({D});vm.runInContext(h.match(/function upcomingSchedule\([^]*?\nfunction openScheduledPreview/)[0].replace(/\nfunction openScheduledPreview$/,''),context);
 for(const league of [...new Set(D.scheduled.map(m=>m.league))]){context.league=league;const items=vm.runInContext('upcomingSchedule(league)',context);assert(items.every(m=>m.league===league&&m.date>='2026-10-06'));assert(items.length>9);assert.equal(items.slice(0,3).length,3);assert.equal(items.slice(0,9).length,9);assert.equal(items.slice(0,items.length+6).length,items.length);}
 context.team='understat:294';context.league='EPL';const team=vm.runInContext('upcomingSchedule(league,team)',context);assert(team.length>9);assert(team.every(m=>m.home==='understat:294'||m.away==='understat:294'));assert.equal(team[3].id,'understat:31261');
}
console.log('PASS bilingual syntax, unchanged data/model, league/team schedules, 3→9 and exhausted slices, exact later fixture');