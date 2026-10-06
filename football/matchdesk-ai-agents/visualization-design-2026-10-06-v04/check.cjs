// Calculation/navigation checks using a DOM stub; browser UI remains unverified.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(__dirname+'/index-v02.html','utf8');
const json=html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const data=JSON.parse(json),code=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes=new Map(),events={};
class Node {
 constructor(){this.value='';this.dataset={};this.hidden=false;this.textContent='';this.classList={toggle(){}}}
 set innerHTML(s){this.html=s;if(s.includes('<option')){this.options=[...s.matchAll(/<option value="([^"]+)"/g)].map(m=>m[1]);this.value=this.options[0]||''}}
 get innerHTML(){return this.html||''}
 querySelectorAll(selector){let attr=selector.includes('data-season')?'season':'id';return [...this.innerHTML.matchAll(new RegExp('data-'+attr+'="([^"]+)"','g'))].map(m=>{let n=new Node();n.dataset[attr]=m[1];return n})}
}
const get=id=>{if(!nodes.has(id))nodes.set(id,new Node());return nodes.get(id)};
get('data').textContent=json;get('season').value='2026/27';get('venue').value='all';get('resultfilter').value='all';
const nav=['matches','team','league'].map(view=>{let n=new Node();n.dataset.view=view;return n});
const context=vm.createContext({document:{getElementById:get,querySelectorAll(){return nav},addEventListener(name,fn){events[name]=fn}},window:{location:{hash:''},addEventListener(name,fn){events[name]=fn}},console});
vm.runInContext(code,context);
let checks=0;function test(name,fn){fn();checks++;console.log('PASS '+name)}
function run(code){return vm.runInContext(code,context)}
test('56 observed logo URLs inserted; no image downloads required',()=>{assert.strictEqual(Object.keys(data.teams).length,56);assert(Object.values(data.teams).every(t=>t.logo&&t.logo.startsWith('https://cdn.statmuse.com/')))});
test('logos are labelled links and include load-failure fallback',()=>{let b=run('badge("understat:83",true)');assert(b.includes('data-team="understat:83"'));assert(b.includes('aria-label="Arsenal 과거 기록 보기"'));assert(b.includes('<img'));assert(b.includes('nextElementSibling.hidden=false'));assert(b.includes('loading="lazy"'))});
test('fixture card keeps logo links outside analysis button',()=>{const buttons=[...get('fixtures').innerHTML.matchAll(/<button[^>]*>([\s\S]*?)<\/button>/g)];assert(buttons.length>0);assert(buttons.every(b=>!b[1].includes('<a')));assert(get('fixtures').innerHTML.includes('<article'));assert(get('comparison').innerHTML.includes('Arsenal'))});
test('delegated logo click opens exact team profile',()=>{let prevented=false;events.click({target:{closest(){return {dataset:{team:'understat:245'}}}},preventDefault(){prevented=true}});assert(prevented);assert.strictEqual(get('teamselect').value,'understat:245');assert(get('teamcontent').innerHTML.includes('Leeds'));assert.strictEqual(get('matches').hidden,true)});
test('cross-league team logo updates league and profile',()=>{run('openTeam("understat:148")');assert.strictEqual(get('league').value,'La_liga');assert.strictEqual(get('teamselect').value,'understat:148');assert(get('teamcontent').innerHTML.includes('Barcelona'))});
test('profile exposes all four seasons, records and season links',()=>{assert(['2023/24','2024/25','2025/26','2026/27'].every(s=>get('teamcontent').innerHTML.includes('data-season="'+s+'"')));assert(get('teamcontent').innerHTML.includes('경기당 승점'));assert(get('teamcontent').innerHTML.includes('홈'));assert(get('teamcontent').innerHTML.includes('원정'))});
test('season records independently sum raw score fields',()=>{run('openTeam("understat:83")');get('season').value='2023/24';get('season').onchange();const ms=data.completed.filter(m=>m.season==='2023/24'&&(m.home==='understat:83'||m.away==='understat:83'));let p=0,gf=0,ga=0;ms.forEach(m=>{let f=m.home==='understat:83'?m.hg:m.ag,a=m.home==='understat:83'?m.ag:m.hg;gf+=f;ga+=a;p+=f>a?3:f===a?1:0});let s=run('calc("understat:83",games("understat:83","2023/24"))');assert.strictEqual(s.n,38);assert.strictEqual(s.p,p);assert.strictEqual(s.gf,gf);assert.strictEqual(s.ga,ga);assert.strictEqual((get('teamcontent').innerHTML.match(/<small class="muted">202[34]-/g)||[]).length,38)});
test('venue filter exposes only 19 home games in completed season',()=>{get('venue').value='home';get('venue').onchange();let ms=run('filterHistory("understat:83",games("understat:83","2023/24"))');assert.strictEqual(ms.length,19);assert(ms.every(m=>m.home==='understat:83'));assert(get('teamcontent').innerHTML.includes('19 / 38경기'))});
test('win filter returns only actual winning results',()=>{get('resultfilter').value='win';get('resultfilter').onchange();let ms=run('filterHistory("understat:83",games("understat:83","2023/24"))');assert(ms.length>0);assert(ms.every(m=>m.hg>m.ag))});
test('empty season stays missing instead of invented zero season',()=>{get('season').value='1900/01';get('season').onchange();assert(get('teamcontent').innerHTML.includes('선택한 시즌의 리그 자료가 없습니다'));assert(get('teamcontent').innerHTML.includes('선택 조건의 경기가 없습니다'))});
test('direct team hash resolves exact club; unknown hash ignored',()=>{context.window.location.hash='#team=understat%3A150';events.hashchange();assert.strictEqual(get('teamselect').value,'understat:150');context.window.location.hash='#team=does-not-exist';events.hashchange();assert.strictEqual(get('teamselect').value,'understat:150')});
test('league table includes navigable team logos',()=>{nav[2].onclick();assert(get('standings').innerHTML.includes('data-team="understat:148"'));assert(get('standings').innerHTML.includes('승점 조정 미반영'))});
test('past comparison remains strictly before scheduled match',()=>{nav[0].onclick();assert(run('games(selected.home,null,selected.date).every(m=>m.date<selected.date)'));assert(get('trend').innerHTML.includes('<svg'))});
test('visitor screen contains no designer menu',()=>{assert(!html.includes('사이트 디자인 기준'));assert(!html.includes('DESIGN-SYSTEM'))});
fs.writeFileSync(__dirname+'/logic-check.json',JSON.stringify({method:'Node VM with DOM stub; not real browser or image rendering',checks,failures:0},null,2));
console.log(checks+' checks passed.');
