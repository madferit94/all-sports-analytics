from pathlib import Path
import json

p=Path(__file__).resolve().parents[1]
repo=p.parents[1]
archive=p/'docs/publication_manifest-0.3.0.json'
if not archive.exists():archive.write_bytes((p/'publication_manifest.json').read_bytes())
(p/'VERSION').write_text('0.4.0\n',encoding='utf8')
(p/'viewer_selection.json').write_text(json.dumps(dict(release='0.4.0',functional_viewer='index.html',adopted_design='pixel',versioned_viewer='visualization-design-2026-10-06-v15/index.html',soft_preview='visualization-design-2026-10-06-v13/index.html',previous_pixel_preview='visualization-design-2026-10-06-v14/index.html',design_acceptance='adopted_by_user',administrator_authentication=False,model_adopted=False),indent=2)+'\n',encoding='utf8')
for name in ['README.md','README.ko.md']:
    f=p/name;s=f.read_text(encoding='utf8')
    s=s.replace('Release 0.3.0','Release 0.4.0').replace('버전 0.3.0','버전 0.4.0')
    s=s.replace('[Current functional viewer — v12](visualization-design-2026-10-06-v12/index.html)','[Open MatchDesk — adopted 8-bit design](index.html) · [versioned v15](visualization-design-2026-10-06-v15/index.html)')
    s=s.replace('[기능 개선 완료 화면 — v12](visualization-design-2026-10-06-v12/index.html)','[MatchDesk 기본 화면 — 채택된 8비트 디자인](index.html) · [v15 버전](visualization-design-2026-10-06-v15/index.html)')
    s=s.replace('They are previews awaiting human design acceptance, not completed browser-rendering certification.','The user adopted the 8-bit design in 0.4.0. All 56 club logos now render from their original images onto 24×24 grids with crisp enlargement and an initials fallback. Real-browser rendering quality remains unverified.')
    s=s.replace('두 디자인 예시는 같은 자료와 기능을 유지합니다. 실제 브라우저 화면 검사와 사용자의 디자인 확정은 아직 남아 있습니다.','8비트 디자인은 사용자 선택으로 기본 화면에 채택했습니다. 56개 팀 로고를 원본 비율의 24×24 격자에 표시하고 확대 시 픽셀 느낌을 줍니다. 로딩 실패 시 팀 약자가 표시됩니다. 실제 브라우저에서의 시각적 품질 확인은 아직 남아 있습니다.')
    s=s.replace('node visualization-design-2026-10-06-v14/check.cjs','node visualization-design-2026-10-06-v15/check.cjs')
    s=s.replace('Node runs 36','Node runs 40').replace('말풍선 36항목','말풍선과 로고 렌더링 40항목')
    s=s.replace('remote logo/font loading and user acceptance are pending','remote logo/font loading and visual verification are pending; design adoption was explicitly confirmed')
    s=s.replace('외부 로고/글꼴 로딩·참가자 확인은 별도이며 미확인입니다','외부 로고/글꼴 로딩·시각적 품질 확인은 별도이며 미확인입니다')
    s=s.replace('[Release SPEC](docs/SPEC-0.3.0.md)','[Release SPEC](docs/SPEC-0.4.0.md) · [0.3.0 SPEC](docs/SPEC-0.3.0.md)')
    s=s.replace('[요구사항·검증 SPEC](docs/SPEC-0.3.0.md)','[요구사항·검증 SPEC](docs/SPEC-0.4.0.md) · [0.3.0 SPEC](docs/SPEC-0.3.0.md)')
    s=s.replace('UI v01–v14 are preserved development revisions within semantic release 0.3.0.','UI v01–v15 are preserved. Release 0.4.0 adopts v15 as the canonical index.html; archived v13/v14 remain design history.')
    s=s.replace('화면 v01~v14는 보존된 개발 버전이며 이번 기능 묶음의 버전은 0.3.0입니다.','화면 v01~v15를 보존하며 이번 버전은 0.4.0입니다. 기본 index.html은 채택된 v15와 동일합니다.')
    s=s.rstrip()+'\n| [v15](visualization-design-2026-10-06-v15/index.html) | '+('Adopt pixel design; render all club logos on 24×24 grids' if name=='README.md' else '8비트 기본 디자인 채택·팀 로고 픽셀 표시')+' |\n'
    f.write_text(s,encoding='utf8')
