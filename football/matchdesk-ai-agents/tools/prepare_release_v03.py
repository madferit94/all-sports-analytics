"""Prepare the user-authorized bilingual release docs and content manifest."""
from pathlib import Path
import hashlib,json,subprocess

p=Path(__file__).resolve().parents[1]
repo=p.parents[1]
archive=p/'docs/publication_manifest-0.2.1.json'
if not archive.exists(): archive.write_bytes((p/'publication_manifest.json').read_bytes())
history=[
('v01','Initial wireframes and coordinate audit','기본 설계·좌표 자료 확인'),
('v02','Site design system','사이트 디자인 기준'),
('v03','Visitor UI and team colours','이용자 화면·팀 색상'),
('v04','56 logos and season history','56개 로고·시즌 기록'),
('v05','Team-name routes and overview','팀 이름 연결·종합 정보'),
('v06','47 metrics and match filters','47개 지표·경기 필터'),
('v07','Long-label and card containment','긴 이름·카드 넘침 수정'),
('v08','Optional metric notes','설명 기본 숨김'),
('v09','Korean names and meanings','한글 지표 이름·뜻'),
('v10','Click-to-open explanations','클릭 말풍선·읽는 법'),
('v11','Source metadata separation','출처 관리 자료 분리'),
('v12','Remove external match links','외부 경기 링크 제거'),
('v13','Soft app preview','부드러운 앱 디자인 예시'),
('v14','Pixel clubhouse preview','8비트 디자인 미리보기')]
def table(ko):
    rows=['| UI version | Change / 변경 |','|---|---|']
    for v,en,kr in history:
        target=f'visualization-design-2026-10-06-{v}/'+('index-v02.html' if v=='v04' else 'index.html')
        rows.append(f'| [{v}]({target}) | {kr if ko else en} |')
    return '\n'.join(rows)
