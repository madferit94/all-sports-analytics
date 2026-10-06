// Execute UI calculation and filter logic against a small DOM stub, not a browser.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const json=html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const code=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes=new Map();
class Node {
 constructor(){this.value='';this.dataset={};this.hidden=false;this.textContent='';this.classList={toggle(){}}}
 set innerHTML(s){this.html=s;if(s.includes('<option')){this.options=[...s.matchAll(/<option value="([^"]+)"/g)].map(m=>m[1]);this.value=this.options[0]||''}}
 get innerHTML(){return this.html||''}
 querySelectorAll(){return [...this.innerHTML.matchAll(/data-id="([^"]+)"/g)].map(m=>{let b=new Node();b.dataset.id=m[1];return b})}
}
const get=id=>{if(!nodes.has(id))nodes.set(id,new Node());return nodes.get(id)};
get('data').textContent=json;get('season').value='2026/27';
const nav=['matches','team','league'].map(view=>{let n=new Node();n.dataset.view=view;return n});
const context=vm.createContext({document:{getElementById:get,querySelectorAll(){return nav}},console});
vm.runInContext(code,context);
let checks=0;function test(name,fn){fn();checks++;console.log('PASS '+name)}
test('default EPL comparison displays Arsenal and previous results',()=>{assert(get('comparison').innerHTML.includes('Arsenal'));assert(get('fixtures').innerHTML.includes('aria-pressed="true"'));assert(get('trend').innerHTML.includes('<svg'))});
test('comparison excludes target day and averages match preserved data',()=>{assert(vm.runInContext('games(selected.home,null,selected.date).every(m=>m.date<selected.date)',context));assert.strictEqual(vm.runInContext('calc(selected.home,games(selected.home,null,selected.date).slice(-5)).n',context),5)});
test('league switch updates fixtures and comparison',()=>{get('league').value='La_liga';get('league').onchange();assert(vm.runInContext('L==="La_liga" && selected.league==="La_liga"',context));assert(get('comparison').innerHTML.includes(vm.runInContext('T[selected.home].name',context)))});
test('team and season selection uses matching actual records',()=>{nav[1].onclick();get('teamselect').value='understat:148';get('season').value='2025/26';get('season').onchange();assert(get('teamcontent').innerHTML.includes('Barcelona'));assert.strictEqual(vm.runInContext('calc("understat:148",games("understat:148","2025/26")).n',context),38)});
test('no-record season produces missing state',()=>{get('season').value='1900/01';get('season').onchange();assert(get('teamcontent').innerHTML.includes('자료가 없습니다'))});
test('league menu displays result-derived table',()=>{nav[2].onclick();assert(get('standings').innerHTML.includes('<table>'));assert(get('standings').innerHTML.includes('승점 조정 미반영'));assert.strictEqual(get('matches').hidden,true)});
test('all 56 mapped teams, no generated brand evidence',()=>{const data=JSON.parse(json);assert.strictEqual(Object.keys(data.teams).length,56);assert.strictEqual(Object.values(data.teams).filter(t=>t.colour_family_status==='OFFICIAL_FAMILY_CHECKED').length,6);assert(Object.values(data.teams).every(t=>/^#[0-9a-f]{6}$/i.test(t.primary)&&/^#[0-9a-f]{6}$/i.test(t.secondary)))});
test('visitor-facing content excludes designer menus and unavailable pitch',()=>{assert(!html.includes('사이트 디자인 기준'));assert(!html.includes('DESIGN-SYSTEM'));assert(!html.includes('슈팅 지도'));assert(html.includes('자료 기준'))});
fs.writeFileSync(__dirname+'/logic-check.json',JSON.stringify({kind:'Node VM with DOM stub; not browser rendering or accessibility verification',checks,failures:0},null,2));
console.log(checks+' logic checks passed; real browser UI unverified.');
