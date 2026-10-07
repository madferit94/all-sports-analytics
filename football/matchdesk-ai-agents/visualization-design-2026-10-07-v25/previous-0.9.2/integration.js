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
    msg.textContent=en?'Experimental model · not adopted for production · Records through '+p.training_last_date:'실험 모델 · 정식 채택 전 · 분석 자료 기준 '+p.training_last_date;
    const details=document.createElement('details'),summary=document.createElement('summary'),explanation=document.createElement('p');
    summary.textContent=en?'Model performance and inputs':'모델 성능과 사용 지표';explanation.className='note';
    explanation.textContent=en?'Final holdout 2025/26: 760 matches, accuracy 50.92% (home-pick baseline 45.79%). Ongoing 2026/27: 119 matches, 42.86% (baseline 41.18%); La Liga 43.48%, below baseline 44.93%. Attack uses goals, xG, non-penalty xG and deep completions; defence uses conceded counterparts. PPDA and opponent PPDA describe pressure, not pass accuracy. Form uses points from up to five matches within the current season. Previous-season means shrink toward league averages using eight-match weight; current-season means shrink toward that prior using eight-match weight; recent form shrinks toward the season mean using three-match weight. Missing previous-season history uses league averages; this does not establish promotion status. Passing totals are excluded because historical pre-match snapshots are unavailable; end-of-season totals would leak future information. These are fixed predictions from the available record cutoff, not live updates. Match dates follow the collected source and are not verified kickoffs.':'최종 검증 2025/26: 760경기 정확도 50.92%(홈 승 기준 45.79%). 진행 시즌 2026/27: 119경기 42.86%(기준 41.18%), 라리가 43.48%로 기준 44.93%보다 낮습니다. 공격은 득점·기대 득점·페널티 제외 기대 득점·깊은 지역 진입, 수비는 각 상대 허용 지표를 사용합니다. 압박 지표와 상대 압박 지표는 패스 성공률과 다릅니다. 흐름은 이번 시즌 내 최대 최근 5경기 승점을 사용합니다. 이전 시즌 평균을 리그 평균 8경기분으로 보정하고, 이번 시즌 평균을 그 이전 기록 8경기분으로 보정합니다. 최근 기록은 시즌 평균 3경기분으로 보정합니다. 이전 시즌 기록이 없으면 리그 평균을 사용하며 기록 부재만으로 승격 팀이라고 판단하지 않습니다. 패스 합계는 당시 경기 전 자료가 없어 제외했습니다. 시즌 최종 합계를 과거 경기에 넣으면 미래 정보가 섞이기 때문입니다. 현재 자료 기준으로 고정한 예측이며 실시간 갱신값이 아닙니다. 경기 날짜는 수집 출처 기준이며 공식 킥오프 확인값은 아닙니다.';
    details.append(summary,explanation);host.appendChild(details);
    try{active=MatchDeskSimulation.mount(host,{model:p.model_id,status:p.status,home:p.home_team,away:p.away_team,probabilities:[p.probabilities.home,p.probabilities.draw,p.probabilities.away]},{locale:en?'en':'ko',homeName:T[selected.home].name,awayName:T[selected.away].name,homeColor:T[selected.home].primary,awayColor:T[selected.away].primary});activeKey=selected.id;}catch(e){msg.textContent=en?'Invalid model probabilities. Simulation is unavailable.':'모델 확률 검증에 실패해 시뮬레이션을 표시하지 않습니다.';}
  }
  const baseMatches=renderMatches;renderMatches=function(){baseMatches();update();};
  const baseRender=render;render=function(){baseRender();update();};
  window.addEventListener('pagehide',clear);update();
})();
