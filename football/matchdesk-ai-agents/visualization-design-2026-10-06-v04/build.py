"""Add observed remote crest URLs and navigable historical records; preserve v03."""
import base64
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

OUT = Path(__file__).resolve().parent
PROJECT = OUT.parent
BASE = OUT.parents[3]
old = (PROJECT/'visualization-design-2026-10-06-v03/index.html').read_text(encoding='utf-8')
payload = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',old,re.S)[1])
teams = payload['teams']
found = {}
special = {'arsenal_overview.html':'83','barcelona_overview.html':'148','leeds_overview.html':'245','real_madrid_overview.html':'150'}
for directory in sorted(BASE.iterdir()):
    if not directory.is_dir() or directory.name.startswith('github-'):
        continue
    for path in sorted(directory.rglob('*.html')):
        match = re.search(r'(?:EPL|La_liga)_\d{4}_(\d+)_overview|(?:statmuse_)?understat_(\d+)(?:_overview)?',path.name)
        tid = next((x for x in match.groups() if x),None) if match else special.get(path.name)
        if not tid or 'understat:'+tid not in teams:
            continue
        text = path.read_text(encoding='utf-8',errors='replace')
        image = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"',text)
        canonical = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',text)
        title = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"',text)
        if not image or not canonical or not title:
            continue
        link = html.unescape(image[1])
        if '/forge-v2/' not in link:
            continue
        token = link.split('/forge-v2/',1)[1].split('.png',1)[0]
        try:
            decoded = base64.urlsafe_b64decode(token + '='*((-len(token))%4)).decode()
        except (ValueError,UnicodeError):
            continue
        parts = urlsplit(decoded)
        observed_exceptions = {'78':'a-min--w7gbwxec.png','231':'shield-of-real-valladolid---ecoex2o.png','137':'ma-laga-cf-svg--sg_ylrqg.png'}
        if parts.scheme!='https' or parts.netloc!='cdn.statmuse.com' or not ('logo' in parts.path.lower() or parts.path.endswith(observed_exceptions.get(tid,'__not_a_logo__'))):
            continue
        logo = 'https://cdn.statmuse.com'+parts.path
        found['understat:'+tid] = dict(url=logo,source_page=html.unescape(canonical[1]),source_title=html.unescape(title[1]),
                                       observed_file=str(path.relative_to(BASE)).replace('\\','/'),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                       evidence='Decoded original logo URL from observed StatMuse og:image; no downloaded image or visual identity verification')
for tid, team in teams.items():
    team['logo'] = found[tid]['url'] if tid in found else None
manifest = dict(provider='StatMuse CDN, addresses observed in preserved source pages',observed=len(found),total=len(teams),missing=[t['name'] for tid,t in teams.items() if tid not in found],
                availability='Remote load not yet verified; image failure falls back to team initials',logos=found)
with (OUT/'logo-manifest-v02.json').open('x',encoding='utf-8') as f:json.dump(manifest,f,ensure_ascii=False,indent=2)