en='''# MatchDesk — Football Analytics Agent Team

[English](README.md) | [한국어](README.ko.md)

**Release 0.3.0 · 2026-10-06.** A provider-neutral five-agent project for football evidence, team analysis, interactive viewing, independent review and traceable decisions.

## Open a viewer

- [Current functional viewer — v12](visualization-design-2026-10-06-v12/index.html).
- [Soft app design preview — v13](visualization-design-2026-10-06-v13/index.html).
- [8-bit pixel clubhouse preview — v14](visualization-design-2026-10-06-v14/index.html).
- [Three design directions](design-candidates-2026-10-06-v01/index.html).

Download/open HTML locally; GitHub's source view does not run it. This release does not host a website. Choose Matches, Teams or League. Team names/logos open the team overview; metric names open a meaning/reading-tip bubble. Search accepts Korean labels or original codes. The source/collection panel and external match links are removed from v11/v12 onwards.

## What works, and what is pending

The viewers show PL/LaLiga history, selected-match summaries, recent xG, fixtures, season history, team search and filters. The pixel/soft designs retain the same data and behavior. They are previews awaiting human design acceptance, not completed browser-rendering certification.

The baseline prediction experiment is now archived in [modeling](modeling/README.md). Its new-season accuracy underperforms the comparison baseline; adoption remains **false**, and probabilities are not shown in the viewer. Automatic refresh, administrator authentication, prediction API, hosting and a new five-agent runtime run are not implemented. Claude runtime execution is unverified.

## Data scope

The HTML embeds **2,399 completed matches, 641 scheduled matches and 56 clubs**, plus 4,798 team-match detail records and 160 team-season snapshots with 47 StatMuse metrics. Completed totals: 760 in each of 2023/24–2025/26 and 119 in elapsed 2026/27. Last recorded completed date: **2026-09-20**. No refresh was performed for these design changes.

Understat is the core match/date/xG source; StatMuse supplies additional whole-season statistics. Date/venue/result filters apply to match data; StatMuse season totals are explicitly not filtered. Football-Data, odds and Champions League are excluded. No shot-coordinate dataset is available; the pixel pitch is decorative.

The published CSV package remains a **20-completed/2-scheduled demonstration subset**. Full training CSV and provider caches remain local; the larger HTML display data does not make the demo CSV a complete modeling corpus. Squad/value/news evidence has different observation dates and documented gaps.

## Five execution owners

| Agent | Responsibility |
|---|---|
| Director | Plan, assign, track and decide after independent review |
| Research | Collect matches, auxiliary evidence and team news |
| Analyst | Team comparison and experimental modeling |
| Builder | Viewer, chart and service implementation |
| Reviewer | Independent calculation, data and model checks |

[Five-agent package](agent-team-integrated-2026-10-06-v01/README.md) · [Preserved ten-role package](agent-team-2026-10-06-v01/README.md) · [Actual archived run](team-run-2026-10-06-v01/README.md).
The actual representative Arsenal–Leeds/Malaga–Espanyol run used the previous ten-role arrangement; it is not relabelled as a five-agent run. Reviewer and final director stay separate from authors and each other. Model adoption and business decisions remain with the human user.

## Verification and limitations

```sh
python -m unittest discover -s agent-team-2026-10-06-v01/tests -v
python -m unittest discover -s agent-team-integrated-2026-10-06-v01/tests -v
python -m unittest discover -s modeling/tests -v
node visualization-design-2026-10-06-v14/check.cjs
```

Python 3.11+ with the pinned NumPy requirement is needed for model tests; agent tests use the standard library. Node runs 36 calculation/navigation/interaction checks with a DOM stub. **Real-browser rendering, mobile touch, remote logo/font loading and user acceptance are pending.** A separate local source report is not an authenticated admin area. Historical snapshots still preserve earlier provenance. Team hex colours are UI choices, not verified official brand hex codes.

Archived run: 49 auxiliary entries (26 collected, 22 missing, 1 blocked), 117 squad players and 44 previous starters; an independent saved-input comparison recorded 271 checks. These verify scope and consistency, not every provider fact.

## Versions and specifications

[VERSION](VERSION) · [CHANGELOG](CHANGELOG.md) · [Release SPEC](docs/SPEC-0.3.0.md) · [Version policy](docs/VERSIONING.md) · [Current viewer selection](viewer_selection.json) · [Content hashes](publication_manifest.json).
UI v01–v14 are preserved development revisions within semantic release 0.3.0. Older references and the original 0.2.1 manifest remain available. Some archived build/review commands describe the original local environment; use the checked-in HTML or current checks rather than assuming every old generator is portable.

'''
ko='''# MatchDesk — AI 경기 분석실 에이전트 팀

[English](README.md) | [한국어](README.ko.md)

**버전 0.3.0 · 2026-10-06.** 축구 자료 수집·팀 분석·화면·독립 검증·최종 내부 판단을 연결하는 5인 에이전트 프로젝트입니다. AI 제공자와 모델은 고정하지 않습니다.

## 화면 열기

- [기능 개선 완료 화면 — v12](visualization-design-2026-10-06-v12/index.html)
- [부드러운 앱 디자인 예시 — v13](visualization-design-2026-10-06-v13/index.html)
- [8비트 게임 디자인 미리보기 — v14](visualization-design-2026-10-06-v14/index.html)
- [디자인 후보 3개 비교](design-candidates-2026-10-06-v01/index.html)

HTML을 내려받아 브라우저에서 엽니다. GitHub의 코드 보기에서는 실행되지 않으며 인터넷에 서비스로 올린 상태도 아닙니다. 경기·팀·리그 메뉴와 팀 이름/로고로 탐색하고, 지표 이름을 누르면 뜻과 읽는 법이 열립니다. 한글 이름과 원본 약어 모두 검색할 수 있습니다. v11부터 출처·수집 시점 영역을 제거했고 v12부터 외부 경기 링크를 제거했습니다.

## 구현한 것과 남은 것

팀별 종합 정보·최근 기대 득점·시즌 기록·예정 경기·팀 검색·시즌/장소/결과/날짜 필터가 작동합니다. 두 디자인 예시는 같은 자료와 기능을 유지합니다. 실제 브라우저 화면 검사와 사용자의 디자인 확정은 아직 남아 있습니다.

[첫 예측 모델 실험](modeling/README.ko.md)의 코드·검사·독립 검토 기록도 보존했습니다. 새 시즌 적중률이 비교 기준보다 낮아 **모델 채택은 false**이며 사이트에 예측 확률을 표시하지 않습니다. 자동 갱신·관리자 로그인·예측 API(프로그램 간 연결 창구)·공개 서비스·통합 5인 팀 재실행은 미구현입니다. Claude 실제 실행도 미검증입니다.

## 자료 범위

HTML에는 **완료 2,399경기·예정 641경기·56개 팀**, 팀별 경기 상세 4,798행과 160개 팀·시즌 × 47개 StatMuse 지표를 포함합니다. PL·라리가 합산으로 2023/24~2025/26은 시즌당 760경기, 진행된 2026/27은 119경기입니다. 마지막 완료 경기 날짜는 **2026-09-20**이며 디자인 변경 중 새로 수집하지 않았습니다.

경기·날짜·기대 득점은 Understat, 추가 시즌 통계는 StatMuse입니다. 경기 필터와 시즌 전체 통계의 범위를 구분해 표시합니다. 풋볼데이터·배당·챔스는 제외합니다. 슈팅 좌표 자료는 없으며 픽셀 경기장 그림은 장식입니다.

공개 CSV는 기존 **완료 20경기·예정 2경기 시연 부분자료**입니다. 전체 학습 CSV와 사이트 캐시는 로컬에 남아 있습니다. HTML의 더 큰 화면용 자료와 모델 입력 CSV를 같은 것으로 간주하지 않습니다. 선수단·시장 가치·기사 자료는 관찰 날짜가 다르고 누락도 존재합니다.

## 에이전트 5개

| 에이전트 | 담당 |
|---|---|
| 팀장·최종 내부 판단 | 계획·배정·상태 관리·독립 검증 뒤 승인/보류 |
| 자료·동향 수집 | 경기·선수단·포메이션·가치·소식 |
| 분석·예측 | 팀 비교와 실험 모델 |
| 시각화·웹 | 차트·화면·서비스 구현 |
| 독립 검증·모델 평가 | 자료·계산·성능 대조 |

[현재 5인 구성](agent-team-integrated-2026-10-06-v01/README.md) · [이전 10역할 구성](agent-team-2026-10-06-v01/README.md) · [실제 실행 기록](team-run-2026-10-06-v01/README.md).
대표 2경기 실제 실행은 이전 10역할 배정이며 5인 실행으로 바꾸어 기록하지 않습니다. 작성자·독립 검증자·최종 결재자를 분리하며 최종 모델 채택과 사업 판단은 사용자에게 있습니다.

## 검증과 한계

```sh
python -m unittest discover -s agent-team-2026-10-06-v01/tests -v
python -m unittest discover -s agent-team-integrated-2026-10-06-v01/tests -v
python -m unittest discover -s modeling/tests -v
node visualization-design-2026-10-06-v14/check.cjs
```

모델 검사는 Python 3.11 이상과 지정 NumPy가 필요합니다. 화면은 Node에서 화면 요소를 흉내 내는 검사로 계산·검색·이동·말풍선 36항목을 확인합니다. **실제 화면 모양·모바일 터치·외부 로고/글꼴 로딩·참가자 확인은 별도이며 미확인입니다.** 관리자용 로컬 파일 분리는 로그인 권한 검사가 아닙니다. 이전 화면의 출처 기록은 보존합니다. 팀 강조색의 정확한 색상 값은 디자인 선택값입니다.

이전 실행의 보조 49기록은 수집26·미수집22·접근차단1, 선수단117명·직전 선발44명입니다. 원자료 독립 대조271항목도 보존합니다. 검사 통과가 모든 제공처 사실을 인증하는 것은 아닙니다.

## 버전 관리와 SPEC

[VERSION](VERSION) · [변경 이력](CHANGELOG.md) · [요구사항·검증 SPEC](docs/SPEC-0.3.0.md) · [버전 규칙](docs/VERSIONING.md) · [현재 화면 선택](viewer_selection.json) · [내용 해시](publication_manifest.json).
해시는 파일 내용이 바뀌었는지 비교하는 값입니다. 화면 v01~v14는 보존된 개발 버전이며 이번 기능 묶음의 버전은 0.3.0입니다. 0.2.1 파일 명세도 보관합니다. 일부 과거 생성/검증 명령은 당시 로컬 환경의 기록으로, 모든 과거 생성기가 다른 컴퓨터에서 바로 실행된다는 뜻은 아닙니다.

'''
(p/'README.md').write_text(en+table(False)+'\n',encoding='utf8')
(p/'README.ko.md').write_text(ko+table(True)+'\n',encoding='utf8')
(p/'VERSION').write_text('0.3.0\n',encoding='utf8')
change=p/'CHANGELOG.md'
old=change.read_text(encoding='utf8')
if '## 0.3.0' not in old:
    old=old.replace('# Release history / 변경 이력','# Release history / 변경 이력\n\n## 0.3.0 — 2026-10-06\n\n- Preserve UI v01–v14: team colours/logos/history, match filters, 47 Korean metrics, click explanations, layout fixes and source/external-link removal.\n- Add functioning soft-app and 8-bit previews, release SPEC, viewer selection and refreshed hashes.\n- Publish archived baseline code/review while keeping service adoption false; no model improvement or deployment in this release.\n- 화면 v01~v14 보존, 팀 정보·필터·한글 지표·말풍선·넘침 수정·외부 링크 제거. 부드러운/8비트 미리보기와 SPEC·버전 명세 추가. 모델 실험은 보존하되 서비스 채택은 보류.\n- Actual browser rendering, administrator authentication, automatic refresh and user design acceptance remain pending.',1)
