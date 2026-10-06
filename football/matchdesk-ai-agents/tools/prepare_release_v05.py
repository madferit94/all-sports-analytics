"""One-time documentation update for the bilingual pixel release."""
from pathlib import Path
import json
p=Path(__file__).resolve().parents[1];repo=p.parents[1]
archive=p/'docs/publication_manifest-0.4.0.json'
assert not archive.exists(), 'Release preparation already performed'
archive.write_bytes((p/'publication_manifest.json').read_bytes())
(p/'VERSION').write_text('0.5.0\n',encoding='utf8')
selection=json.loads((p/'viewer_selection.json').read_text(encoding='utf8'))
selection.update(release='0.5.0',versioned_viewer='visualization-design-2026-10-06-v16/index.html',english_viewer='index.en.html',languages=['ko','en'],club_coverage={'EPL':27,'La_liga':29})
(p/'viewer_selection.json').write_text(json.dumps(selection,indent=2)+'\n',encoding='utf8')
for name in ['README.md','README.ko.md']:
 f=p/name;s=f.read_text(encoding='utf8')
 s=s.replace('Release 0.4.0','Release 0.5.0').replace('버전 0.4.0','버전 0.5.0')
 s=s.replace('versioned v15](visualization-design-2026-10-06-v15/index.html)','versioned v16](visualization-design-2026-10-06-v16/index.html)')
 s=s.replace('v15 버전](visualization-design-2026-10-06-v15/index.html)','v16 버전](visualization-design-2026-10-06-v16/index.html)')
 s=s.replace('docs/SPEC-0.4.0.md','docs/SPEC-0.5.0.md')
 s=s.replace('node visualization-design-2026-10-06-v15/check.cjs','node visualization-design-2026-10-06-v16/check.cjs\nnode visualization-design-2026-10-06-v16/check-en.cjs')
 s=s.replace('Search accepts Korean labels or original codes.','Search accepts the selected language’s labels, descriptions or original codes.')
 s=s.replace('UI v01–v15 are preserved. Release 0.4.0 adopts v15 as the canonical index.html; archived v13/v14 remain design history.','UI v01–v16 are preserved. Release 0.5.0 provides Korean index.html and English index.en.html identical to their v16 snapshots; earlier designs remain history.')
 s=s.replace('화면 v01~v15를 보존하며 이번 버전은 0.4.0입니다. 기본 index.html은 채택된 v15와 동일합니다.','화면 v01~v16을 보존하며 이번 버전은 0.5.0입니다. 한국어 index.html과 영어 index.en.html은 v16의 각 언어 화면과 동일합니다.')
 note=('\n- [English site](index.en.html) · [Korean site](index.html): full UI, 47 metric definitions and reading tips. Premier League 27 / LaLiga 29 clubs include historical teams. Header language links retain the selected team route; other filters reset when switching. 40 Korean + 15 English Node VM checks passed; real browser rendering remains unverified.\n' if name=='README.md' else '\n- [영어 사이트](index.en.html) · [한국어 사이트](index.html): 메뉴·필터·47개 지표 이름·의미·읽는 법을 번역했습니다. 프리미어리그 27개·라리가 29개는 과거 시즌 팀을 포함한 수입니다. 상단 언어 전환 시 선택 팀 주소는 유지되고 나머지 필터는 초기화됩니다. 한국어 40개·영어 15개 코드 동작 검사 통과. 실제 브라우저 화면은 확인 전입니다.\n')
 s=s.replace('## Open a viewer','## Open a viewer'+note) if name=='README.md' else s.replace('## 화면 열기','## 화면 열기'+note)
 if note.strip() not in s:s=s.replace('\n## ',note+'\n## ',1)
 s=s.rstrip()+'\n| [v16](visualization-design-2026-10-06-v16/index.html) · [English](visualization-design-2026-10-06-v16/index.en.html) | '+('Bilingual pixel UI, 47 English metric explanations, language switch' if name=='README.md' else '한·영 8비트 화면·47개 영어 지표 설명·언어 전환')+' |\n'
 f.write_text(s,encoding='utf8')