style = '''<style>
.logolink{display:inline-flex;align-items:center;justify-content:center;border-radius:8px;text-decoration:none;color:inherit;flex-shrink:0;min-width:44px;min-height:44px;background:#fff;border:1px solid #dce2e9;transition:box-shadow .15s}.logolink:hover{box-shadow:0 0 0 2px #c7d2e1}.logolink.big{min-width:66px;min-height:72px;border-bottom:3px solid var(--accent)}.logoimg{object-fit:contain;width:30px;height:30px;padding:2px}.big .logoimg{width:54px;height:60px;padding:5px}.logofallback{font-size:12px;font-weight:750;padding:8px}.logofallback[hidden]{display:none}.big .logofallback{font-size:20px}.fixture-top{display:flex;justify-content:space-between;align-items:center}.openmatch{padding:7px 12px;min-height:44px;background:#f1f4f8;border:0;border-radius:6px;font-size:13px;color:#314255}.seasonbutton{border:0;background:none;color:#2454c6;text-decoration:underline;padding:10px 5px;min-height:44px}.selectedseason{background:#f1f5fb}.historyfilters{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}.historyfilters label{font-size:14px;color:#536174}.splitstats{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:22px 0}.splitstats>div{border:1px solid #e1e6ed;border-radius:9px;padding:16px}.splitstats strong{display:block;font-size:21px}.timeline-title{display:flex;justify-content:space-between;align-items:center;margin:26px 0 12px}.historyname{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}.teamheader h2{font-size:26px;margin:0}.seasontrend{display:flex;align-items:end;gap:12px;height:130px;margin:20px 0 8px;padding:0 12px}.seasoncolumn{flex:1;text-align:center}.seasoncolumn .stick{height:var(--height);min-height:2px;background:var(--colour);border-radius:5px 5px 0 0;border:1px solid #17283b25}.seasoncolumn small{font-size:12px;color:#536174}.historytoolbar{display:flex;gap:10px;align-items:center;margin-bottom:18px;flex-wrap:wrap}@media(max-width:750px){.splitstats{grid-template-columns:1fr}.logolink.big{min-width:48px;min-height:54px}.big .logoimg{width:42px;height:46px}.historyname{align-items:flex-start}}
</style>'''
old = old.replace('</head>',style+'</head>')
old = re.sub(r'<script id="data" type="application/json">.*?</script>',lambda _: '<script id="data" type="application/json">'+json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>',old,flags=re.S)
badge = '''function badge(id,big=false){const t=T[id],initials=esc(t.name.split(' ').map(x=>x[0]).join('').slice(0,3));return `<a class="logolink ${big?'big':''}" href="#team=${encodeURIComponent(id)}" data-team="${id}" aria-label="${esc(t.name)} 과거 기록 보기" style="--accent:${colour(id)}">${t.logo?`<img class="logoimg" src="${esc(t.logo)}" alt="" width="${big?54:30}" height="${big?60:30}" loading="lazy" referrerpolicy="no-referrer" onerror="this.hidden=true;this.nextElementSibling.hidden=false">`:''}<span class="logofallback" ${t.logo?'hidden':''}>${initials}</span></a>`}'''
old, n = re.subn(r'function badge\(id,big=false\).*?\nfunction team',lambda _:badge+'\nfunction team',old,flags=re.S)
assert n==1
start = '<button class="fixture ${m.id===selected.id?\'selected\':\'\'}" data-id="${m.id}" aria-pressed="${m.id===selected.id}"><span class="muted">${m.date}</span><div class="pair">${team(m.home)}<span class="muted">vs</span>${team(m.away)}</div></button>'
end = '<article class="fixture ${m.id===selected.id?\'selected\':\'\'}"><div class="fixture-top"><span class="muted">${m.date}</span><button class="openmatch" data-id="${m.id}" aria-pressed="${m.id===selected.id}">분석</button></div><div class="pair">${team(m.home)}<span class="muted">vs</span>${team(m.away)}</div></article>'
assert start in old
old = old.replace(start,end)
old = old.replace('<label>시즌 <select id="season">','<label>시즌 <select id="season">')
old = old.replace('</select></label></div><article class="panel" id="teamcontent">','</select></label><label>장소 <select id="venue"><option value="all">전체</option><option value="home">홈</option><option value="away">원정</option></select></label><label>결과 <select id="resultfilter"><option value="all">전체</option><option value="win">승리</option><option value="draw">무승부</option><option value="loss">패배</option></select></label></div><article class="panel" id="teamcontent">')
update = r'''function historyRows(id,ms){return `<div class="tablewrap"><table><thead><tr><th>날짜 / 상대</th><th>장소</th><th>결과</th><th>xG</th><th>상대 xG</th></tr></thead><tbody>${ms.slice().reverse().map(m=>{let h=m.home===id,opp=h?m.away:m.home,f=h?m.hg:m.ag,a=h?m.ag:m.hg;return `<tr><td>${team(opp)}<small class="muted">${m.date}</small></td><td>${h?'홈':'원정'}</td><td><a href="${m.source}" target="_blank" rel="noopener" aria-label="${m.date} 원본 경기 보기">${f>a?'승':f===a?'무':'패'} ${f} : ${a}</a></td><td>${(h?m.hx:m.ax).toFixed(2)}</td><td>${(h?m.ax:m.hx).toFixed(2)}</td></tr>`}).join('')}</tbody></table></div>`}
function filterHistory(id,ms){let venue=$('venue').value,result=$('resultfilter').value;return ms.filter(m=>{let h=m.home===id,f=h?m.hg:m.ag,a=h?m.ag:m.hg;return (venue==='all'||(venue==='home'?h:!h))&&(result==='all'||(result==='win'?f>a:result==='draw'?f===a:f<a))})}
function updateTeam(){let id=$('teamselect').value,season=$('season').value,ms=games(id,season),s=calc(id,ms),seasons=['2023/24','2024/25','2025/26','2026/27'],summaries=seasons.map(year=>({year,...calc(id,games(id,year))})),filtered=filterHistory(id,ms),home=calc(id,ms.filter(m=>m.home===id)),away=calc(id,ms.filter(m=>m.away===id));let maxRate=Math.max(1,...summaries.filter(v=>v.n).map(v=>v.p/v.n));
$('teamcontent').innerHTML=`<div class="historyname"><div class="club teamheader">${badge(id,true)}<div><h2>${esc(T[id].name)}</h2><span class="muted">${L==='EPL'?'프리미어리그':'라리가'} · ${season}</span></div></div><span class="status">리그 기록</span></div>${s.n?`<div class="summary"><div><strong>${s.n}</strong><label>경기</label></div><div><strong>${s.p}</strong><label>승점</label></div><div><strong>${s.w} / ${s.d} / ${s.l}</strong><label>승 / 무 / 패</label></div><div><strong>${s.gf} : ${s.ga}</strong><label>득점 / 실점</label></div></div><div class="splitstats">${[['홈',home],['원정',away]].map(([label,v])=>`<div><h3>${label} · ${v.n}경기</h3><strong>${v.w}승 ${v.d}무 ${v.l}패</strong><span class="muted">경기당 승점 ${v.n?(v.p/v.n).toFixed(2):'—'} · xG ${v.n?(v.xg/v.n).toFixed(2):'—'}</span></div>`).join('')}</div>`:'<p class="muted">선택한 시즌의 리그 자료가 없습니다.</p>'}<div class="timeline-title"><h3>시즌별 기록</h3><span class="muted">경기당 승점</span></div><div class="seasontrend" role="img" aria-label="시즌별 경기당 승점, 상세 수치는 아래 표에 표시">${summaries.map(v=>`<div class="seasoncolumn"><small>${v.n?(v.p/v.n).toFixed(2):'—'}</small><div class="stick" style="--height:${v.n?(v.p/v.n)/maxRate*90:2}px;--colour:${colour(id)}"></div><small>${v.year}</small></div>`).join('')}</div><div class="tablewrap"><table><thead><tr><th>시즌</th><th>경기</th><th>승·무·패</th><th>득실점</th><th>승점</th><th>경기당 xG</th></tr></thead><tbody>${summaries.map(v=>`<tr class="${v.year===season?'selectedseason':''}"><td><button class="seasonbutton" data-season="${v.year}" aria-label="${v.year} 경기 기록 보기">${v.year}</button></td><td>${v.n||'—'}</td><td>${v.n?`${v.w}·${v.d}·${v.l}`:'—'}</td><td>${v.n?`${v.gf}:${v.ga}`:'—'}</td><td>${v.n?v.p:'—'}</td><td>${v.n?(v.xg/v.n).toFixed(2):'—'}</td></tr>`).join('')}</tbody></table></div><p class="note">2026/27은 진행 중 · 자료 없는 시즌은 — 표시</p><div class="timeline-title"><h3>경기 기록</h3><span class="muted">${filtered.length} / ${ms.length}경기</span></div>${filtered.length?historyRows(id,filtered):'<p class="muted">선택 조건의 경기가 없습니다.</p>'}`;
$('teamcontent').querySelectorAll('[data-season]').forEach(b=>b.onclick=()=>{$('season').value=b.dataset.season;$('venue').value='all';$('resultfilter').value='all';updateTeam()})}
function openTeam(id){if(!T[id])return;L=T[id].league;V='team';$('league').value=L;$('venue').value='all';$('resultfilter').value='all';render();$('teamselect').value=id;updateTeam()}
'''
old,n=re.subn(r'function updateTeam\(\).*?\nfunction renderLeague',lambda _:update+'function renderLeague',old,flags=re.S)
assert n==1
old=old.replace("$('teamselect').onchange=updateTeam;$('season').onchange=updateTeam;", "$('teamselect').onchange=()=>{$('venue').value='all';$('resultfilter').value='all';updateTeam()};$('season').onchange=updateTeam;$('venue').onchange=updateTeam;$('resultfilter').onchange=updateTeam;")
navigation = r'''
document.addEventListener('click',event=>{const link=event.target.closest('[data-team]');if(!link)return;event.preventDefault();openTeam(link.dataset.team);const hash='#team='+encodeURIComponent(link.dataset.team);if(window.location.hash!==hash)window.location.hash=hash});
function readTeamHash(){if(!window.location.hash.startsWith('#team='))return;try{openTeam(decodeURIComponent(window.location.hash.slice(6)))}catch(error){}}
window.addEventListener('hashchange',readTeamHash);readTeamHash();
'''
old=old.replace('</script></body>',navigation+'</script></body>')
old=old.replace('팀 색상은 화면용 대표색','구단 로고: StatMuse · 시즌 기록은 수집 리그 범위')
assert '사이트 디자인 기준' not in old
with (OUT/'index-v02.html').open('x',encoding='utf-8') as f:f.write(old)
print(json.dumps(dict(logo_urls=len(found),teams=len(teams),missing=manifest['missing'],source='preserved pages; remote logo rendering unverified'),ensure_ascii=False))
