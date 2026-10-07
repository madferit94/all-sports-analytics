(function(){
'use strict';
const chartEN=document.documentElement.lang==='en',choices=new Map(),groupNames={recent:chartEN?'Match trends':'경기별 흐름',attack:chartEN?'Attack':'공격',defence:chartEN?'Defence':'수비',passing:chartEN?'Passing':'패스·점유',duels:chartEN?'Duels':'경합',discipline:chartEN?'Discipline':'반칙·징계'};
const nfmt=v=>v===null?(chartEN?'No data':'자료 없음'):Number.isInteger(v)?String(v):v.toFixed(2);
function chartSvg(plan,id){
 const colors=[colour(id),'#a04d36','#a47700'],rows=plan.rows,w=600,h=270,left=55,right=20,top=20,bottom=70,plotW=w-left-right,plotH=h-top-bottom;
 const values=rows.flatMap(r=>r.values).filter(v=>v!==null),max=plan.type==='percent'?100:Math.max(1,...(plan.type==='stacked'?rows.filter(r=>r.values.every(v=>v!==null)).map(r=>r.values.reduce((a,b)=>a+b,0)):values))*1.1;
 let out=`<svg class="team-metric-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(plan.title)}"><title>${esc(plan.title)}</title>`;
 if(plan.type==='stacked'||plan.type==='percent'){
  const height=Math.max(240,rows.length*76+40);out=`<svg class="team-metric-chart" viewBox="0 0 600 ${height}" role="img" aria-label="${esc(plan.title)}"><title>${esc(plan.title)}</title>`;
  rows.forEach((r,i)=>{const y=24+i*76;out+=`<text x="10" y="${y}" font-size="20">${esc(r.label)}</text>`;
   if(r.values.some(v=>v===null)){out+=`<text x="20" y="${y+34}" font-size="20">${chartEN?'No data':'자료 없음'}</text>`;return;}
   let x=20;out+=`<rect x="20" y="${y+10}" width="400" height="22" fill="#dde3ce"/>`;
   r.values.forEach((v,j)=>{const width=Math.max(0,v/max*400);out+=`<rect x="${x}" y="${y+10}" width="${width}" height="22" fill="${colors[j]}" stroke="#fff9e9"><title>${esc(plan.series[j])}: ${nfmt(v)}</title></rect>`;x+=width;});out+=`<text x="435" y="${y+27}" font-size="18">${esc(r.values.map(nfmt).join(' / '))}${plan.type==='percent'?'%':''}</text>`;
  });
  if(plan.type==='percent')out+=`<text x="20" y="${height-5}" font-size="18">0%</text><text x="380" y="${height-5}" font-size="18">100%</text>`;
 }else{
  [0,max/2,max].forEach(v=>{const y=top+plotH-v/max*plotH;out+=`<line x1="${left}" x2="${w-right}" y1="${y}" y2="${y}" stroke="#d5dece"/><text x="5" y="${y+4}" font-size="18">${nfmt(v)}</text>`;});
  const bw=plotW/Math.max(1,rows.length),x=i=>left+bw*(i+.5),y=v=>top+plotH-v/max*plotH;
  plan.series.forEach((name,j)=>{
   if(plan.type==='line'){
    let points=[];function flush(){if(points.length>1)out+=`<polyline points="${points.join(' ')}" fill="none" stroke="${colors[j]}" stroke-width="3"/>`;points=[];}
    rows.forEach((r,i)=>{const v=r.values[j];if(v===null){flush();return;}points.push(`${x(i)},${y(v)}`);out+=`<circle cx="${x(i)}" cy="${y(v)}" r="4" fill="${colors[j]}"><title>${esc(r.label+' '+r.opponent)}: ${nfmt(v)}</title></circle>`;});flush();
   }else rows.forEach((r,i)=>{const v=r.values[j];if(v===null)return;const width=Math.min(45,bw*.65/plan.series.length),xx=x(i)+(j-plan.series.length/2)*width;out+=`<rect x="${xx}" y="${y(v)}" width="${Math.max(1,width-2)}" height="${plotH-(y(v)-top)}" fill="${colors[j]}"><title>${esc(r.label+' '+name)}: ${nfmt(v)}</title></rect>`;});
  });
  rows.forEach((r,i)=>{if(rows.length<=10||i===0||i===rows.length-1||i%Math.ceil(rows.length/7)===0)out+=`<text x="${x(i)}" y="${top+plotH+23}" text-anchor="middle" font-size="17">${esc(plan.scope==='match'?r.label.slice(5):r.label.slice(0,7))}</text>`;if(r.values.every(v=>v===null))out+=`<text x="${x(i)}" y="${top+plotH-8}" text-anchor="middle" font-size="18">—</text>`;});
 }
 return out+'</svg>';
}
function mountTeamChart(){
 const host=$('teamchart');if(!host||V!=='team')return;const id=$('teamselect').value,state=choices.get(id)||{group:'recent',key:'xg_for',window:'5'};choices.set(id,state);
 const keys=state.group==='recent'?Object.keys(MatchDeskCharts.recentMeta):Object.keys(D.metric_meta).filter(k=>D.metric_meta[k].category===state.group);if(!keys.includes(state.key))state.key=keys[0];
 const label=k=>MatchDeskCharts.recentMeta[k]?.[chartEN?1:0]||D.metric_meta[k].label;
 let matches=selectedGames(id);if(state.window!=='all')matches=matches.slice(-Number(state.window));const plan=MatchDeskCharts.buildPlan(D,id,matches,state.key,chartEN?'en':'ko');
 const typeNames=chartEN?{line:'Trend line',bars:'Bar comparison',grouped:'Grouped bars',stacked:'Stacked counts',percent:'Percentage bars'}:{line:'추이선',bars:'비교 막대',grouped:'나란히 비교 막대',stacked:'구성별 누적 막대',percent:'비율 막대'};
 const scope=plan.scope==='match'?(chartEN?'Uses the team filters above. '+matches.length+' recorded matches.':'위 팀 필터 적용 · '+matches.length+'경기'):(chartEN?'Full-season snapshots; match filters do not apply. 2026/27 is ongoing.':'시즌 전체 통계 · 경기 필터 미적용 · 2026/27 진행 중');
 host.innerHTML=`<h3>${chartEN?'Explore team metrics':'팀 지표 시각화'}</h3><div class="chart-groups" role="group" aria-label="${chartEN?'Metric categories':'지표 분류'}">${Object.entries(groupNames).map(([g,name])=>`<button type="button" data-chart-group="${g}" aria-pressed="${g===state.group}">${name}</button>`).join('')}</div><div class="chart-controls"><label>${chartEN?'Metric':'시각화 지표'}<select id="teamchartmetric">${keys.map(k=>`<option value="${esc(k)}" ${k===state.key?'selected':''}>${esc(label(k))}</option>`).join('')}</select></label>${plan.scope==='match'?`<label>${chartEN?'Chart range':'차트 경기 범위'}<select id="teamchartwindow"><option value="5" ${state.window==='5'?'selected':''}>${chartEN?'Last 5':'최근 5경기'}</option><option value="10" ${state.window==='10'?'selected':''}>${chartEN?'Last 10':'최근 10경기'}</option><option value="all" ${state.window==='all'?'selected':''}>${chartEN?'All filtered matches':'필터 적용 전체 경기'}</option></select></label>`:''}</div><h4>${esc(plan.title)}</h4><p class="chart-scope">${scope}${plan.missingCount?' · '+(chartEN?'Missing results excluded: ':'결과 누락 제외: ')+plan.missingCount:''}</p><div class="chart-legend">${plan.series.map((name,i)=>`<span><i style="background:${[colour(id),'#a04d36','#a47700'][i]}"></i>${esc(name)}</span>`).join('')}</div>${!plan.rows.length||plan.rows.every(r=>r.values.every(v=>v===null))?`<p>${chartEN?'No data for this selection.':'선택 항목의 자료가 없습니다.'}</p>`:chartSvg(plan,id)}<p class="chart-scope">${typeNames[plan.type]} · ${esc(plan.unit)}${state.key.startsWith('ppda')?(chartEN?' · Lower values generally indicate stronger pressure.':' · 낮을수록 강한 압박 경향'):''}${plan.scope==='match'&&matches.length?' · '+matches[0].date+' ~ '+matches[matches.length-1].date:''}</p>${state.key==='SH-BLK'?`<p class="chart-scope">${esc(plan.description)}</p>`:''}<details><summary>${chartEN?'View chart values':'차트 수치 보기'}</summary><div class="tablewrap"><table><thead><tr><th>${chartEN?'Date / season':'날짜 / 시즌'}</th>${plan.series.map(s=>`<th>${esc(s)}</th>`).join('')}</tr></thead><tbody>${plan.rows.map(r=>`<tr><td>${esc(r.label)}${r.opponent?'<br>'+esc(r.opponent):''}</td>${r.values.map(v=>`<td>${nfmt(v)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></details>`;
 $('teamchartmetric').onchange=event=>{state.key=event.target.value;mountTeamChart();};if($('teamchartwindow'))$('teamchartwindow').onchange=event=>{state.window=event.target.value;mountTeamChart();};
 host.querySelectorAll('[data-chart-group]').forEach(b=>b.onclick=()=>{state.group=b.dataset.chartGroup;mountTeamChart();});
}
const baseUpdateTeam=updateTeam;updateTeam=function(){baseUpdateTeam();mountTeamChart();};
const baseMetricHelp=openMetricHelp;openMetricHelp=function(code,trigger){baseMetricHelp(code,trigger);$('metricchartjump')?.remove();if(V!=='team'||$('metricpopover').hidden)return;const raw=code.replace('detail:',''),key=raw==='deep_allowed'?'deep':raw;if(!MatchDeskCharts.recentMeta[key]&&!D.metric_meta[key])return;const button=document.createElement('button');button.id='metricchartjump';button.type='button';button.className='schedule-more';button.textContent=chartEN?'Visualize this metric':'이 지표 시각화 보기';button.onclick=()=>{const id=$('teamselect').value,state=choices.get(id)||{window:'5'};state.key=key;state.group=MatchDeskCharts.recentMeta[key]?'recent':D.metric_meta[key].category;choices.set(id,state);closeMetricHelp(false);mountTeamChart();$('teamchart').scrollIntoView({block:'center',behavior:'auto'});$('teamchartmetric').focus({preventScroll:true});};$('metricpopover').appendChild(button);const pop=$('metricpopover'),height=pop.getBoundingClientRect().height;pop.style.top=Math.max(12,Math.min(trigger.getBoundingClientRect().bottom+8,window.innerHeight-height-12))+'px';};
mountTeamChart();
})();
