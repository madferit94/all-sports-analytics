(function(global){
'use strict';
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function timeline(race){
 const records=race.records||{},raw=records.laps||[];
 const valid=raw.filter(l=>l.date_start&&Number.isFinite(l.lap_duration)&&l.lap_duration>0);
 const start=valid.length?Math.min(...valid.map(l=>Date.parse(l.date_start))):Date.parse(race.session.date_start);
 const drivers=(records.drivers||[]).map(d=>{
  const result=(records.session_result||[]).find(x=>x.driver_number===d.driver_number)||{};
  const laps=valid.filter(l=>l.driver_number===d.driver_number).map(l=>({start:(Date.parse(l.date_start)-start)/1000,end:(Date.parse(l.date_start)-start)/1000+l.lap_duration,number:l.lap_number})).sort((a,b)=>a.start-b.start);
  return {driver:d,result,laps,stints:(records.stints||[]).filter(x=>x.driver_number===d.driver_number),pit:(records.pit||[]).filter(x=>x.driver_number===d.driver_number).map(x=>({...x,time:(Date.parse(x.date)-start)/1000}))};
 });
 const duration=Math.max(1,...drivers.flatMap(d=>d.laps.map(l=>l.end)));
 function state(time){
  const t=clamp(time,0,duration);
  const items=drivers.map(d=>{
   const active=d.laps.find(l=>t>=l.start&&t<l.end),past=d.laps.filter(l=>l.end<=t),previous=past[past.length-1];
   const progress=active?active.number-1+(t-active.start)/(active.end-active.start):previous?previous.number:0;
   const last=d.laps[d.laps.length-1],finished=!!last&&t>=last.end;
   const fullyRecorded=last&&last.number>=d.result.number_of_laps;
   const status=d.result.dns?'DNS':d.result.dsq&&t===duration?'DSQ':t===duration&&d.result.dnf?'DNF':t===duration&&d.result.position?'FINISHED':!d.laps.length?'NO DATA':finished?(d.result.dnf?'DNF':fullyRecorded?'FINISHED':'NO LAP DATA'):active?'RACING':'NO LAP DATA';
   const lap=active?active.number:previous?previous.number:0;
   const stint=d.stints.find(s=>lap>=s.lap_start&&lap<=s.lap_end);
   const inPit=d.pit.some(p=>t>=p.time&&t<p.time+(p.pit_duration||p.lane_duration||0));
   return {...d,progress,lap,status,compound:stint?.compound||'—',inPit,moving:!!active&&!d.result.dns};
  });
  items.sort((a,b)=>t===duration?(a.result.position||99)-(b.result.position||99):b.progress-a.progress||a.driver.driver_number-b.driver.driver_number);
  items.forEach((d,i)=>{d.rank=t===duration?(d.result.position||null):(d.progress>0?i+1:null)});
  return items;
 }
 return {start,duration,drivers,state};
}
function mount(container,race,options={}){
 const en=options.locale==='en',tr=(ko,english)=>en?english:ko,model=timeline(race),shape=options.shape;
 if(race.state!=='completed'){container.textContent=tr('종료된 레이스에서만 기록을 재생합니다.','Replay is available for completed races only.');return {destroy(){container.replaceChildren()}};}
 const points=shape?.status==='LOCATION_TRACE'&&shape.points?.length>20?shape.points:Array.from({length:120},(_,i)=>[.5+.46*Math.cos(i/120*Math.PI*2),.5+.28*Math.sin(i/120*Math.PI*2)]);
 const lengths=[0];for(let i=1;i<=points.length;i++){const a=points[i-1],b=points[i%points.length];lengths.push(lengths[i-1]+Math.hypot(a[0]-b[0],a[1]-b[1]));}
 function position(p){const dist=(p%1)*lengths[lengths.length-1];let i=1;while(i<lengths.length-1&&lengths[i]<dist)i++;const f=(dist-lengths[i-1])/(lengths[i]-lengths[i-1]||1),a=points[i-1],b=points[i%points.length];return [a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f]}
 const root=document.createElement('section');root.className='f1-record-replay';
 root.innerHTML=`<style>.f1-record-replay{border:3px solid #284535;background:#fff9e6;padding:16px;min-width:0;color:#193442}.f1-record-replay canvas{width:100%;height:auto;image-rendering:pixelated;background:#d5e4b8}.f1-replay-controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:12px 0}.f1-replay-controls button,.f1-replay-controls select{font:inherit;padding:8px;min-height:40px}.f1-replay-controls input{width:100%}.f1-replay-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:5px;font-family:Arial,sans-serif;font-size:14px}.f1-replay-row{border-left:6px solid var(--color);padding:7px;background:#fff;display:flex;justify-content:space-between;gap:7px}.f1-replay-note{font:14px/1.6 Arial,sans-serif}.f1-replay-clock{font:700 18px Arial,sans-serif}</style><h3>${tr('8비트 레이스 기록 재생','8-bit race record replay')}</h3><canvas width="800" height="450" aria-label="${tr('랩 기록 기반 레이스 재구성','Race reconstruction from recorded laps')}"></canvas><div class="f1-replay-controls"><button type="button" data-play>${tr('재생','Play')}</button><button type="button" data-reset>${tr('처음부터','Reset')}</button><label>${tr('속도','Speed')} <select data-speed><option value="10">10×</option><option value="30" selected>30×</option><option value="60">60×</option><option value="120">120×</option></select></label><span class="f1-replay-clock" aria-live="off"></span><input data-seek type="range" min="0" max="${model.duration}" value="0" step="any" aria-label="${tr('레이스 시간 이동','Seek race time')}"></div><p class="f1-replay-note">${shape?.status==='LOCATION_TRACE'?tr('트랙: 해당 세션의 한 랩 위치 기록 윤곽','Track: one recorded lap location trace'):tr('트랙: 실제 서킷 지도가 아닌 도식','Track: schematic, not the actual circuit map')} · ${tr('차량 이동과 중간 순위는 랩 시작·완료 시각 사이를 보간한 재구성입니다. 실제 GPS 주행·실시간 추월 기록이 아닙니다. 결측 구간은 차량을 멈추고 표시합니다.','Cars and intermediate order are reconstructed between recorded lap start/end times, not actual GPS movement or recorded overtakes. Cars pause during missing intervals.')}</p><div class="f1-replay-list"></div>`;
 container.replaceChildren(root);const canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d'),play=root.querySelector('[data-play]'),reset=root.querySelector('[data-reset]'),speed=root.querySelector('[data-speed]'),seek=root.querySelector('[data-seek]'),clock=root.querySelector('.f1-replay-clock'),list=root.querySelector('.f1-replay-list');
 let time=0,playing=false,frame=0,last=0,disposed=false,lastList=-1;const reduced=global.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
 if(reduced)root.querySelector('.f1-replay-note').append(document.createTextNode(tr(' 움직임 줄이기 설정: 자동 재생 안 함.',' Reduced-motion setting: no autoplay.')));
 function draw(){
  const states=model.state(time);ctx.clearRect(0,0,800,450);ctx.lineWidth=28;ctx.strokeStyle='#43534b';ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(80+p[0]*620,50+p[1]*340):ctx.moveTo(80+p[0]*620,50+p[1]*340));ctx.closePath();ctx.stroke();
  states.forEach((d,i)=>{const [x,y]=position(d.progress);const px=80+x*620,py=50+y*340;ctx.globalAlpha=['DNS','NO DATA','DNF','DSQ'].includes(d.status)?.35:1;ctx.fillStyle=/^[a-f\d]{6}$/i.test(d.driver.team_colour||'')?'#'+d.driver.team_colour:'#24465d';ctx.fillRect(Math.round(px-6),Math.round(py-4),12,8);ctx.fillStyle='#162633';ctx.font='bold 11px monospace';ctx.fillText(String(d.driver.driver_number),px+8,py+(i%3-1)*10)});ctx.globalAlpha=1;
  seek.value=time;clock.textContent=`${Math.floor(time/60)}:${String(Math.floor(time%60)).padStart(2,'0')} / ${Math.floor(model.duration/60)}:${String(Math.floor(model.duration%60)).padStart(2,'0')}${time>=model.duration?' · '+tr('종료','Finished'):''}`;
  if(time>=model.duration){ctx.fillStyle='#fff9e6';ctx.fillRect(275,185,250,58);ctx.fillStyle='#193442';ctx.font='bold 24px monospace';ctx.textAlign='center';ctx.fillText('FINISH',400,220);ctx.textAlign='left'}
  const statuses={'RACING':'주행','FINISHED':'완주','DNF':'리타이어','DNS':'미출발','DSQ':'실격','NO DATA':'자료 없음','NO LAP DATA':'랩 기록 공백'};
  const listKey=`${Math.floor(time)}:${time>=model.duration}`;if(listKey!==lastList){lastList=listKey;list.replaceChildren(...states.map(d=>{const row=document.createElement('div');row.className='f1-replay-row';row.style.setProperty('--color',/^[a-f\d]{6}$/i.test(d.driver.team_colour||'')?'#'+d.driver.team_colour:'#24465d');const name=document.createElement('span');name.textContent=`${d.rank??'—'} · ${d.driver.name_acronym||d.driver.driver_number}`;const detail=document.createElement('span');detail.textContent=`L${d.lap} · ${d.compound} · ${d.inPit?tr('피트','PIT'):(en?d.status:statuses[d.status]||d.status)}`;row.append(name,detail);return row}))}
 }
 function tick(now){if(disposed||!playing)return;if(last)time=Math.min(model.duration,time+(now-last)/1000*Number(speed.value));last=now;draw();if(time>=model.duration){playing=false;play.textContent=tr('재생','Play');last=0;return}frame=requestAnimationFrame(tick)}
 const toggle=()=>{playing=!playing;play.textContent=playing?tr('일시정지','Pause'):tr('재생','Play');cancelAnimationFrame(frame);last=0;if(playing){if(time>=model.duration)time=0;frame=requestAnimationFrame(tick)}};
 const rewind=()=>{playing=false;cancelAnimationFrame(frame);last=0;time=0;lastList=-1;play.textContent=tr('재생','Play');draw()};
 const move=()=>{time=clamp(Number(seek.value),0,model.duration);last=0;lastList=-1;draw()};const hidden=()=>{if(document.hidden&&playing)toggle()};
 play.addEventListener('click',toggle);reset.addEventListener('click',rewind);seek.addEventListener('input',move);document.addEventListener('visibilitychange',hidden);draw();
 return {destroy(){disposed=true;playing=false;cancelAnimationFrame(frame);document.removeEventListener('visibilitychange',hidden);play.removeEventListener('click',toggle);reset.removeEventListener('click',rewind);seek.removeEventListener('input',move);container.replaceChildren()},timeline:model};
}
global.MatchLabF1Replay={mount,timeline};
})(typeof window!=='undefined'?window:globalThis);

