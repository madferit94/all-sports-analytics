/* Natural-language shortcuts over recorded F1 data. No LLM/API and no arbitrary execution. */
(function(g){'use strict';
const aliases={1:['노리스','norris'],3:['페르스타펜','베르스타펜','verstappen','max'],5:['보르톨레토','bortoleto'],6:['하자르','hadjar'],10:['가슬리','gasly'],11:['페레즈','perez','pérez'],12:['안토넬리','antonelli'],14:['알론소','alonso'],16:['르클레르','leclerc'],18:['스트롤','stroll'],23:['알본','albon'],27:['휠켄베르크','훌켄베르크','hulkenberg','hülkenberg'],30:['로슨','lawson'],31:['오콘','ocon'],41:['린드블라드','lindblad'],43:['콜라핀토','colapinto'],44:['해밀턴','hamilton'],55:['사인츠','sainz'],63:['러셀','russell'],77:['보타스','bottas'],81:['피아스트리','piastri'],87:['베어먼','bearman']};
const definitions=[
 {id:'mean_stop',ko:'평균 정비 정차 시간',en:'Mean stationary stop',unit:'s',pattern:/정비\s*정차\s*시간|정차\s*시간|피트\s*스톱\s*시간|pit\s*stop\s*(?:time|duration)s?|stationary\s*(?:stop\s*)?(?:time|duration)s?/gi},
 {id:'mean_pit_lane',ko:'평균 피트레인 시간',en:'Mean pit-lane time',unit:'s',pattern:/피트\s*레인\s*시간|pit[ -]*lane\s*(?:time|duration)s?/gi},
 {id:'top_speed',ko:'최고 측정 속도',en:'Top recorded speed',unit:'km/h',pattern:/최고\s*(?:측정\s*)?속도|top\s*speed|maximum\s*speed/gi},
 {id:'points',ko:'획득 포인트',en:'Race points',unit:'',pattern:/획득\s*포인트|포인트|득점|points?/gi},
 {id:'final_position',ko:'최종 순위',en:'Final position',unit:'',pattern:/최종\s*순위|경기\s*결과|final\s*(?:position|rank)|race\s*results?/gi},
 {id:'win_probability',ko:'우승 확률',en:'Win probability',unit:'%',pattern:/우승\s*(?:확률|가능성)|win\s*probabilit(?:y|ies)/gi},
 {id:'laps',ko:'랩타임 변화',en:'Lap-time trend',unit:'s',pattern:/랩\s*타임(?:\s*변화)?|lap[ -]*times?(?:\s*trend)?/gi}
];
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function parse(question,race,prediction){
 if(typeof question!=='string'||!question.trim()||question.length>500)return {error:'question'};
 let text=question.toLowerCase().trim(),drivers=[];
 const roster=race.state==='completed'?(race.records?.drivers||[]):(prediction?.drivers||[]);
 for(const d of roster){const names=[d.full_name,d.name,...(aliases[d.driver_number]||[])].filter(Boolean).sort((a,b)=>b.length-a.length);let hit=false;for(const name of names){const q=name.toLowerCase();if(text.includes(q)){text=text.split(q).join(' ');hit=true;}}if(hit)drivers.push(d.driver_number);}
 const found=[];for(const def of definitions){def.pattern.lastIndex=0;if(def.pattern.test(text)){found.push(def);def.pattern.lastIndex=0;text=text.replace(def.pattern,' ');}}
 if(found.length!==1)return {error:'unsupported'};
 let metric=found[0].id;
 if(metric==='laps'&&/평균|average|mean/.test(text)){metric='mean_lap';text=text.replace(/평균|average|mean/g,' ');}
 // Reject unknown filters, dates, drivers and instructions instead of silently ignoring them.
 text=text.replace(/보여\s*줘(?:요)?|보여\s*주세요|그려\s*줘(?:요)?|그려\s*주세요|알려\s*줘(?:요)?|알려\s*주세요|시각화(?:해줘|해\s*주세요)?|비교(?:해줘|해\s*주세요)?|순위|차트|그래프|평균|전체|선수|드라이버|현재\s*경기|선택한\s*경기|변화|시간|show|please|compare|comparison|chart|graph|plot|rankings?|rank|average|mean|all|drivers|driver|current\s*race|this\s*race|trend|and|versus|vs\.?|the|me|of/gi,' ').replace(/[\s,?!·.&와과을를은는이가의]+/g,'');
 if(text)return {error:'unsupported'};
 if(race.state!=='completed'&&metric!=='win_probability')return {error:'future'};
 if(metric==='laps'&&!drivers.length)return {error:'drivers'};
 if(metric==='laps'&&drivers.length>4)return {error:'too_many'};
 return {metric,drivers,session_key:race.session.session_key};
}
function execute(plan,race,prediction){
 if(plan.error)return plan;
 const roster=race.state==='completed'?(race.records?.drivers||[]):(prediction?.drivers||[]),chosen=roster.filter(d=>!plan.drivers.length||plan.drivers.includes(d.driver_number));
 if(plan.metric==='laps')return {kind:'line',metric:'laps',unit:'s',rows:chosen.map(d=>({name:d.full_name||d.name,points:(race.records?.laps||[]).filter(x=>x.driver_number===d.driver_number&&Number.isFinite(x.lap_duration)&&x.lap_duration>0).sort((a,b)=>a.lap_number-b.lap_number).map(x=>({lap:x.lap_number,value:x.lap_duration}))}))};
 const rows=chosen.map(d=>{const m=g.MatchLabF1Metrics.calculate(race,d.driver_number,prediction).find(x=>x.key===plan.metric);return {name:d.full_name||d.name,value:typeof m?.value==='number'?m.value:null,coverage:m?.coverage}});
 const lower=['mean_lap','mean_stop','mean_pit_lane','final_position'].includes(plan.metric);
 rows.sort((a,b)=>a.value===null?1:b.value===null?-1:(a.value-b.value)*(lower?1:-1));
 return {kind:'bar',metric:plan.metric,unit:plan.metric==='mean_lap'?'s':definitions.find(x=>x.id===plan.metric)?.unit||'',rows};
}
function label(metric,en){if(metric==='mean_lap')return en?'Mean recorded lap time':'평균 기록 랩타임';const d=definitions.find(d=>d.id===metric);return d?.[en?'en':'ko']||metric;}
function draw(result,en){
 const colors=['#9b2624','#245789','#486524','#703b86'],fmt=v=>Number(v.toFixed(3)).toString(),title=label(result.metric,en);
 if(result.kind==='bar'){
  const valid=result.rows.filter(x=>x.value!==null);if(!valid.length)return `<p>${en?'No recorded values for this request.':'이 요청에 사용할 기록이 없습니다.'}</p>`;
  const scale=result.unit==='%'?100:1,max=Math.max(1,...valid.map(x=>x.value*scale));
  return `<h4>${esc(title)}</h4><div class="nl-bars">${result.rows.map(x=>`<div class="nl-bar-row"><span>${esc(x.name)}</span><div>${x.value===null?'—':`<strong>${fmt(x.value*scale)} ${esc(result.unit)}</strong><div class="nl-bar" aria-hidden="true"><i style="width:${Math.max(0,x.value*scale/max*100)}%"></i></div>`}${x.coverage?`<small>${en?'Recorded stops':'확보한 정차 기록'} ${x.coverage.recorded}/${x.coverage.total}${x.coverage.recorded<x.coverage.total?(en?' · partial average':' · 일부 기록 평균'):''}</small>`:''}</div></div>`).join('')}</div>`;
 }
 const points=result.rows.flatMap(r=>r.points);if(!points.length)return `<p>${en?'No valid lap times.':'유효한 랩타임 기록이 없습니다.'}</p>`;
 const min=Math.floor(Math.min(...points.map(x=>x.value))),max=Math.ceil(Math.max(...points.map(x=>x.value)))+1,last=Math.max(...points.map(x=>x.lap));
 let svg=`<svg viewBox="0 0 640 300" role="img" aria-label="${esc(title)}"><title>${esc(title)}</title>`;
 for(let i=0;i<5;i++){const y=20+i*55,v=max-(max-min)*i/4;svg+=`<line x1="60" x2="615" y1="${y}" y2="${y}" stroke="#c0ccad"/><text x="0" y="${y+5}" font-size="14">${v.toFixed(1)}s</text>`;}
 result.rows.forEach((r,i)=>{let prev=null;r.points.forEach(p=>{const x=60+(p.lap-1)/Math.max(1,last-1)*555,y=240-(p.value-min)/(max-min)*220;if(prev&&prev.lap+1===p.lap)svg+=`<line x1="${prev.x}" y1="${prev.y}" x2="${x}" y2="${y}" stroke="${colors[i]}" stroke-width="2" stroke-dasharray="${i?i*3+' 3':'none'}"/>`;svg+=`<circle cx="${x}" cy="${y}" r="2.5" fill="${colors[i]}"><title>${esc(r.name)} · ${p.lap}: ${p.value}s</title></circle>`;prev={x,y,lap:p.lap};});});
 svg+=`<text x="60" y="280" font-size="14">${en?'Lap':'랩'} 1</text><text x="560" y="280" font-size="14">${en?'Lap':'랩'} ${last}</text></svg>`;
 return `<h4>${esc(title)}</h4><p>${result.rows.map((r,i)=>`<span style="color:${colors[i]}">${i?'┄':'━'} ${esc(r.name)}</span>`).join(' · ')}</p><div class="nl-line" tabindex="0" aria-label="${en?'Scrollable lap chart':'좌우로 이동 가능한 랩타임 차트'}">${svg}</div><details><summary>${en?'Recorded values':'수치 보기'}</summary><div class="table-wrap"><table><thead><tr><th>${en?'Driver':'드라이버'}</th><th>${en?'Lap':'랩'}</th><th>s</th></tr></thead><tbody>${result.rows.flatMap(r=>r.points.map(p=>`<tr><td>${esc(r.name)}</td><td>${p.lap}</td><td>${p.value}</td></tr>`)).join('')}</tbody></table></div></details>`;
}
function mount(host,race,prediction,{locale='ko'}={}){
 const en=locale==='en',examples=race.state==='completed'?(en?['Compare Norris and Verstappen lap times','Rank pit stop times','Compare top speed']:['노리스와 페르스타펜 랩타임 비교','정비 정차 시간 순위','최고 속도 비교']):(en?['Win probability ranking']:['우승 확률 순위']);
 const errors={question:en?'Enter a question (up to 500 characters).':'질문을 500자 이내로 입력해 주세요.',unsupported:en?'This shortcut supports lap times, stop times, pit-lane times, top speed, race points, final position and win probability for the selected GP. Other races, teams and custom filters are not supported yet.':'선택한 GP의 랩타임·정차 시간·피트레인 시간·최고 속도·포인트·최종 순위·우승 확률을 지원합니다. 다른 경기·팀 단위·세부 조건은 아직 지원하지 않습니다.',future:en?'This GP has no completed records. Ask for win probability.':'아직 종료 기록이 없는 GP입니다. 우승 확률을 요청해 주세요.',drivers:en?'Name up to four drivers to plot lap times.':'랩타임 차트에 표시할 드라이버 이름을 입력해 주세요. 최대 4명까지 비교합니다.',too_many:en?'Compare up to four drivers.':'최대 4명까지 비교해 주세요.'};
 host.innerHTML=`<style>.nl-form{display:grid;gap:12px}.nl-form textarea{width:100%;max-width:100%;min-height:90px;padding:12px;font:16px/1.5 system-ui;resize:vertical;border:2px solid #162e37;background:#fffdf5;color:#162e37}.nl-examples{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.nl-examples button{white-space:normal;overflow-wrap:anywhere;max-width:100%}.nl-output{margin-top:20px;overflow-wrap:anywhere}.nl-bar-row{display:grid;grid-template-columns:minmax(100px,1fr) minmax(0,2fr);gap:12px;padding:10px 0;border-bottom:1px solid #c0ccad}.nl-bar-row>*{min-width:0;overflow-wrap:anywhere}.nl-bar-row small{display:block}.nl-bar{height:12px;background:#d6dfc7;margin:6px 0}.nl-bar i{display:block;height:100%;background:#245789}.nl-line{max-width:100%;overflow:auto}.nl-line svg{min-width:640px;display:block}.nl-status{min-height:24px}.nl-note{color:#52666d}</style><h3>${en?'Ask the data analyst':'자연어로 분석 요청'}</h3><p class="nl-note">${en?'Selected GP only · Saved records · No AI API call':'선택한 그랑프리 기준 · 저장된 기록 분석 · AI API 호출 없음'}</p><form class="nl-form"><label for="f1-question">${en?'What would you like to compare?':'어떤 기록을 비교할까요?'}</label><textarea id="f1-question" maxlength="500" placeholder="${esc(examples[0])}"></textarea><button type="submit">${en?'Create chart':'차트 만들기'}</button></form><div class="nl-examples">${examples.map(x=>`<button type="button" data-example="${esc(x)}">${esc(x)}</button>`).join('')}</div><p class="nl-status" role="status" aria-live="polite"></p><div class="nl-output"></div>`;
 const form=host.querySelector('form'),input=host.querySelector('textarea'),status=host.querySelector('.nl-status'),out=host.querySelector('.nl-output');
 function run(){out.replaceChildren();const plan=parse(input.value,race,prediction);if(plan.error){status.textContent=errors[plan.error];return}const result=execute(plan,race,prediction);out.innerHTML=draw(result,en);const note=['laps','mean_lap'].includes(plan.metric)?(en?'All recorded laps, including pit and Safety Car laps; not clean race pace.':'피트·세이프티카 랩도 포함한 기록입니다. 순수 주행 페이스와는 다릅니다.'):plan.metric==='win_probability'?(en?'Experimental saved model probabilities, not guaranteed results.':'저장된 실험 모델 확률이며 실제 결과를 보장하지 않습니다.'):(en?'Missing values are excluded. Lower stop/lap times are faster.':'없는 값은 계산에서 제외합니다. 정차·랩타임은 작을수록 빠릅니다.');status.textContent=(en?'Chart ready. ':'차트를 만들었습니다. ')+note;}
 form.onsubmit=e=>{e.preventDefault();run()};host.querySelectorAll('[data-example]').forEach(b=>b.onclick=()=>{input.value=b.dataset.example;run()});
 return {destroy(){host.replaceChildren()}};
}
g.MatchLabF1Natural={parse,execute,draw,mount};
})(typeof window==='undefined'?globalThis:window);