for name in ['README.md','README.ko.md']:
    f=repo/name;s=f.read_text(encoding='utf8')
    s=s.replace('MatchDesk football agent project · 0.3.0','MatchDesk football agent project · 0.4.0').replace('MatchDesk AI 경기 분석실 · 0.3.0','MatchDesk AI 경기 분석실 · 0.4.0')
    s=s.replace('football/matchdesk-ai-agents/docs/SPEC-0.3.0.md','football/matchdesk-ai-agents/docs/SPEC-0.4.0.md')
    s=s.replace('[8-bit HTML preview](football/matchdesk-ai-agents/visualization-design-2026-10-06-v14/index.html)','[Adopted 8-bit viewer](football/matchdesk-ai-agents/index.html)')
    s=s.replace('[8비트 HTML 미리보기](football/matchdesk-ai-agents/visualization-design-2026-10-06-v14/index.html)','[채택된 8비트 기본 화면](football/matchdesk-ai-agents/index.html)')
    s=s.replace('filters and two design previews','filters and an adopted pixel interface').replace('필터·디자인 예시를 제공합니다','필터·채택된 8비트 화면을 제공합니다')
    f.write_text(s,encoding='utf8')
f=p/'CHANGELOG.md';s=f.read_text(encoding='utf8')
s=s.replace('# Release history / 변경 이력','# Release history / 변경 이력\n\n## 0.4.0 — 2026-10-06\n\n- Adopt the 8-bit design as the canonical index.html and preserve v15.\n- Render original logos for all 56 teams onto 24×24 grids, reuse loads, retain aspect ratios and fall back to initials on image/canvas failures. No logo raster files are rewritten.\n- Update bilingual READMEs, selection, SPEC and hashes; preserve earlier design previews.\n- 8비트 디자인을 기본 화면으로 채택. 56개 원본 팀 로고의 픽셀 표시·비율 유지·로딩 재사용·실패 대체 처리. 자료/모델 변경과 웹 호스팅 없음.\n- Node VM: 40 checks passed; actual browser rendering and visual quality confirmation remain pending.',1)
f.write_text(s,encoding='utf8')
f=p/'docs/VERSIONING.md';s=f.read_text(encoding='utf8').replace('current version is0.3.0','current version is0.4.0')
s+='\n## 0.4.0 adopted design\n\nThe user adopted the pixel design. index.html is identical to v15, and viewer_selection.json points to it. v13/v14 stay preserved previews, not the current entry. docs/publication_manifest-0.3.0.json preserves the preceding release. No repository-wide tag is used in this multi-project repository.\n'
f.write_text(s,encoding='utf8')
f=p/'tools/check_release.py';s=f.read_text(encoding='utf8')
s=s.replace("p/'docs/SPEC-0.3.0.md'","p/'docs/SPEC-0.4.0.md'")
s=s.replace("payload('v12')==payload('v13')==payload('v14')","payload('v12')==payload('v13')==payload('v14')==payload('v15')")
s=s.replace("p/'docs/publication_manifest-0.2.1.json'","p/'docs/publication_manifest-0.3.0.json'")
s=s.replace("else '0.3.0'","else '0.4.0'")
s=s.replace("manifest=dict(version='0.3.0'","manifest=dict(version='0.4.0'")
s=s.replace("old=json.loads", "assert (p/'index.html').read_bytes()==(p/'visualization-design-2026-10-06-v15/index.html').read_bytes(), 'Default entry differs from adopted v15'\nold=json.loads")
f.write_text(s,encoding='utf8')
record=dict(release='0.4.0',date='2026-10-06',pixel_viewer_node_vm_checks=40,failures=0,design_acceptance='adopted_by_user',real_browser_rendering_verified=False,real_logo_loading_verified=False,notes='40 Node VM checks executed locally; Image/canvas are stubs. Unchanged agent/model checks remain preserved in release-checks-0.3.0.json.')
(p/'docs/release-checks-0.4.0.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8')
print('Prepared release 0.4.0 documentation and adopted viewer selection.')
