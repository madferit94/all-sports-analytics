'use strict';
// Independent reviewer: expectations below are recorded before executing assertions.
// Scope: original season totals, 47 metadata metrics / 10 recent metrics; HTML-embedded
// engine and UI execution in an isolated simulated DOM, not browser visual verification.
const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto');
const base=path.resolve(__dirname,'..'), enginePath=path.join(__dirname,'team-chart-engine.cjs');
const engine=require(enginePath),tests=[],issues=[];
const previousReportPath=path.join(__dirname,'reviewer-report.json');
const previousReport=fs.existsSync(previousReportPath)?JSON.parse(fs.readFileSync(previousReportPath,'utf8')):null;
const priorRuns=previousReport?[...(previousReport.prior_runs||[]),...(previousReport.summary.FAIL?[{observed_at:previousReport.observed_at,summary:previousReport.summary,issues:previousReport.issues,cause:'Reviewer expected zero counts for wholly missing score; corrected to null under missing-data requirement. This was a checker defect, not an app regression.'}]:[])]:[];
const expectation={season:'Four snapshots 2023/24..2026/27; raw totals preserved, percentage bars and paired aerial/duel stacked counts; missing remains null; current season ongoing.',recent:'Home/away orientation from completed match plus team detail; PPDA att/def, zero or absent denominator null; under four observations bars; WDL counts only observed finite scores.',filters:'Actual HTML selectedGames applies season, venue, result, date and recent bounds. Recent chart inherits that subset then chart window; season snapshot independent of match subset.',ui:'Actual embedded engine/UI source executes, data table accompanies chart, missing line point breaks connection, paired missing season says no data; no non-finite SVG dimensions.',unknown:'Browser appearance, keyboard, touch, external assets and user acceptance delegated to root; no model evaluation or final approval.'};
function check(name,expected,actual,detail={}){const pass=JSON.stringify(expected)===JSON.stringify(actual);tests.push({name,status:pass?'PASS':'FAIL',expected,actual,...detail});if(!pass)issues.push({name,expected,actual});}
function finite(v){return typeof v==='number'&&Number.isFinite(v)?v:null;}
function load(file){const html=fs.readFileSync(path.join(base,file),'utf8'),match=html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/);return {html,D:JSON.parse(match[1])};}
const files=['index.html','index.en.html'];
for(const file of files){
 const {html,D}=load(file),locale=file.includes('.en.')?'en':'ko',id='understat:83';
 const src=fs.readFileSync(enginePath,'utf8'),ui=fs.readFileSync(path.join(__dirname,'team-chart-ui.js'),'utf8');
 const norm=s=>s.replace(/\r\n/g,'\n').trim();
 check(file+' embeds engine',true,norm(html).includes(norm(src)));
 check(file+' embeds UI',true,norm(html).includes(norm(ui)));
 const ctx={window:{}};vm.createContext(ctx);vm.runInContext(src,ctx);const build=ctx.window.MatchDeskCharts.buildPlan;
 check(file+' metadata count',47,Object.keys(D.metric_meta).length);
 check(file+' recent count',10,Object.keys(engine.recentMeta).length);
 for(const key of Object.keys(D.metric_meta)){
  let count=0,mismatch=[];let sample;
  for(const team of Object.keys(D.teams)){
   const plan=build(D,team,[],key,locale),meta=D.metric_meta[key],pair=/^AER-/.test(key)?['AER-W','AER-L']:/^DUEL-/.test(key)?['DUEL-W','DUEL-L']:[key];
   const want=engine.seasons.map(s=>pair.map(k=>finite(D.snapshots[team+'|'+s]?.values[k])));
   const got=plan.rows.map(r=>r.values);count+=want.flat().length;
   if(JSON.stringify(want)!==JSON.stringify(got))mismatch.push(team);
   if(team===id)sample={team,expected:want,actual:got,type:plan.type,unit:plan.unit};
   const expectedType=pair.length===2?'stacked':meta.unit==='%'?'percent':'bars';
   if(plan.type!==expectedType||plan.scope!=='season'||!plan.rows[3].label.includes(locale==='en'?'ongoing':'진행 중'))mismatch.push(team+':type/scope/ongoing');
  }
  check(file+' season '+key,[],mismatch,{numeric_values_compared:count,sample});
 }
 const all=D.completed.filter(m=>m.home===id||m.away===id).sort((a,b)=>a.date.localeCompare(b.date)||a.id.localeCompare(b.id));
 const selected=all.slice(-10);
 for(const key of Object.keys(engine.recentMeta)){
  const expectedRows=selected.map(m=>{const h=m.home===id,d=D.match_detail[id+'|'+m.id]||{},gf=h?m.hg:m.ag,ga=h?m.ag:m.hg;
   switch(key){case 'goals':return [gf,ga];case 'deep':return [finite(d.deep),finite(d.deep_allowed)];case 'xg_for':return [h?m.hx:m.ax];case 'xg_against':return [h?m.ax:m.hx];case 'ppda':return [typeof d.ppda_att==='number'&&d.ppda_def>0?d.ppda_att/d.ppda_def:null];case 'ppda_allowed':return [typeof d.ppda_allowed_att==='number'&&d.ppda_allowed_def>0?d.ppda_allowed_att/d.ppda_allowed_def:null];case 'results':return [gf>ga?1:0,gf===ga?1:0,gf<ga?1:0];default:return [finite(d[key])];}});
  const expected=key==='results'?[expectedRows.reduce((s,r)=>s.map((v,j)=>v+r[j]),[0,0,0])]:expectedRows;
  check(file+' recent '+key,expected,build(D,id,selected,key,locale).rows.map(r=>r.values),{input_match_ids:selected.map(m=>m.id)});
  const expectedType=key==='results'?'stacked':['goals','deep'].includes(key)?'grouped':'line';
  check(file+' recent type '+key,expectedType,build(D,id,selected,key,locale).type);
 }
 check(file+' short xG bars','bars',build(D,id,selected.slice(0,3),'xg_for',locale).type);
 check(file+' four xG line','line',build(D,id,selected.slice(0,4),'xg_for',locale).type);
 for(const key of Object.keys(D.metric_meta))check(file+' promoted294 '+key,[[null],[null],[null]],build(D,'understat:294',[],key,locale).rows.slice(0,3).map(r=>[r.values.every(v=>v===null)?null:'non-null']));
 const fixture=structuredClone(D),m=selected[0];fixture.match_detail[id+'|'+m.id]={ppda_att:100,ppda_def:0,ppda_allowed_att:100,ppda_allowed_def:0,npxg_for:null};
 for(const key of ['ppda','ppda_allowed','npxg_for','deep'])check(file+' boundary '+key,[null],build(fixture,id,[m],key,locale).rows[0].values.slice(0,1));
 fixture.snapshots[id+'|2026/27'].values.SH=123;
 check(file+' raw total not per-game',123,build(fixture,id,selected.slice(0,1),'SH',locale).rows[3].values[0]);
 fixture.snapshots[id+'|2026/27'].values['POSS%']=null;
 check(file+' missing percentage',null,build(fixture,id,selected,'POSS%',locale).rows[3].values[0]);
 const missingScore={...m,hg:null,ag:null};
 const invalidResult=build(fixture,id,[missingScore],'results',locale);
 check(file+' missing score must not be draw',[null,null,null],invalidResult.rows[0].values);
 check(file+' missing score count',1,invalidResult.missingCount);
 const partialResults=build(fixture,id,[m,missingScore],'results',locale);
 const gf=m.home===id?m.hg:m.ag,ga=m.home===id?m.ag:m.hg;
 check(file+' mixed observed and missing result counts',[gf>ga?1:0,gf===ga?1:0,gf<ga?1:0],partialResults.rows[0].values);
 check(file+' empty results remain missing',[null,null,null],build(D,id,[],'results',locale).rows[0].values);
 check(file+' completed score finite',0,D.completed.filter(m=>finite(m.hg)===null||finite(m.ag)===null).length);
 const elements=new Map(),$=key=>{if(!elements.has(key))elements.set(key,{value:'',innerHTML:'',textContent:'',querySelectorAll:()=>[],focus(){},scrollIntoView(){}});return elements.get(key);};
 const sandbox={D,$,V:'none',colour:()=> '#123456',esc:s=>String(s).replace(/[&<>"']/g,'_'),document:{documentElement:{lang:locale}},updateTeam(){},openMetricHelp(){},MatchDeskCharts:ctx.window.MatchDeskCharts};vm.createContext(sandbox);
 for(const name of ['games','filterHistory','selectedGames']){const line=html.split('\n').find(l=>l.startsWith('function '+name+'('));if(!line)throw Error(name+' missing');vm.runInContext(line,sandbox);}
 sandbox.selectedGames=sandbox.selectedGames; // executed HTML functions above
 $('season').value='2026/27';$('venue').value='all';$('resultfilter').value='all';$('rangefilter').value='season';$('teamselect').value=id;
 const current=all.filter(m=>m.season==='2026/27');
 check(file+' current season filters',current.map(m=>m.id),Array.from(sandbox.selectedGames(id),m=>m.id));
 $('venue').value='home';$('resultfilter').value='win';
 const wins=current.filter(m=>m.home===id&&m.hg>m.ag);
 check(file+' home wins filters',wins.map(m=>m.id),Array.from(sandbox.selectedGames(id),m=>m.id));
 $('venue').value='all';$('resultfilter').value='all';$('rangefilter').value='custom';$('startdate').value='2026-09-01';$('enddate').value='2026-09-20';
 check(file+' date filters',current.filter(m=>m.date>='2026-09-01'&&m.date<='2026-09-20').map(m=>m.id),Array.from(sandbox.selectedGames(id),m=>m.id));
 $('startdate').value='2026-09-20';$('enddate').value='2026-09-01';check(file+' invalid date range',0,sandbox.selectedGames(id).length);
 $('rangefilter').value='5';check(file+' recent five filters',current.slice(-5).map(m=>m.id),Array.from(sandbox.selectedGames(id),m=>m.id));
 $('season').value='2025/26';$('rangefilter').value='10';check(file+' recent ten filters',all.filter(m=>m.season==='2025/26').slice(-10).map(m=>m.id),Array.from(sandbox.selectedGames(id),m=>m.id));
 $('season').value='2026/27';$('rangefilter').value='5';
 const exportUi=ui.replace(/\}\)\(\);\s*$/, 'globalThis.__reviewUi={chartSvg,mountTeamChart,choices};})();');vm.runInContext(exportUi,sandbox);sandbox.V='team';sandbox.__reviewUi.mountTeamChart();
 check(file+' rendered selected count',true,$('teamchart').innerHTML.includes(locale==='en'?`${Math.min(5,current.length)} recorded matches`:`${Math.min(5,current.length)}경기`));
 check(file+' rendered exact value table',true,$('teamchart').innerHTML.includes('<table>')&&$('teamchart').innerHTML.includes(locale==='en'?'View chart values':'차트 수치 보기'));
 sandbox.__reviewUi.choices.set(id,{group:'attack',key:'SH',window:'5'});sandbox.__reviewUi.mountTeamChart();
 check(file+' season scope warning',true,$('teamchart').innerHTML.includes(locale==='en'?'match filters do not apply':'경기 필터 미적용'));
 check(file+' season exact SH',true,$('teamchart').innerHTML.includes(`<td>${D.snapshots[id+'|2026/27'].values.SH}</td>`));
 sandbox.__reviewUi.choices.set(id,{group:'defence',key:'SH-BLK',window:'5'});sandbox.__reviewUi.mountTeamChart();
 check(file+' SH-BLK caution visible',true,$('teamchart').innerHTML.includes(D.metric_meta['SH-BLK'].description));
 const gapPlan={title:'isolated gap',type:'line',scope:'match',series:['xG'],rows:[1,2,null,4,5].map((v,i)=>({label:'2026-09-0'+i,values:[v]}))};
 const gapSvg=sandbox.__reviewUi.chartSvg(gapPlan,id);
 check(file+' missing line breaks',2,(gapSvg.match(/<polyline /g)||[]).length);
 check(file+' gap omits missing point',4,(gapSvg.match(/<circle /g)||[]).length);
 const svgs=Object.keys(D.metric_meta).map(key=>sandbox.__reviewUi.chartSvg(build(D,id,[],key,locale),id)).join('');
 check(file+' SVG finite geometry',false,/NaN|Infinity|undefined/.test(svgs));
 const missingStack=sandbox.__reviewUi.chartSvg(build(D,'understat:294',[],'AER-W',locale),'understat:294');
 check(file+' missing paired counts label',true,missingStack.includes(locale==='en'?'No data':'자료 없음'));
}
const counts={PASS:tests.filter(t=>t.status==='PASS').length,FAIL:tests.filter(t=>t.status==='FAIL').length};
const report={run_id:'team-chart-independent-review-2026-10-07-v31',match_key:'team-charts-all-metrics',agent_id:'reviewer',role:'reviewer',producer_id:'/root/chart_reviewer',status:counts.FAIL?'FAILED':'DONE',observed_at:new Date().toISOString(),summary:counts,expectation,execution_kind:'AI_NODE_EXECUTION_AND_SIMULATED_DOM',evidence:[{path:'reviewer-check.cjs',description:'Independent expected values and repeatable comparison code'}],inputs:files.map(file=>({path:file,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(base,file))).digest('hex')})),tests,issues,prior_runs:priorRuns,initial_static_finding:'Initial source used gf===ga without finite validation; null/null would count draw. Reported to root before tests; builder corrected source before first executable check. No initial-runtime reproduction claimed.',unverified:['Actual browser visual/keyboard/narrow-screen behavior delegated to root','User screen acceptance','Source-provider factual authenticity beyond stored data','Prediction model performance outside chart scope','Final approval is not issued by reviewer']};
fs.writeFileSync(path.join(__dirname,'reviewer-report.json'),JSON.stringify(report,null,2)+'\n');
const lines=['# 팀 지표 차트 독립 검증',`완료 범위: 저장 KO/EN HTML 내장 엔진·화면 코드를 Node와 격리된 가상 화면 요소에서 실행. 시즌 47종×56팀×4시즌 및 경기별 10종 대조. ${counts.PASS} PASS / ${counts.FAIL} FAIL.`, '', '## 실행 전 기대값',...Object.entries(expectation).map(([k,v])=>`- ${k}: ${v}`),'','## 실제 대조값',...tests.filter(t=>/recent |raw total|missing score|home wins|date filters|current season/.test(t.name)).map(t=>`- ${t.name}: ${t.status}; 기대 ${JSON.stringify(t.expected)} / 실제 ${JSON.stringify(t.actual)}`),'','## 발견과 조치',...issues.map(i=>`- ${i.name}: 기대 ${JSON.stringify(i.expected)} / 실제 ${JSON.stringify(i.actual)}. 공유 앱 코드는 수정하지 않고 상위 담당자에게 보고.`),'','## 근거 파일','- reviewer-check.cjs: 실행 전 기준과 재현 코드','- reviewer-report.json: 모든 기대값·실제값·원본 SHA256 및 실행 시점',`- 재현: 지정된 Node로 visualization-design-2026-10-07-v31/reviewer-check.cjs 실행`,'','## 미확인과 필요한 사용자 판단',...report.unverified.map(x=>'- '+x),'','검증 주체: /root/chart_reviewer, 작성자와 독립. 가상 화면 요소 실행은 실제 브라우저 화면 확인과 다릅니다. 최종 결재 아님.'];
fs.writeFileSync(path.join(__dirname,'reviewer-report.ko.md'),lines.join('\n')+'\n');
const additions=['','## 최초 발견과 후속 대조','- 최초 정적 검토: 득점 null/null을 gf===ga로 비교하여 무승부로 세는 조건을 상위 담당자에게 보고했습니다. 상위 작성자가 수정한 뒤 최초 자동 검사했으므로 이전 앱 오류의 실행 재현을 주장하지 않습니다.','- 최종 동일 결측 입력: 기대 [null,null,null] / 실제 [null,null,null], missingCount 기대 1 / 실제 1. 관찰 가능한 경기만 결과 집계.','- 검사기 최초 실패 2건: 기대 [0,0,0]이 결측값 0 대체 금지와 충돌했습니다. 검사기 기대값을 null로 정정하고 같은 입력으로 재실행했습니다. 이전 FAIL 기대·실제·원인은 JSON prior_runs에 보존했습니다.',`- 최종 결과: ${counts.PASS} PASS / ${counts.FAIL} FAIL, 종료 코드 ${counts.FAIL?1:0}.`,`- 시즌 원본 값 대조 수: ${tests.reduce((s,t)=>s+(t.numeric_values_compared||0),0)} (KO/EN 포함). 실제 제공처 재수집·사실 인증은 범위 밖.`];
fs.appendFileSync(path.join(__dirname,'reviewer-report.ko.md'),additions.join('\n')+'\n');
console.log(JSON.stringify({counts,issues,report:'visualization-design-2026-10-07-v31/reviewer-report.json'},null,2));
process.exitCode=counts.FAIL?1:0;