change.write_text(old,encoding='utf8')
policy=p/'docs/VERSIONING.md'
text=policy.read_text(encoding='utf8').replace('current version is0.2.1','current version is0.3.0')
text+='\n## 0.3.0 publication scope\n\nViewer revisions v01–v14 remain immutable comparisons. viewer_selection.json separates functional v12 from soft v13 and pixel v14 previews. The HTML now embeds a larger display dataset; the CSV demo is unchanged. Full provider caches, complete modeling CSV and the local admin source report remain outside this release. Archived reviewer command records may retain generic machine paths describing the original execution environment. docs/publication_manifest-0.2.1.json preserves the previous file listing.\n'
policy.write_text(text,encoding='utf8')
(p/'viewer_selection.json').write_text(json.dumps(dict(release='0.3.0',functional_viewer='visualization-design-2026-10-06-v12/index.html',soft_preview='visualization-design-2026-10-06-v13/index.html',pixel_preview='visualization-design-2026-10-06-v14/index.html',design_acceptance='pending',administrator_authentication=False,model_adopted=False),indent=2)+'\n',encoding='utf8')
for name,section in [('README.md','''\n## MatchDesk football agent project · 0.3.0\n\n[Project and version history](football/matchdesk-ai-agents/README.md) · [Release SPEC](football/matchdesk-ai-agents/docs/SPEC-0.3.0.md) · [8-bit HTML preview](football/matchdesk-ai-agents/visualization-design-2026-10-06-v14/index.html). Team analytics with Korean metric explanations, filters and two design previews. Experimental prediction adoption remains false. Download HTML to view; no hosted service is claimed.\n'''),('README.ko.md','''\n## MatchDesk AI 경기 분석실 · 0.3.0\n\n[프로젝트·버전 이력](football/matchdesk-ai-agents/README.ko.md) · [요구사항·검증 SPEC](football/matchdesk-ai-agents/docs/SPEC-0.3.0.md) · [8비트 HTML 미리보기](football/matchdesk-ai-agents/visualization-design-2026-10-06-v14/index.html). 팀 통계·한글 지표 풀이·필터·디자인 예시를 제공합니다. 예측 모델 채택은 보류이며 HTML을 내려받아 확인합니다. 공개 서비스로 배포한 상태는 아닙니다.\n''')]:
    target=repo/name
    text=target.read_text(encoding='utf8')
    if '## MatchDesk' not in text:
        marker='[English](README.md) | [한국어](README.ko.md)'
        text=text.replace(marker,marker+'\n'+section,1)
        target.write_text(text,encoding='utf8')
for name,note in [('README.md','> Release note: archived source/tests/review are published in 0.3.0. The original local assessment below remains historical; model adoption is still false and generated runs stay ignored.\n\n'),('README.ko.md','> 0.3.0 공개 기록: 실험 코드·검사·검토 문서를 이번 버전에 포함합니다. 아래의 로컬 개발 설명은 당시 상태이며 모델 채택은 계속 보류, 생성 실행 결과는 Git 추적 제외입니다.\n\n')]:
    target=p/'modeling'/name
    text=target.read_text(encoding='utf8')
    if '0.3.0' not in text: target.write_text(note+text,encoding='utf8')
print('Updated bilingual docs, version history and release selection; 0.2.1 manifest archived.')
