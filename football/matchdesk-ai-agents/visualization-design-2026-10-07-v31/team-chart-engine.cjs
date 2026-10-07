(function(root){
'use strict';
const recentMeta={xg_for:['기대 득점','Expected goals','line'],xg_against:['기대 실점','Expected goals conceded','line'],goals:['득점·실점','Goals scored / conceded','grouped'],deep:['위험 지역 패스 성공·허용','Deep completions / allowed','grouped'],npxg_for:['페널티 제외 기대 득점','Non-penalty xG','line'],npxg_against:['페널티 제외 기대 실점','Non-penalty xG conceded','line'],expected_points:['기대 승점','Expected points','line'],ppda:['압박: 수비 행동당 허용 패스','Pressure: PPDA','line'],ppda_allowed:['상대 압박: 수비 행동당 허용 패스','Opponent pressure: PPDA','line'],results:['승·무·패 구성','Win / draw / loss mix','stacked']};
const seasons=['2023/24','2024/25','2025/26','2026/27'];
const finite=x=>typeof x==='number'&&Number.isFinite(x)?x:null;
const quotient=(a,b)=>finite(a)!==null&&finite(b)!==null&&b>0?a/b:null;
function buildPlan(data,id,matches,key,locale){
 const en=locale==='en',labels=key==='goals'?(en?['Goals scored','Goals conceded']:['득점','실점']):(en?['Completed','Allowed']:['성공','허용']);
 if(recentMeta[key]){
  const meta=recentMeta[key],rows=matches.map(m=>{const home=m.home===id,detail=data.match_detail[id+'|'+m.id]||{},gf=home?m.hg:m.ag,ga=home?m.ag:m.hg;let values;
   if(key==='goals')values=[finite(gf),finite(ga)];else if(key==='deep')values=[finite(detail.deep),finite(detail.deep_allowed)];else if(key==='results')values=finite(gf)===null||finite(ga)===null?[null,null,null]:[gf>ga?1:0,gf===ga?1:0,gf<ga?1:0];else if(key==='xg_for')values=[finite(home?m.hx:m.ax)];else if(key==='xg_against')values=[finite(home?m.ax:m.hx)];else if(key==='ppda')values=[quotient(detail.ppda_att,detail.ppda_def)];else if(key==='ppda_allowed')values=[quotient(detail.ppda_allowed_att,detail.ppda_allowed_def)];else values=[finite(detail[key])];
   return {label:m.date,opponent:data.teams[home?m.away:m.home]?.name||'',values};});
  if(key==='results')return {title:meta[en?1:0],type:'stacked',scope:'match',unit:en?'matches':'경기',series:en?['Wins','Draws','Losses']:['승리','무승부','패배'],rows:[{label:en?'Selected matches':'선택 경기',values:[0,1,2].map(i=>rows.some(r=>r.values[i]!==null)?rows.reduce((sum,r)=>sum+(r.values[i]||0),0):null)}],matchCount:matches.length,missingCount:rows.filter(r=>r.values.some(v=>v===null)).length};
  return {title:meta[en?1:0],type:meta[2]==='line'&&rows.length<4?'bars':meta[2],scope:'match',unit:en?'per match':'경기별',series:meta[2]==='grouped'?labels:[meta[en?1:0]],rows,matchCount:matches.length};
 }
 const meta=data.metric_meta[key];if(!meta)throw Error('Unknown chart metric');
 const pair=key.startsWith('AER-')?['AER-W','AER-L']:key.startsWith('DUEL-')?['DUEL-W','DUEL-L']:null;
 const rows=seasons.map(season=>{const values=data.snapshots[id+'|'+season]?.values||{};return {label:season+(season==='2026/27'?(en?' · ongoing':' · 진행 중'):''),values:(pair||[key]).map(code=>finite(values[code]))};});
 return {title:meta.label,type:pair?'stacked':meta.unit==='%'?'percent':'bars',scope:'season',unit:meta.unit==='%'?'%':meta.unit==='경기당'||meta.unit==='per match'?(en?'per match':'경기당'):(en?'season total':'시즌 합계'),series:pair?(en?['Won','Lost']:['승리','패배']):[meta.label],rows,description:meta.description};
}
const api={buildPlan,recentMeta,seasons};if(typeof module==='object'&&module.exports)module.exports=api;if(root)root.MatchDeskCharts=api;
})(typeof window!=='undefined'?window:globalThis);
