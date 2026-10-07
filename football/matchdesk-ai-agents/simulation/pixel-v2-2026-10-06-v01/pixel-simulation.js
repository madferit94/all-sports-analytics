(function(root){
  'use strict';
  function validate(p){
    if(!p || !Array.isArray(p.probabilities) || p.probabilities.length!==3 || p.probabilities.some(x=>typeof x!=='number'||!Number.isFinite(x)||x<0||x>1) || Math.abs(p.probabilities.reduce((a,b)=>a+b,0)-1)>1e-6) throw new Error('Three ordered probabilities summing to 1 are required.');
    if(!p.model || ['unavailable','blocked','pending','error'].includes(p.status)) throw new Error('An available model prediction is required.');
    if(p.scoreDistribution){
      if(!Array.isArray(p.scoreDistribution)||!p.scoreDistribution.length) throw new Error('Invalid score distribution.');
      p.scoreDistribution.forEach(s=>{if(!Number.isInteger(s.home)||!Number.isInteger(s.away)||s.home<0||s.away<0||s.home>12||s.away>12||!Number.isFinite(s.probability)||s.probability<0) throw new Error('Invalid score cell.');});
      const masses=[0,0,0];p.scoreDistribution.forEach(s=>masses[s.home>s.away?0:s.home===s.away?1:2]+=s.probability);
      if(masses.some((v,i)=>Math.abs(v-p.probabilities[i])>1e-6)) throw new Error('Score cells must match supplied outcome probabilities.');
    }
    return p;
  }
  function sample(p,rng){
    validate(p);rng=rng||Math.random;
    const u=rng();if(!Number.isFinite(u)||u<0||u>=1) throw new Error('Random value must be in [0,1).');
    let outcome=u<p.probabilities[0]?0:u<p.probabilities[0]+p.probabilities[1]?1:2;
    let score=[[1,0],[1,1],[0,1]][outcome];
    if(p.scoreDistribution){
      const cells=p.scoreDistribution.filter(s=>(s.home>s.away?0:s.home===s.away?1:2)===outcome);
      const mass=cells.reduce((a,s)=>a+s.probability,0), v=rng();
      if(!Number.isFinite(v)||v<0||v>=1) throw new Error('Random value must be in [0,1).');
      let t=v*mass,selected=cells[cells.length-1];for(const cell of cells){t-=cell.probability;if(t<0){selected=cell;break;}}score=[selected.home,selected.away];
    }
    const goals=[];for(let i=0;i<score[0];i++) goals.push(0);for(let i=0;i<score[1];i++) goals.push(1);
    // Interleave only fictional event order. No real shot coordinates or timings.
    goals.sort((a,b)=>a-b);const ordered=[];while(goals.length){ordered.push(goals.shift());if(goals.length)ordered.push(goals.pop());}
    return {outcome,score,goals:ordered,scoreFromModel:!!p.scoreDistribution};
  }
  function rosterPositions(progress,colors){
    if(!Number.isFinite(progress)||progress<0||progress>1)throw new Error('Progress must be in [0,1].');
    colors=colors||['#cf3340','#4779d5'];
    const keeperColors=['#f5c542','#bd72e8','#f3ede0','#e98b43'].filter(c=>!colors.map(x=>x.toLowerCase()).includes(c));
    const shape=[[27,98],[62,52],[62,82],[62,112],[62,142],[99,52],[99,82],[99,112],[99,142],[136,76],[136,122]],players=[];
    for(let team=0;team<2;team++)for(let index=0;index<11;index++){
      const goalkeeper=index===0,base=shape[index],phase=progress*8*Math.PI;
      const direction=team===0?1:-1,advance=(.5+.5*Math.sin(progress*4*Math.PI+team*Math.PI));
      const range=goalkeeper?0:index>=9?110:index>=5?75:38;
      const x=Math.max(23,Math.min(297,(team===0?base[0]:320-base[0])+direction*advance*range+Math.sin(phase+index*1.7+team)*(goalkeeper?2:8)));
      const y=Math.max(43,Math.min(153,base[1]+Math.cos(phase*.6+index+team)*(goalkeeper?8:14)));
      const shirt=goalkeeper?keeperColors[team]:colors[team];
      players.push({team,index,role:goalkeeper?'goalkeeper':'outfield',x,y,shirt,stride:Math.sin(progress*60*Math.PI+index)>0?1:-1});
    }
    return players;
  }
  function drawRoster(ctx,players){
    players.forEach(({x,y,shirt,role,stride})=>{
      x=Math.round(x);y=Math.round(y);const step=stride||1;
      ctx.fillStyle='#f1c795';ctx.fillRect(x-1,y-5,3,3);ctx.fillStyle=shirt;ctx.fillRect(x-3,y-2,7,6);ctx.fillStyle='#172c3a';ctx.fillRect(x-3,y+4+(step>0?0:2),2,3);ctx.fillRect(x+2,y+4+(step>0?2:0),2,3);
      if(role==='goalkeeper'){ctx.fillStyle='#ffffff';ctx.fillRect(x-5,y,2,2);ctx.fillRect(x+4,y,2,2);}
    });
  }
  function matchFrame(progress,colors,goals){
    if(!Array.isArray(goals)||goals.some(t=>t!==0&&t!==1))throw new Error('Invalid goal sequence');
    const players=rosterPositions(progress,colors), times=goals.map((_,i)=>(i+1)/(goals.length+1));
    const cycle=Math.min(goals.length,Math.floor(progress*(goals.length+1)));
    const u=Math.min(1,progress*(goals.length+1)-cycle), team=cycle<goals.length?goals[cycle]:(goals.length?1-goals[goals.length-1]:0);
    const direction=team===0?1:-1, mirror=x=>team===0?x:320-x;
    const previous=cycle?{x:goals[cycle-1]===0?306:14,y:98}:{x:160,y:98};
    // Every attack begins exactly where the previous one ended. Return the
    // ball to the centre on a visible ground path instead of teleporting it.
    const points=[previous,{x:160,y:98},{x:mirror(176),y:130},{x:mirror(201),y:119},{x:mirror(222),y:66},{x:mirror(248),y:75},{x:mirror(271),y:98},{x:mirror(cycle<goals.length?306:293),y:98}];
    const knots=[0,.12,.20,.36,.48,.65,.82,1];
    const phases=['kickoff','pass','dribble','pass','dribble','pass',cycle<goals.length?'shot':'save'];
    let segment=knots.findIndex((t,i)=>i<knots.length-1&&u>=t&&u<knots[i+1]);if(segment<0)segment=6;
    const mix=Math.max(0,Math.min(1,(u-knots[segment])/(knots[segment+1]-knots[segment])));
    const a=points[segment],b=points[segment+1],ball={x:a.x+(b.x-a.x)*mix,y:a.y+(b.y-a.y)*mix};
    const phase=phases[segment];
    // Continuous formation translation follows the ball. Local runs and
    // defensive tracking use smooth weights, so changing possession never
    // changes an actor's position abruptly.
    const shape=[[27,98],[62,52],[62,82],[62,112],[62,142],[99,52],[99,82],[99,112],[99,142],[136,76],[136,122]];
    players.forEach(p=>{
      const dir=p.team===0?1:-1,base=shape[p.index],bx=p.team===0?base[0]:320-base[0];
      const oriented=(ball.x-160)*dir;
      const advance=Math.max(0,Math.min(1,(oriented+135)/270));
      const range=p.index>=9?130:p.index>=5?95:52;
      let x=bx+dir*(p.index===0?0:advance*range),y=base[1];
      if(p.index===0){y=98+(ball.y-98)*.36;}
      else{
        const run=progress*36*Math.PI+p.index*1.8+p.team;
        x+=Math.sin(run)*10;y+=Math.cos(run*.7)*9+(ball.y-98)*.18;
        const distance=Math.hypot(x-ball.x,y-ball.y),press=Math.exp(-distance*distance/2200)*.78;
        x+=(ball.x-dir*6-x)*press;y+=(ball.y-5-y)*press;
      }
      p.x=Math.max(23,Math.min(297,x));p.y=Math.max(43,Math.min(153,y));
      p.stride=Math.sin(progress*160*Math.PI+p.index)>0?1:-1;
    });
    // During a carry, the midfielder/forward travels with the ball at his
    // feet; smooth handoff weights retain continuity before and after it.
    if(phase==='dribble'){
      const carrier=players.find(p=>p.team===team&&p.index===(segment===2?6:9));
      const weight=Math.sin(mix*Math.PI)**2;
      carrier.x+=(ball.x-direction*5-carrier.x)*weight;
      carrier.y+=(ball.y-5-carrier.y)*weight;
      carrier.x=Math.max(23,Math.min(297,carrier.x));carrier.y=Math.max(43,Math.min(153,carrier.y));
    }
    const flash=times.some(t=>progress>=t&&progress<t+Math.min(.028,.08/(goals.length+1)));
    return {players,ball,phase,team,goal:flash,score:[times.filter((t,i)=>t<=progress&&goals[i]===0).length,times.filter((t,i)=>t<=progress&&goals[i]===1).length]};
  }
  function mount(container,prediction,options){
    validate(prediction);options=options||{};if(!container||!container.ownerDocument)throw new Error('A DOM container is required.');
    const doc=container.ownerDocument,win=doc.defaultView||root,en=options.locale==='en';
    const labels=en?{title:'8-bit match simulation',note:'A fictional sample drawn from model probabilities. The movement and goal times are invented; this is not a real match replay.',play:'Play',pause:'Pause',replay:'New simulation',home:'Home win',draw:'Draw',away:'Away win',sample:'Sample result',ready:'Ready',done:'Finished',motion:'Reduced motion: showing the sample result without animation.',score:'Illustrative score; the model supplies outcome probabilities only.'}:{title:'8비트 경기 시뮬레이션',note:'모델 확률에서 뽑은 가상 경기입니다. 선수 움직임과 골 시간은 연출이며 실제 경기 재현이 아닙니다.',play:'재생',pause:'일시정지',replay:'새 시뮬레이션',home:'홈 승',draw:'무승부',away:'원정 승',sample:'가상 결과',ready:'재생 준비',done:'종료',motion:'움직임 줄이기 설정에 따라 가상 결과만 표시합니다.',score:'연출용 점수입니다. 모델은 승무패 확률만 제공합니다.'};
    const names=[options.homeName||prediction.home||'HOME',options.awayName||prediction.away||'AWAY'].map(String);
    const colors=[options.homeColor||'#cf3340',options.awayColor||'#4779d5'].map(x=>/^#[0-9a-f]{6}$/i.test(x)?x:'#4779d5');
    const section=doc.createElement('section');section.className='md-pixel-simulation';
    function el(tag,text,cls){const n=doc.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;}
    section.appendChild(el('h3',labels.title));section.appendChild(el('p',labels.note+' '+(en?'11 players per team including a goalkeeper. The shape is fictional, not a confirmed formation.':'각 팀은 골키퍼 포함 11명입니다. 배치는 연출용이며 실제 포메이션이 아닙니다.'),'md-sim-note'));
    const odds=el('div',undefined,'md-sim-odds');[labels.home,labels.draw,labels.away].forEach((label,i)=>odds.appendChild(el('span',label+' '+(prediction.probabilities[i]*100).toFixed(1)+'%')));section.appendChild(odds);
    const canvas=el('canvas');canvas.width=320;canvas.height=180;canvas.setAttribute('role','img');canvas.setAttribute('aria-label',labels.title);section.appendChild(canvas);
    const result=el('p',labels.ready,'md-sim-result');result.setAttribute('aria-live','polite');section.appendChild(result);
    const controls=el('div',undefined,'md-sim-controls'),play=el('button',labels.play),replay=el('button',labels.replay);play.type=replay.type='button';controls.append(play,replay);section.appendChild(controls);
    container.appendChild(section);
    const ctx=canvas.getContext('2d');if(!ctx){section.appendChild(el('p',en?'Canvas is unavailable.':'이 환경에서는 애니메이션을 표시할 수 없습니다.'));play.disabled=replay.disabled=true;return {destroy:()=>section.remove()};}
    ctx.imageSmoothingEnabled=false;
    const reduced=!!(win.matchMedia&&win.matchMedia('(prefers-reduced-motion: reduce)').matches);
    let run=sample(prediction,options.rng),elapsed=0,last=0,playing=false,raf=0,destroyed=false;
    let duration=Math.max(18000,(run.goals.length+1)*3500);
    function state(){const shown=run.goals.filter((_,i)=>elapsed/duration>=(i+1)/(run.goals.length+1));return [shown.filter(x=>x===0).length,shown.filter(x=>x===1).length];}
    function draw(){
      const progress=Math.min(elapsed/duration,1),score=state();ctx.fillStyle='#172c3a';ctx.fillRect(0,0,320,180);
      ctx.fillStyle='#457e45';ctx.fillRect(10,27,300,143);for(let x=10;x<310;x+=40){ctx.fillStyle='#4b884b';ctx.fillRect(x,27,20,143);}
      ctx.strokeStyle='#d8e9b3';ctx.lineWidth=1;ctx.strokeRect(18.5,35.5,283,126);ctx.beginPath();ctx.moveTo(160,35);ctx.lineTo(160,162);ctx.stroke();ctx.strokeRect(18.5,70.5,37,55);ctx.strokeRect(265.5,70.5,36,55);ctx.strokeRect(11.5,84.5,7,27);ctx.strokeRect(301.5,84.5,7,27);
      // Pixel circle at midfield.
      const ring=[[0,-16],[8,-14],[14,-8],[16,0],[14,8],[8,14],[0,16],[-8,14],[-14,8],[-16,0],[-14,-8],[-8,-14]];ring.forEach(([x,y])=>{ctx.fillStyle='#d8e9b3';ctx.fillRect(159+x,97+y,2,2);});
      const scene=matchFrame(progress,colors,run.goals);drawRoster(ctx,scene.players);
      ctx.fillStyle='#173629';ctx.fillRect(Math.round(scene.ball.x)-1,Math.round(scene.ball.y)+4,5,2);
      ctx.fillStyle='#fff5d5';ctx.fillRect(Math.round(scene.ball.x),Math.round(scene.ball.y),4,4);
      if(scene.goal){ctx.fillStyle='#172c3a';ctx.fillRect(113,67,94,28);ctx.fillStyle='#ffd56b';ctx.font='bold 19px monospace';ctx.textAlign='center';ctx.fillText('GOAL!',160,87);}
      ctx.fillStyle='#fff5d5';ctx.font='bold 10px monospace';ctx.textAlign='center';ctx.fillText(score[0]+' : '+score[1]+'   '+Math.round(progress*90)+"'",160,17);
      canvas.setAttribute('aria-label',names[0]+' '+score[0]+' : '+score[1]+' '+names[1]);
    }
    function finish(){playing=false;play.textContent=labels.play;result.textContent=labels.sample+': '+names[0]+' '+run.score[0]+' : '+run.score[1]+' '+names[1]+' · '+labels.done;}
    function frame(now){if(!playing||destroyed)return;if(last)elapsed=Math.min(duration,elapsed+Math.max(0,Math.min(now-last,100)));last=now;draw();if(elapsed>=duration)finish();else raf=win.requestAnimationFrame(frame);}
    play.addEventListener('click',()=>{if(playing){playing=false;win.cancelAnimationFrame(raf);play.textContent=labels.play;last=0;return;}if(elapsed>=duration)elapsed=0;if(reduced){elapsed=duration;draw();finish();return;}playing=true;last=0;play.textContent=labels.pause;raf=win.requestAnimationFrame(frame);});
    replay.addEventListener('click',()=>{playing=false;win.cancelAnimationFrame(raf);run=sample(prediction,options.rng);duration=Math.max(18000,(run.goals.length+1)*3500);elapsed=reduced?duration:0;last=0;play.textContent=labels.play;result.textContent=labels.ready;draw();if(reduced)finish();});
    if(reduced){elapsed=duration;section.appendChild(el('p',labels.motion,'md-sim-note'));draw();finish();}else draw();
    return {destroy:()=>{destroyed=true;playing=false;win.cancelAnimationFrame(raf);section.remove();},sample:()=>({outcome:run.outcome,score:run.score.slice(),scoreFromModel:run.scoreFromModel})};
  }
  const api={validate,sample,mount,rosterPositions,drawRoster,matchFrame};if(typeof module==='object'&&module.exports)module.exports=api;if(root)root.MatchDeskSimulation=api;
})(typeof window!=='undefined'?window:globalThis);
