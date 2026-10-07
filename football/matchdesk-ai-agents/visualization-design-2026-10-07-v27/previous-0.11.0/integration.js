(function(){
  'use strict';
  const bundle=JSON.parse(document.getElementById('prematch-predictions-v22').textContent);
  const byKey=new Map(bundle.predictions.map(p=>[p.match_key,p]));
  const en=document.documentElement.lang==='en';
  let active=null,activeKey=null,host=null;
  function clear(){if(active)active.destroy();active=null;activeKey=null;if(host)host.remove();host=null;}
  function update(){
    if(V!=='matches'||!selected){clear();return;}
    if(activeKey===selected.id)return;
    clear();host=document.createElement('div');host.id='prediction-simulation-v22';document.getElementById('matches').appendChild(host);
    const p=byKey.get(selected.id);const msg=document.createElement('p');msg.className='note';host.appendChild(msg);
    if(!p){msg.textContent=en?'Prediction is not available for this match.':'이 경기의 모델 확률은 아직 준비되지 않았습니다.';return;}
    if(p.home_team_key!==selected.home||p.away_team_key!==selected.away||p.league!==L||p.date!==selected.date){msg.textContent=en?'The match identity does not match. Simulation is unavailable.':'경기 식별 정보가 일치하지 않아 시뮬레이션을 표시하지 않습니다.';return;}
    msg.textContent=en?'Selected model: logistic regression · Input records through '+p.training_last_date:'선정 모델: 로지스틱 · 예측 입력 자료 기준 '+p.training_last_date;
    const details=document.createElement('details'),summary=document.createElement('summary'),explanation=document.createElement('p');
    summary.textContent=en?'Model performance and inputs':'모델 성능과 사용 지표';explanation.className='note';
    explanation.textContent=en?"All-team logistic regression, 111 inputs and 1,518 training matches. 2025/26: 758 games, 48.15% accuracy, log loss 1.0229. Collected 2026/27: 119 games, 42.86% accuracy, log loss 1.0025. Uses attack, defence, pressure, shots, clearances, duels, passing and last-five results. No explicit home advantage, rest days or match-count input. Retrospective experiment; future performance unverified. Inputs use a fixed record snapshot.":"전체 팀 111입력 로지스틱. 1,518경기로 학습했습니다. 2025/26 758경기 정확도48.15%,확률오차1.0229. 2026/27수집119경기 정확도42.86%,확률오차1.0025. 공격·수비·압박·슈팅·클리어링·경합·패스의 경기별기록과 최근5경기결과를 사용합니다. 홈원정효과·휴식일·경기수는 직접입력하지 않습니다. 과거자료로 비교한 실험이며 미래성능은 미검증입니다. 예측입력은 자료기준일 스냅샷으로 고정되어 있습니다.";
    details.append(summary,explanation);host.appendChild(details);
    if(p.score_summary){const s=p.score_summary,preview=document.createElement('p');preview.className='md-sim-note';preview.textContent=(en?'4+ total goals: ':'총 4골 이상: ')+(s.four_plus_probability*100).toFixed(1)+'% · '+(en?'Most likely scores: ':'가능성 높은 점수: ')+s.top_scores.map(cell=>cell.home+':'+cell.away+' ('+(cell.probability*100).toFixed(1)+'%)').join(', ');host.appendChild(preview);}
    try{active=MatchDeskSimulation.mount(host,{model:p.model_id,status:p.status,home:p.home_team,away:p.away_team,probabilities:[p.probabilities.home,p.probabilities.draw,p.probabilities.away],scoreDistribution:p.scoreDistribution},{locale:en?'en':'ko',homeName:T[selected.home].name,awayName:T[selected.away].name,homeColor:T[selected.home].primary,awayColor:T[selected.away].primary});activeKey=selected.id;}catch(e){msg.textContent=en?'Invalid model probabilities. Simulation is unavailable.':'모델 확률 검증에 실패해 시뮬레이션을 표시하지 않습니다.';}
  }
  const baseMatches=renderMatches;renderMatches=function(){baseMatches();update();};
  const baseRender=render;render=function(){baseRender();update();};
  window.addEventListener('pagehide',clear);update();
})();
