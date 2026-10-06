from pathlib import Path
import re

out = Path(__file__).parent
prior = out.parent / 'visualization-design-2026-10-06-v09'
page = (prior / 'index.html').read_text(encoding='utf-8')
toggle = '<label class="metric-details-toggle"><input id="metricdetails" type="checkbox" aria-controls="snapshotstats teamcontent">지표 설명 보기</label>'
assert toggle in page
page = page.replace(toggle, '')
page = page.replace('<label>${esc(meta.label)}</label>', '<button type="button" class="metric-trigger" data-metric="${esc(code)}" aria-haspopup="dialog" aria-expanded="false" aria-controls="metricpopover">${esc(meta.label)}<span aria-hidden="true">ⓘ</span></button>')
page = page.replace('<small class="metric-note">${esc(meta.description)}</small>', '')
page = page.replace("function renderSnapshot(){", "function renderSnapshot(){closeMetricHelp(false);")
page = re.sub(r"function syncMetricDetails\(\).*?syncMetricDetails\(\);", '', page, flags=re.S)
popover = '''<aside id="metricpopover" class="metric-popover" role="dialog" aria-modal="false" aria-labelledby="metrichelptitle" hidden>
<div class="metric-popover-head"><h3 id="metrichelptitle"></h3><button id="metrichelpclose" type="button" aria-label="지표 설명 닫기">×</button></div>
<p id="metrichelpmeaning"></p><div class="metric-reading"><b>읽는 법</b><p id="metrichelpreading"></p></div></aside>'''
page = page.replace('<script id="data"', popover + '<script id="data"', 1)
css = '''<style id="metric-popover-v10">
#snapshotstats .metric-trigger{display:flex;align-items:center;justify-content:space-between;gap:8px;width:100%;min-height:44px;padding:0;background:none;border:0;text-align:left;font:inherit;font-size:14px;font-weight:600;line-height:1.5;color:#33465b;cursor:pointer;overflow-wrap:anywhere}
.metric-trigger span{color:#657b92;flex-shrink:0}
.metric-trigger:hover,.metric-trigger[aria-expanded="true"]{color:#135bb0!important}
.metric-trigger:focus-visible,#metrichelpclose:focus-visible{outline:2px solid #135bb0;outline-offset:4px;border-radius:4px}
.metric-popover[hidden]{display:none}
.metric-popover{position:fixed;z-index:1000;box-sizing:border-box;width:min(340px,calc(100vw - 24px));max-height:calc(100dvh - 24px);overflow:auto;padding:18px;background:#fff;border:1px solid #b8cbe0;border-radius:14px;box-shadow:0 12px 40px #182b4030;color:#263b52;font-size:14px;line-height:1.7}
.metric-popover:before{content:'';position:absolute;left:22px;top:0;width:36px;height:3px;background:#3370b4;border-radius:0 0 4px 4px}
.metric-popover-head{display:flex;justify-content:space-between;align-items:center;gap:12px}
.metric-popover-head h3{font-size:16px;margin:0;overflow-wrap:anywhere}
#metrichelpclose{display:grid;place-items:center;width:44px;height:44px;flex-shrink:0;background:#f1f5f9;border:0;border-radius:10px;font-size:24px;cursor:pointer;color:#33465b}
.metric-popover p{margin:10px 0 0;overflow-wrap:anywhere}
.metric-reading{margin-top:14px;padding:12px;background:#f3f6fa;border-radius:10px}
.metric-reading b{font-size:12px;color:#57708b}
.metric-reading p{margin:4px 0 0}
</style>'''
page = page.replace('</head>', css + '</head>', 1)
js = '''
let metricHelpTrigger=null;
const metricReadingTips={
 'POSS-L':'수가 많다고 곧바로 공격력이 나쁘다는 뜻은 아닙니다. 공을 다룬 횟수와 패스 시도, 경기 수도 함께 보세요.',
 'PKC':'득점·실점이 아니라 상대에게 준 기회의 횟수입니다. 실제 페널티킥 실점과 구분해서 보세요.',
 'TKL-LM':'위기 상황의 수비 기록입니다. 많다는 이유만으로 전체 수비가 좋다고 판단하지 마세요.',
 'PASS%':'패스가 얼마나 잘 연결됐는지 보여줍니다. 패스 거리와 공격 지역 패스도 함께 보세요.',
 'POSS%':'공을 오래 소유한 정도입니다. 점유율만으로 승리나 좋은 득점 기회를 판단할 수는 없습니다.',
 'xA':'실제 도움과 비교할 수 있는 참고값입니다. 이 숫자만으로 다음 경기 도움 수를 확정할 수는 없습니다.',
 'SH-BLK':'공격·수비 방향의 원본 정의가 확인되기 전에는 수비력 평가에 사용하지 마세요.'
};
function closeMetricHelp(returnFocus=true){
 const trigger=metricHelpTrigger;
 if(trigger)trigger.setAttribute('aria-expanded','false');
 $('metricpopover').hidden=true;metricHelpTrigger=null;
 if(returnFocus&&trigger&&trigger.isConnected!==false)trigger.focus();
}
function openMetricHelp(code,trigger){
 const meta=D.metric_meta[code];if(!meta)return;
 if(metricHelpTrigger===trigger&&!$('metricpopover').hidden){closeMetricHelp();return}
 closeMetricHelp(false);metricHelpTrigger=trigger;
 $('metrichelptitle').textContent=meta.label;
 $('metrichelpmeaning').textContent=meta.description;
 $('metrichelpreading').textContent=metricReadingTips[code]||(meta.unit==='%'?'같은 리그와 기간의 비율을 비교해 보세요. 이 지표 하나만으로 팀의 전체 경기력을 판단하지 마세요.':meta.unit==='경기당'?'경기당 평균입니다. 시즌 누적 횟수와 구분해 비교해 보세요.':'시즌 전체 누적값입니다. 경기 수가 다르면 같은 기간이나 경기당 값으로 비교해 보세요.');
 trigger.setAttribute('aria-expanded','true');
 const pop=$('metricpopover');pop.hidden=false;
 const rect=trigger.getBoundingClientRect(),vw=window.innerWidth,vh=window.innerHeight;
 const width=Math.min(340,vw-24),height=pop.getBoundingClientRect().height;
 pop.style.left=Math.max(12,Math.min(rect.left,vw-width-12))+'px';
 pop.style.top=Math.max(12,Math.min(rect.bottom+8,vh-height-12))+'px';
 $('metrichelpclose').focus();
}
'''
page = page.replace('<script>', '<script>' + js, 1)
old = "document.addEventListener('click',event=>{const link=event.target.closest('[data-team]');"
new = "document.addEventListener('click',event=>{const metric=event.target.closest('[data-metric]');if(metric&&metric.dataset.metric){openMetricHelp(metric.dataset.metric,metric);return}if(!event.target.closest('#metricpopover'))closeMetricHelp(false);const link=event.target.closest('[data-team]');"
assert old in page
page = page.replace(old, new)
endjs = "\n$('metrichelpclose').onclick=()=>closeMetricHelp();\ndocument.addEventListener('keydown',event=>{if(event.key==='Escape'&&!$('metricpopover').hidden){event.preventDefault();closeMetricHelp()}});\nwindow.addEventListener('resize',()=>closeMetricHelp(false));\nwindow.addEventListener('scroll',event=>{if(event.target&&event.target.closest&&event.target.closest('#metricpopover'))return;closeMetricHelp(false)},true);\n"
page = page.replace('</script></body></html>', endjs + '</script></body></html>')
(out / 'index.html').write_text(page, encoding='utf-8')
check = (prior / 'check.cjs').read_text(encoding='utf-8')
check = re.sub(r"^test\('(?:metric explanations|explanation toggle|explanation preference).*?\n", '', check, flags=re.M)
check = check.replace("this.value='';", "this.value='';this.style={};this.attributes={};")
check = check.replace(' set innerHTML(s)', " setAttribute(name,value){this.attributes[name]=value}\n focus(){this.focused=true}\n getBoundingClientRect(){return {left:950,bottom:650,height:240}}\n set innerHTML(s)")
check = check.replace("window:{location:", "window:{innerWidth:1100,innerHeight:800,location:")
check = check.replace("assert(!cards.includes('TKL-LM'));assert(!cards.includes('PKC'));", "assert(!cards.replace(/<[^>]*>/g,'').includes('TKL-LM'));assert(!cards.replace(/<[^>]*>/g,'').includes('PKC'));")
check = check.replace("assert(cards.includes(data.metric_meta.PKC.description))", "assert(cards.includes('data-metric=\"PKC\"'));assert(!cards.includes('<small class=\"metric-note\">'))")
extra = '''
test('clicking a metric opens its meaning and reading tips in a labelled dialog',()=>{const trigger=new Node();trigger.dataset.metric='POSS-L';events.click({target:{closest(selector){return selector==='[data-metric]'?trigger:null}}});assert.strictEqual(get('metricpopover').hidden,false);assert.strictEqual(get('metrichelptitle').textContent,'공 소유권 상실');assert.strictEqual(get('metrichelpmeaning').textContent,data.metric_meta['POSS-L'].description);assert(get('metrichelpreading').textContent.includes('패스 시도'));assert.strictEqual(trigger.attributes['aria-expanded'],'true');assert(get('metrichelpclose').focused);assert(parseFloat(get('metricpopover').style.left)<=748);assert(parseFloat(get('metricpopover').style.top)<=548)});
test('same metric toggles, another switches, close returns focus',()=>{const a=new Node(),b=new Node();run('closeMetricHelp(false)');context.a=a;context.b=b;run('openMetricHelp("PKC",a)');run('openMetricHelp("TKL-LM",b)');assert.strictEqual(a.attributes['aria-expanded'],'false');assert.strictEqual(get('metrichelptitle').textContent,'최종 수비 태클');run('openMetricHelp("TKL-LM",b)');assert(get('metricpopover').hidden);assert(b.focused);run('openMetricHelp("PKC",a)');get('metrichelpclose').onclick();assert(get('metricpopover').hidden);assert(a.focused)});
test('Escape and outside click close bubble; clicking inside preserves it',()=>{const a=new Node();context.a=a;run('openMetricHelp("PKC",a)');events.click({target:{closest(selector){return selector==='#metricpopover'?get('metricpopover'):null}}});assert(!get('metricpopover').hidden);let prevented=false;events.keydown({key:'Escape',preventDefault(){prevented=true}});assert(prevented);assert(get('metricpopover').hidden);run('openMetricHelp("PKC",a)');events.click({target:{closest(){return null}}});assert(get('metricpopover').hidden)});
test('filter changes close stale explanation while search and sources stay available',()=>{const a=new Node();context.a=a;run('openMetricHelp("PKC",a)');get('metricsearch').value='공 소유권 상실';get('metricsearch').oninput();assert(get('metricpopover').hidden);assert(get('snapshotstats').innerHTML.includes('공 소유권 상실'));assert(html.includes('출처·수집 시점'));assert(!html.includes('id="metricdetails"'));assert(html.includes('aria-haspopup="dialog"'))});
test('scrolling within a long bubble preserves it while page scrolling dismisses it',()=>{const a=new Node();context.a=a;run('openMetricHelp("PKC",a)');events.scroll({target:{closest(){return get('metricpopover')}}});assert(!get('metricpopover').hidden);events.scroll({target:{closest(){return null}}});assert(get('metricpopover').hidden)});
'''
check = check.replace("fs.writeFileSync(__dirname+'/logic-check.json'", extra + "\nfs.writeFileSync(__dirname+'/logic-check.json'")
(out / 'check.cjs').write_text(check, encoding='utf-8')
print('Built v10 metric popovers; v09 preserved.')
