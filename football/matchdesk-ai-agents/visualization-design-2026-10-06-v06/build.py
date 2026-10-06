"""Connect collected match-level and season-snapshot statistics with honest filters."""
import csv
import hashlib
import json
import re
from pathlib import Path

out=Path(__file__).resolve().parent
project=out.parent
base=out.parents[3]
source=base/'source-unified-2026-10-06-v01'
page=(project/'visualization-design-2026-10-06-v05/index.html').read_text(encoding='utf-8')
data=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',page,re.S)[1])
def read(name):
    with (source/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def number(s):
    return None if s in ('',None) else float(s)
match_rows=read('team_match_stats.csv')
fields=['npxg_for','npxg_against','deep','deep_allowed','ppda_att','ppda_def','ppda_allowed_att','ppda_allowed_def','expected_points']
data['match_detail']={r['team_key']+'|'+r['match_key']:{k:number(r[k]) for k in fields} for r in match_rows}
assert len(data['match_detail'])==4798
snapshots=read('team_season_additional_stats.csv')
stat_fields=[k for k in snapshots[0] if k.startswith('statmuse_')]
data['snapshots']={r['team_key']+'|'+r['season']:dict(values={k.removeprefix('statmuse_'):number(r[k]) for k in stat_fields},source=r['source_url'],observed=r['observed_at_utc']) for r in snapshots}
assert len(data['snapshots'])==160
meta={
'A':('助攻','attack'),'xA':('기대 도움','attack'),'POSS%':('점유율','passing'),'PK':('페널티킥 득점','attack'),'FK':('프리킥 득점','attack'),'SH':('슈팅','attack'),'SOT':('유효 슈팅','attack'),'TCH':('터치','passing'),'TCH-BOX':('상대 박스 터치','attack'),'OFF':('오프사이드','attack'),'PASS':('성공 패스','passing'),'PASS/M':('경기당 패스','passing'),'PASS%':('패스 성공률','passing'),'PASS-ATT':('시도 패스','passing'),'BCC':('큰 기회 창출','attack'),'PASS-KEY':('키 패스','passing'),'PASS-LNG':('긴 패스','passing'),'PASS-F3RD':('파이널 서드 패스','passing'),'THRU-BALL':('스루 패스','passing'),'CRS':('크로스','passing'),'CNR':('코너킥','attack'),'TKL':('태클','defence'),'TKL-W':('성공 태클','defence'),'TKL-LM':('TKL-LM','defence'),'SH-BLK':('슈팅 차단','defence'),'BLK-CRS':('크로스 차단','defence'),'INT':('인터셉트','defence'),'CLR':('클리어링','defence'),'REC':('볼 회수','defence'),'ERR-SH':('슈팅으로 이어진 실수','defence'),'ERR-G':('실점으로 이어진 실수','defence'),'PKC':('PKC','discipline'),'OG':('자책골','defence'),'SV':('선방','defence'),'SV-PK':('페널티킥 선방','defence'),'CS':('무실점 경기','defence'),'YC':('경고','discipline'),'RC':('퇴장','discipline'),'FOUL':('파울','discipline'),'FOULED':('피파울','discipline'),'PK-W':('페널티킥 획득','attack'),'CNR-W':('코너킥 획득','attack'),'AER-W':('공중볼 경합 승리','duels'),'AER-L':('공중볼 경합 패배','duels'),'DUEL-W':('경합 승리','duels'),'DUEL-L':('경합 패배','duels'),'POSS-L':('소유권 상실','duels')}
meta['A']=('도움','attack')  # Korean display label, source code A retained.
assert set(meta)=={k.removeprefix('statmuse_') for k in stat_fields}
data['metric_meta']={k:dict(label=v[0],category=v[1],unit='%' if '%' in k else '경기당' if k=='PASS/M' else '원본 합계') for k,v in meta.items()}
page=re.sub(r'<script id="data" type="application/json">.*?</script>',lambda _:'<script id="data" type="application/json">'+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>',page,flags=re.S)
style='''<style>
.filterdeck{display:flex;gap:12px;flex-wrap:wrap;padding:16px 0}.filterdeck label{font-size:13px;color:#536174;display:flex;align-items:center;gap:7px}.filterdeck input{font:inherit;min-height:44px;border:1px solid #cbd4df;border-radius:6px;padding:8px;background:#fff;max-width:100%}.catalog{display:flex;gap:8px;flex-wrap:wrap;max-height:140px;overflow:auto;margin:12px 0 22px}.catalogitem{background:#fff;border:1px solid #dce2e9;border-radius:8px;padding:4px 10px 4px 4px}.catalogitem .mini{font-size:13px}.catalogitem.active{border:2px solid #17283b;padding:3px 9px 3px 3px}.metricgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0}.metriccard{background:#f5f7fa;border:1px solid #e1e6ed;border-radius:9px;padding:16px;min-width:0}.metriccard strong{display:block;font-size:25px;margin:7px 0}.metriccard label{display:block;font-size:13px;color:#536174}.metriccard small{font-size:11px;color:#536174}.statfilters{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:18px 0}.statfilters input{min-height:44px;padding:8px 12px;border:1px solid #cbd4df;border-radius:6px;font:inherit;max-width:100%}.scope{display:flex;gap:14px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin-top:26px}.scope p{font-size:13px;color:#536174}.scope h3{margin:0}.filtererror{color:#a32020;font-size:14px}.filtererror:empty{display:none}.coretable{margin-top:18px}.catalogsearch input{min-height:44px;padding:8px 12px;border:1px solid #cbd4df;border-radius:6px;font:inherit;max-width:100%}@media(max-width:750px){.metricgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.filterdeck{gap:8px}.filterdeck label{flex-wrap:wrap}.metriccard{padding:12px}}
</style>'''
page=page.replace('</head>',style+'</head>')
needle='<section id="team" hidden><div class="teamchooser">'
replacement='<section id="team" hidden><label class="catalogsearch">팀 검색 <input id="teamsearch" type="search" placeholder="팀 이름" aria-label="팀 이름 검색"></label><div id="teamcatalog" class="catalog" aria-label="팀 목록"></div><div class="teamchooser">'
assert needle in page
page=page.replace(needle,replacement)
needle='</div><article class="panel" id="teamcontent"></article></section>'
replacement='</div><div class="filterdeck"><label>경기 범위 <select id="rangefilter"><option value="season">시즌 전체</option><option value="5">최근 5경기</option><option value="10">최근 10경기</option><option value="custom">날짜 선택</option></select></label><label>시작 <input id="startdate" type="date" disabled></label><label>종료 <input id="enddate" type="date" disabled></label></div><div id="filtererror" class="filtererror" role="status"></div><article class="panel" id="teamcontent"></article><article class="panel"><div class="scope"><h3>시즌 상세 통계</h3><span id="snapcount" class="status"></span></div><p class="muted">StatMuse 시즌 전체 · 기간/장소/결과 필터 미적용</p><div class="statfilters"><label>지표 <select id="metricgroup"><option value="all">전체 지표</option><option value="attack">공격</option><option value="passing">패스·점유</option><option value="defence">수비·골키핑</option><option value="duels">경합</option><option value="discipline">반칙·징계</option></select></label><input id="metricsearch" type="search" placeholder="슈팅, 패스, xA…" aria-label="지표 검색"></div><div id="snapshotstats" class="metricgrid"></div><details><summary>출처·수집 시점</summary><div id="snapshotprovenance" class="note"></div></details></article></section>'
assert needle in page
page=page.replace(needle,replacement)
js=r'''function renderCatalog(){let query=$('teamsearch').value.trim().toLowerCase(),selected=$('teamselect').value,season=$('season').value;let ts=Object.values(T).filter(t=>t.league===L&&t.name.toLowerCase().includes(query)).sort((a,b)=>a.name.localeCompare(b.name));$('teamcatalog').innerHTML=ts.length?ts.map(t=>`<div class="catalogitem ${t.id===selected?'active':''}">${team(t.id)}</div>`).join(''):'<span class="muted">검색 결과 없음</span>'}
function selectedGames(id){let ms=filterHistory(id,games(id,$('season').value)),range=$('rangefilter').value,error='';if(range==='custom'){let start=$('startdate').value,end=$('enddate').value;if(start&&end&&start>end){error='시작 날짜는 종료 날짜보다 앞서야 합니다.';ms=[]}else ms=ms.filter(m=>(!start||m.date>=start)&&(!end||m.date<=end))}else if(range==='5'||range==='10')ms=ms.slice(-Number(range));$('filtererror').textContent=error;return ms}
function scopeText(){let range=$('rangefilter').value,venue=$('venue').value,result=$('resultfilter').value;return [range==='season'?'시즌 전체':range==='custom'?'선택 기간':`최근 ${range}경기`,{all:'전체 장소',home:'홈',away:'원정'}[venue],{all:'전체 결과',win:'승리',draw:'무승부',loss:'패배'}[result]].join(' · ')}
function sumDetail(id,ms,key){let vals=ms.map(m=>D.match_detail[id+'|'+m.id]?.[key]).filter(v=>v!==null&&v!==undefined);return vals.length===ms.length&&ms.length?vals.reduce((s,v)=>s+v,0):null}
function detailedMatchStats(id,ms){let rows=[['페널티 제외 기대 득점','npxg_for'],['페널티 제외 기대 실점','npxg_against'],['기대 승점','expected_points'],['Deep (원본 지표)','deep'],['Deep 허용 (원본 지표)','deep_allowed']].map(([label,key])=>{let v=sumDetail(id,ms,key);return `<div class="metriccard"><label>${label}</label><strong>${v===null?'—':v.toFixed(key.includes('deep')?0:2)}</strong><small>선택 ${ms.length}경기 합계</small></div>`});let numerator=sumDetail(id,ms,'ppda_att'),denominator=sumDetail(id,ms,'ppda_def'),ratio=numerator!==null&&denominator>0?numerator/denominator:null;rows.push(`<div class="metriccard"><label>PPDA · 합산 비율</label><strong>${ratio===null?'—':ratio.toFixed(2)}</strong><small>원본 att 합 / def 합</small></div>`);return `<div class="scope"><h3>선택 경기 상세 지표</h3><span class="status">Understat · ${ms.length}경기</span></div><div class="metricgrid">${rows.join('')}</div>`}
function renderSnapshot(){let id=$('teamselect').value,season=$('season').value,snap=D.snapshots[id+'|'+season],group=$('metricgroup').value,q=$('metricsearch').value.trim().toLowerCase();if(!snap){$('snapshotstats').innerHTML='<p class="muted">해당 팀·시즌의 상세 자료 없음</p>';$('snapcount').textContent='자료 없음';$('snapshotprovenance').textContent='';return}let entries=Object.entries(snap.values).filter(([code,v])=>{let meta=D.metric_meta[code];return (group==='all'||meta.category===group)&&(!q||code.toLowerCase().includes(q)||meta.label.toLowerCase().includes(q))});$('snapcount').textContent=entries.length+' / '+Object.keys(snap.values).length+'지표';$('snapshotstats').innerHTML=entries.length?entries.map(([code,v])=>{let meta=D.metric_meta[code];return `<div class="metriccard"><label>${esc(meta.label)}</label><strong>${v===null?'—':(Number.isInteger(v)?v:v.toFixed(2))}${v!==null&&meta.unit==='%'?'%':''}</strong><small>${esc(code)} · ${meta.unit}</small></div>`}).join(''):'<p class="muted">선택 조건의 지표 없음</p>';$('snapshotprovenance').innerHTML=`${season} 시즌 원본 값 · 수집 ${esc(snap.observed)}<br><a href="${esc(snap.source)}" target="_blank" rel="noopener">StatMuse 원본 보기</a>`}
function refreshTeam(){updateTeam();renderSnapshot();renderCatalog()}
function syncRange(){let custom=$('rangefilter').value==='custom';$('startdate').disabled=!custom;$('enddate').disabled=!custom;refreshTeam()}
'''
page=page.replace('function updateTeam(){',js+'function updateTeam(){',1)
needle="season=$('season').value,ms=games(id,season),s=calc(id,ms)"
assert needle in page
page=page.replace(needle,"season=$('season').value,ms=selectedGames(id),s=calc(id,ms)",1)
page=page.replace('<span class="status">리그 기록</span>','<span class="status">${scopeText()}</span>',1)
page=page.replace('${teamOverview(id,ms)}<details','${teamOverview(id,ms)}${detailedMatchStats(id,ms)}<details',1)
page=page.replace("$('resultfilter').value='all';updateTeam()})}","$('resultfilter').value='all';refreshTeam()})}",1)
page=page.replace("$('teamselect').value=id;updateTeam()}","$('teamselect').value=id;refreshTeam()}",1)
page=page.replace("else $('teamselect').value=L==='EPL'?'understat:83':'understat:148';updateTeam()}","else $('teamselect').value=L==='EPL'?'understat:83':'understat:148';refreshTeam()}",1)
needle="$('teamselect').onchange=()=>{$('venue').value='all';$('resultfilter').value='all';updateTeam()};$('season').onchange=updateTeam;$('venue').onchange=updateTeam;$('resultfilter').onchange=updateTeam;"
assert needle in page
page=page.replace(needle,"$('teamselect').onchange=()=>{$('venue').value='all';$('resultfilter').value='all';refreshTeam()};$('season').onchange=()=>{$('rangefilter').value='season';$('startdate').value='';$('enddate').value='';syncRange()};$('venue').onchange=refreshTeam;$('resultfilter').onchange=refreshTeam;$('rangefilter').onchange=syncRange;$('startdate').onchange=refreshTeam;$('enddate').onchange=refreshTeam;$('metricgroup').onchange=renderSnapshot;$('metricsearch').oninput=renderSnapshot;$('teamsearch').oninput=renderCatalog;")
page=page.replace('ms.slice(-5),r=calc(id,recent)','ms.slice(-5),r=calc(id,recent)')
page=page.replace('<h3>최근 ${r.n}경기</h3>','<h3>선택 조건 · 최근 ${r.n}경기</h3>',1)
page=page.replace('<h3>시즌 공격·수비</h3>','<h3>선택 경기 공격·수비</h3>',1)
page=page.replace('선택한 시즌의 리그 자료가 없습니다','선택 조건의 리그 자료가 없습니다')
page=page.replace('선택시즌 전체','선택조건 전체')
with (out/'index.html').open('x',encoding='utf-8') as f:f.write(page)
manifest=dict(match_rows=len(match_rows),snapshot_rows=len(snapshots),statmuse_fields=len(stat_fields),fields=stat_fields,source_hashes={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in ['team_match_stats.csv','team_season_additional_stats.csv']},policy='Match filters apply to Understat; StatMuse values remain full selected-season snapshot, never converted to filtered match totals.')
with (out/'data-manifest.json').open('x',encoding='utf-8') as f:json.dump(manifest,f,ensure_ascii=False,indent=2)
test=(project/'visualization-design-2026-10-06-v05/check.cjs').read_text(encoding='utf-8')
test=test.replace("get('resultfilter').value='all';","get('resultfilter').value='all';get('rangefilter').value='season';get('metricgroup').value='all';",1)
test=test.replace('선택한 시즌의 리그 자료가 없습니다','선택 조건의 리그 자료가 없습니다').replace('시즌 공격·수비','선택 경기 공격·수비')
# When filtering to home matches, the selected summary denominator is also 19.
test=test.replace("'19 / 38경기'","'19 / 19경기'")
extra=r'''
test('team catalog contains league clubs and search narrows list',()=>{get('teamsearch').value='Arsenal';get('teamsearch').oninput();assert(get('teamcatalog').innerHTML.includes('Arsenal'));assert(!get('teamcatalog').innerHTML.includes('Liverpool'));get('teamsearch').value='';get('teamsearch').oninput()});
test('all 47 collected snapshot metrics exposed, category and text search work',()=>{run('openTeam("understat:83")');get('season').value='2023/24';get('season').onchange();assert.strictEqual(Object.keys(data.snapshots['understat:83|2023/24'].values).length,47);assert(get('snapcount').textContent.includes('47 / 47'));get('metricgroup').value='passing';get('metricgroup').onchange();assert(get('snapshotstats').innerHTML.includes('패스 성공률'));assert(!get('snapshotstats').innerHTML.includes('유효 슈팅'));get('metricsearch').value='PASS%';get('metricsearch').oninput();assert(get('snapcount').textContent.includes('1 / 47'));get('metricgroup').value='all';get('metricsearch').value='';run('renderSnapshot()')});
test('recent and custom-date filters change match summaries and detail totals',()=>{get('rangefilter').value='5';get('rangefilter').onchange();assert.strictEqual(run('selectedGames("understat:83").length'),5);get('rangefilter').value='custom';get('rangefilter').onchange();get('startdate').value='2023-08-01';get('enddate').value='2023-08-31';get('enddate').onchange();let ms=run('selectedGames("understat:83")');assert(ms.length>0);assert(ms.every(m=>m.date>='2023-08-01'&&m.date<='2023-08-31'));let expected=ms.reduce((s,m)=>s+data.match_detail['understat:83|'+m.id].npxg_for,0);assert(Math.abs(run('sumDetail("understat:83",selectedGames("understat:83"),"npxg_for")')-expected)<1e-8)});
test('season snapshot does not silently change under match filters',()=>{let expected=data.snapshots['understat:83|2023/24'].values.SH;assert.strictEqual(run('D.snapshots["understat:83|2023/24"].values.SH'),expected);const before=get('snapshotstats').innerHTML;get('venue').value='away';get('venue').onchange();assert.strictEqual(get('snapshotstats').innerHTML,before);assert(html.includes('期間')===false);assert(html.includes('기간/장소/결과 필터 미적용'))});
test('invalid dates are explicit and missing period is not zero statistics',()=>{get('startdate').value='2023-09-01';get('enddate').value='2023-08-01';get('enddate').onchange();assert(get('filtererror').textContent.includes('시작 날짜'));assert.strictEqual(run('selectedGames("understat:83").length'),0);assert.strictEqual(run('sumDetail("understat:83",[],"npxg_for")'),null);assert(!get('teamcontent').innerHTML.includes('NaN'))});
test('ratio aggregation and missing values preserve meaning',()=>{assert(run('detailedMatchStats("understat:83",[])').includes('—'));assert(run('detailedMatchStats("understat:83",games("understat:83","2023/24"))').includes('PPDA · 합산 비율'));assert.strictEqual(data.metric_meta['POSS%'].unit,'%');assert.strictEqual(data.metric_meta['PASS/M'].unit,'경기당')});
'''
test=test.replace("fs.writeFileSync(__dirname+'/logic-check.json'",extra+"\nfs.writeFileSync(__dirname+'/logic-check.json'")
with (out/'check.cjs').open('x',encoding='utf-8') as f:f.write(test)
print(json.dumps(manifest,ensure_ascii=False))
