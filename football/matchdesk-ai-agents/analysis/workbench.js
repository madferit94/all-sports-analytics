// Adapter-driven workbench. All labels and data are supplied by the version builder.
const recordAnalyst=MatchDeskAnalysis.create(D);
const analysisRenderers=new Map();
function registerAnalysisService({name,parse,execute,render}){if(typeof render!=='function')throw new TypeError('Renderer required');recordAnalyst.register(name,execute,parse);analysisRenderers.set(name,render)}
let analystPrevious=null;
function analystMessage(key){return analystText[key]||analystText.unsupported}
function analystDefaults(){return {league:L,team:$('teamselect').value||(L==='EPL'?'understat:83':'understat:148'),season:$('season').value||'2026/27'}}
function renderAnalysis(result){
 const output=$('analystresult');
 if(analysisRenderers.has(result.tool)){analysisRenderers.get(result.tool)(result,output);$('analyststatus').textContent=analystText.done;return}
 if(result.status!=='ok'){
  $('analyststatus').textContent=result.status==='empty'?analystText.empty:result.reason==='empty'?analystText.unsupported:analystMessage(result.reason);
  output.innerHTML='';return;
 }
 const plan=result.plan,metric=MatchDeskAnalysis.metrics[result.metric][analystLanguage];
 const criterion=[plan.league==='EPL'?'Premier League':'LaLiga',plan.season,plan.last?analystText.last.replace('{n}',plan.last):analystText.full,plan.tool==='venue'?analystText.split:analystText[plan.venue],result.metric==='w'?'%':plan.perMatch?analystText.average:analystText.total].join(' · ');
 const labels=result.rows.map(r=>r.label==='home'?analystText.home:r.label==='away'?analystText.away:r.label);
 const max=Math.max(1,...result.rows.map(r=>Math.max(r.value||0,r.actual||0)));
 const chart=result.rows.map((r,i)=>`<div class="analystbar"><span>${esc(labels[i])}</span><div><div class="analysttrack"><span style="width:${(r.value||0)/max*100}%"></span></div>${r.actual!==undefined?`<div class="analysttrack actual"><span style="width:${r.actual/max*100}%"></span></div>`:''}</div><strong>${r.value===null?'—':r.value.toFixed(2)}${result.unit}${r.actual!==undefined?' / '+r.actual:''}</strong></div>`).join('');
 const rows=result.rows.map((r,i)=>`<tr><td>${r.id&&T[r.id]?teamName(r.id):esc(labels[i])}${r.opponent?'<br><small>'+esc(r.opponent)+'</small>':''}</td><td>${r.n}</td><td>${r.value===null?'—':r.value.toFixed(2)}${result.unit}</td>${r.actual!==undefined?'<td>'+r.actual+'</td>':''}</tr>`).join('');
 const actual=result.rows.some(r=>r.actual!==undefined);
 output.innerHTML=`<h3>${esc(metric)}${actual?' / '+esc(analystText.actual):''}</h3><p class="muted">${esc(criterion)}</p><p>${esc(analystText.through)} ${result.datasetThrough} · ${esc(analystText.local)}</p>${actual?`<p class="analystlegend">${esc(analystText.series)}</p>`:''}<div class="analystchart" role="img" aria-label="${esc(metric+' · '+analystText.tableBelow)}">${chart}</div><div class="tablewrap"><table><thead><tr><th>${esc(analystText.item)}</th><th>${esc(analystText.matches)}</th><th>${esc(metric)}</th>${actual?'<th>'+esc(analystText.actual)+'</th>':''}</tr></thead><tbody>${rows}</tbody></table></div><details><summary>${esc(analystText.proof)}</summary><p>${esc(analystText.execution)}</p><p>${esc(analystText.formula)}: <code>${esc(result.formula)}</code></p><p>${esc(analystText.scopeNote)}</p><pre>${esc(JSON.stringify({tool:plan.tool,teams:plan.teams,league:plan.league,season:plan.season,last:plan.last,venue:plan.venue,metric:plan.metric,perMatch:plan.perMatch,verification:result.verification},null,2))}</pre></details>`;
 $('analyststatus').textContent=analystText.done;
}
function submitAnalysis(question){
 $('analyststatus').textContent=analystText.running;
 const plan=recordAnalyst.parse(question,analystDefaults(),analystPrevious);
 const result=recordAnalyst.execute(plan);
 if(result.status==='ok')analystPrevious=plan;
 renderAnalysis(result);return result;
}
$('analystform').onsubmit=event=>{event.preventDefault();submitAnalysis($('analystquery').value)};
$('analystexamples').querySelectorAll('button').forEach(button=>button.onclick=()=>{$('analystquery').value=button.dataset.id;submitAnalysis(button.dataset.id)});