for name in ['README.md','README.ko.md']:
 f=repo/name;s=f.read_text(encoding='utf8').replace('MatchDesk football agent project · 0.4.0','MatchDesk football agent project · 0.5.0').replace('MatchDesk AI 경기 분석실 · 0.4.0','MatchDesk AI 경기 분석실 · 0.5.0').replace('football/matchdesk-ai-agents/docs/SPEC-0.4.0.md','football/matchdesk-ai-agents/docs/SPEC-0.5.0.md')
 marker='[English MatchDesk site](football/matchdesk-ai-agents/index.en.html)' if name=='README.md' else '[MatchDesk 영어 화면](football/matchdesk-ai-agents/index.en.html)'
 s=s.replace('\n## ', '\n'+marker+' · PL + LaLiga, 56 clubs, Korean/English UI.\n\n## ',1)
 f.write_text(s,encoding='utf8')
f=p/'CHANGELOG.md';s=f.read_text(encoding='utf8').replace('# Release history / 변경 이력','# Release history / 변경 이력\n\n## 0.5.0 — 2026-10-06\n\n- Add canonical English index.en.html alongside Korean index.html, preserving v16 in both languages.\n- Translate all UI, filters, 47 StatMuse metric labels/definitions, reading tips and accessibility labels. Language links preserve selected-team hashes; other filters reset.\n- Confirm 27 Premier League and 29 LaLiga historical/current clubs retain pixel logos and club colours. Statistical data and prediction adoption unchanged.\n- 한·영 화면과 지표 설명 제공, 선택 팀을 유지하는 언어 전환. 한국어 40개·영어 15개 코드 검사 통과. 실제 화면·참가자 확인 전.\n',1);f.write_text(s,encoding='utf8')
f=p/'docs/VERSIONING.md';s=f.read_text(encoding='utf8')+'\n## 0.5.0 bilingual interface\n\nBoth canonical language entries match the preserved v16 snapshots. The 0.4.0 manifest remains in docs/publication_manifest-0.4.0.json. English changes presentation metadata only, preserving all statistics.\n';f.write_text(s,encoding='utf8')
record=dict(release='0.5.0',date='2026-10-06',korean_node_vm_checks=40,english_node_vm_checks=15,failures=0,league_clubs={'EPL':27,'La_liga':29},translated_metrics=47,real_browser_rendering_verified=False,participant_confirmation='pending',method='Node VM DOM stubs, not actual browser rendering')
(p/'docs/release-checks-0.5.0.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8')
f=p/'tools/check_release.py';s=f.read_text(encoding='utf8').replace("p/'docs/SPEC-0.4.0.md'","p/'docs/SPEC-0.5.0.md'").replace("payload('v15'),","payload('v15')==payload('v16'),").replace("p/'visualization-design-2026-10-06-v15/index.html'","p/'visualization-design-2026-10-06-v16/index.html'").replace('adopted v15','adopted v16').replace("p/'docs/publication_manifest-0.3.0.json'","p/'docs/publication_manifest-0.4.0.json'").replace("else '0.4.0'","else '0.5.0'").replace("manifest=dict(version='0.4.0'","manifest=dict(version='0.5.0'")
extra="""
en_html=(p/'index.en.html').read_text(encoding='utf8')
assert (p/'index.en.html').read_bytes()==(p/'visualization-design-2026-10-06-v16/index.en.html').read_bytes()
english=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',en_html,re.S)[1])
korean=payload('v16')
for key in korean:
    if key!='metric_meta': assert korean[key]==english[key], f'English data drift: {key}'
assert len(english['metric_meta'])==47
assert not re.search('[가-힣]',re.sub(r'<script id="data" type="application/json">.*?</script>','',en_html,flags=re.S).replace('한국어',''))
"""
s=s.replace('old=json.loads',extra+'\nold=json.loads');f.write_text(s,encoding='utf8')
print('Prepared release 0.5.0 metadata; manifest audit follows.')
