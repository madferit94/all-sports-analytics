/* Browser-native recorded-data analysis. No model, SQL interpreter or Python runtime. */
(function(root){
 'use strict';
 const aliases={Arsenal:['아스널','아스날'],Barcelona:['바르셀로나','바르샤'],Liverpool:['리버풀'],'Manchester City':['맨체스터 시티','맨시티'],'Manchester United':['맨체스터 유나이티드','맨유'],'Real Madrid':['레알 마드리드','레알마드리드'],Chelsea:['첼시'],Tottenham:['토트넘'],'Atletico Madrid':['아틀레티코 마드리드'],Valencia:['발렌시아'],Sevilla:['세비야'],Leeds:['리즈']};
 const metrics={xg:{ko:'기대 득점',en:'Expected goals',keys:['기대 득점','기대득점','xg','expected goals']},xga:{ko:'기대 실점',en:'Expected goals against',keys:['기대 실점','기대실점','xga','expected goals against']},gf:{ko:'득점',en:'Goals scored',keys:['득점','goals scored','goals']},ga:{ko:'실점',en:'Goals conceded',keys:['실점','goals conceded']},p:{ko:'승점',en:'Points',keys:['승점','points']},w:{ko:'승률',en:'Win rate',keys:['승률','win rate']}};
 const normalize=s=>String(s).toLowerCase().replace(/\s+/g,' ').trim();
 function summary(id,ms){const s={n:ms.length,gf:0,ga:0,xg:0,xga:0,p:0,w:0,d:0,l:0};for(const m of ms){const h=m.home===id,f=h?m.hg:m.ag,a=h?m.ag:m.hg;s.gf+=f;s.ga+=a;s.xg+=h?m.hx:m.ax;s.xga+=h?m.ax:m.hx;s.w+=f>a;s.d+=f===a;s.l+=f<a;s.p+=f>a?3:f===a?1:0}return s}
 function create(data){
  const registry=new Map(),resolvers=[],teams=Object.entries(data.teams).map(([id,t])=>({...t,id}));
  function parse(question,defaults={},previous=null){
   const q=normalize(question);if(!q||q.length>500)return {error:'empty'};
   for(const resolver of resolvers){const args=resolver.match(question,defaults,previous);if(args)return {...args,question,tool:resolver.name}}
   if(/확률|예측|배당|probabilit|predict|odds/.test(q))return {tool:'prediction',question};
   const recognized=teams.filter(t=>[t.name,...(aliases[t.name]||[])].some(name=>q.includes(normalize(name))));
   if(/챔피언|champions|nfl|분데스|bundesliga|세리에|serie a|k리그|k-league/.test(q))return {error:'league'};
   const explicitLeague=/라리가|la\s?liga/.test(q)?'La_liga':/프리미어|\bpl\b|\bepl\b|premier/.test(q)?'EPL':null;
   if(explicitLeague&&recognized.some(t=>t.league!==explicitLeague))return {error:'league_mismatch'};
   const seasonMatch=q.match(/(20\d{2})\s*[/\-]\s*(\d{2}|20\d{2})/);
   let season=seasonMatch?seasonMatch[1]+'/'+seasonMatch[2].slice(-2):/이번\s?시즌|this season|current season/.test(q)?'2026/27':null;
   if(season&&!['2023/24','2024/25','2025/26','2026/27'].includes(season))return {error:'season'};
   const recent=q.match(/(?:최근|last|recent)\s*(\d+)\s*(?:경기|matches|games)?/),follow=/다시|이 결과|그 결과|이것|다른|대신|again|instead|same|those|only/.test(q)&&previous;
   const plan=follow?{...previous}:{tool:'team',teams:[],league:explicitLeague||defaults.league||'EPL',season:defaults.season||'2026/27',last:null,venue:'all',metric:'xg',perMatch:false};
   if(recognized.length){plan.teams=recognized.map(t=>t.id);if(!explicitLeague)plan.league=recognized[0].league}
   else if(!follow&&defaults.team)plan.teams=[defaults.team];
   if(explicitLeague)plan.league=explicitLeague;if(season)plan.season=season;
   if(recent){plan.last=Number(recent[1]);if(plan.last<1||plan.last>38)return {error:'range'}}
   else if(/시즌\s?전체|full season|all matches/.test(q))plan.last=null;
   if(/홈.*원정|원정.*홈|home.*away|away.*home/.test(q))plan.tool='venue';
   else if(/순위|높은 팀|상위|ranking|rank|top teams|highest/.test(q))plan.tool='ranking';
   else if(plan.teams.length>1||/비교|compare|comparison/.test(q))plan.tool='comparison';
   else if(!follow)plan.tool='team';
   if(plan.tool!=='venue'){if(/원정|\baway\b/.test(q))plan.venue='away';else if(/홈|\bhome\b/.test(q))plan.venue='home';else if(/전체\s?장소|all venues/.test(q))plan.venue='all'}
   const matches=Object.entries(metrics).sort((a,b)=>Math.max(...b[1].keys.map(k=>k.length))-Math.max(...a[1].keys.map(k=>k.length))).filter(([,m])=>m.keys.some(k=>q.includes(k)));
   if(matches.length)plan.metric=matches[0][0];
   plan.compareGoals=(follow&&plan.compareGoals)||(/xg|기대\s?득점|expected goals/.test(q)&&/실제\s?득점|득점과|득점.*비교|actual goals|goals.*compar|compare.*goals.*xg|goals.*(?:and|vs).*xg|xg.*(?:and|vs).*goals/.test(q)&&plan.teams.length===1);
   if(plan.compareGoals)plan.tool='trend';
   plan.perMatch=/경기당|per match|per game|평균|average/.test(q)?true:/합계|total/.test(q)?false:plan.perMatch;
   if(/슈팅|점유|패스|선수|포메이션|부상|시장|날씨|shot|possession|pass|player|formation|injur|weather|npxg|페널티 제외|20\d{2}-\d{2}-\d{2}|승리한 경기|패배한 경기|무승부 경기|won matches|lost matches|drop table|delete from/.test(q))return {error:'metric'};
   if(!recognized.length&&!follow&&!/xg|기대|득점|실점|승점|승률|최근|시즌|홈|원정|리그|순위|goals|points|rate|matches|season|home|away|rank|league/.test(q))return {error:'unsupported'};
   if(plan.tool!=='ranking'&&!plan.teams.length)return {error:'team'};
   plan.question=question;return plan;
  }
  function records(id,plan,venue=plan.venue){let ms=data.completed.filter(m=>m.season===plan.season&&(m.home===id||m.away===id)&&(venue==='all'||(venue==='home'?m.home===id:m.away===id))).sort((a,b)=>a.date.localeCompare(b.date)||a.id.localeCompare(b.id));return plan.last?ms.slice(-plan.last):ms}
  function value(s,plan){return !s.n?null:plan.metric==='w'?s.w/s.n*100:plan.perMatch?s[plan.metric]/s.n:s[plan.metric]}
  const base=(plan,rows)=>({status:rows.some(r=>r.n>0)?'ok':'empty',tool:plan.tool,plan,rows,engine:'JavaScript',datasetThrough:data.completed.map(m=>m.date).sort().at(-1),metric:plan.compareGoals?'xg':plan.metric,perMatch:plan.perMatch,unit:plan.metric==='w'?'%':'',verification:{finite:rows.every(r=>r.value===null||Number.isFinite(r.value)),matches:rows.reduce((n,r)=>n+r.n,0)},formula:plan.metric==='w'?'wins / matches × 100':plan.perMatch?plan.metric+' / matches':'sum('+plan.metric+')'});
  function clubRows(plan){return plan.teams.map(id=>{const ms=records(id,plan),s=summary(id,ms);return {id,label:data.teams[id].name,...s,value:value(s,plan),dates:ms.map(m=>m.date)}})}
  registry.set('team',plan=>base(plan,clubRows(plan)));
  registry.set('comparison',plan=>base(plan,clubRows(plan)));
  registry.set('ranking',plan=>{const ids=teams.filter(t=>t.league===plan.league).map(t=>t.id);const r=clubRows({...plan,teams:ids}).filter(r=>r.n);r.sort((a,b)=>b.value-a.value||a.label.localeCompare(b.label));return base(plan,r)});
  registry.set('venue',plan=>{const id=plan.teams[0];return base(plan,['home','away'].map(venue=>{const ms=records(id,plan,venue),s=summary(id,ms);return {label:venue,...s,value:value(s,plan),dates:ms.map(m=>m.date)}}))});
  registry.set('trend',plan=>{const id=plan.teams[0],ms=records(id,plan);return base(plan,ms.map(m=>{const h=m.home===id;return {id:m.id,label:m.date,n:1,value:h?m.hx:m.ax,actual:h?m.hg:m.ag,opponent:data.teams[h?m.away:m.home].name}}))});
  function execute(plan){if(plan.error)return {status:'unsupported',reason:plan.error};const tool=registry.get(plan.tool);if(!tool)return {status:'unavailable',reason:plan.tool};return tool(plan)}
  return {parse,execute,records,register(name,handler,match){if(typeof handler!=='function')throw new TypeError('Handler required');if(match&&typeof match!=='function')throw new TypeError('Matcher must be a function');registry.set(name,handler);if(match)resolvers.push({name,match})},capabilities(){return [...registry.keys()]}};
 }
 const api={create,metrics,summary};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.MatchDeskAnalysis=api;
})(globalThis);
