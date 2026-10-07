**0.11.4 · 일정 더보기·프리뷰:** 메인·팀 일정에6경기씩 더보기 추가. 팀 다음 경기의 분석 버튼은 해당 경기 전력 비교·모델 확률·시뮬레이션 프리뷰를 엽니다. 주소 새로고침·언어 전환에도 선택 경기 유지. [SPEC](docs/SPEC-0.11.4.md). 저장 일정 기반, 로컬 적용·GitHub 전송 전.

**0.11.3 · 지표 카드 가독성:** 패널 너비에 맞춰 카드 열 수를 조정하고, 지표 제목16px·숫자28px·설명13px로 정리했습니다. 단어와 숫자가 쪼개지지 않도록 수정하고 설명 말풍선을 유지했습니다. 한영 적용, 8비트 제목·숫자 유지. [SPEC](docs/SPEC-0.11.3.md). 로컬 적용, GitHub 전송 전.

**0.11.2 · 경기 움직임 개선:** 선수 전진·복귀·압박·드리블 동작과 연속적인 공 경로를 추가했습니다. 골 직후 공이 순간 이동하는 현상을 제거하고 한영 화면의 시뮬레이션 하단 점수 안내 문단을 삭제했습니다. 예측 확률과 학습 득점 분포는 그대로입니다. [SPEC](docs/SPEC-0.11.2.md). 로컬 적용, GitHub 전송 전.

**0.11.1 · 시뮬레이션 이동 개선:** 22명 유지·20명 필드선수 위치이동·선수 발에 연결한 드리블/패스/슈팅·GOAL 표시·득점후 중앙재개. 하단모델ID제거. 0.11.0 득점학습/승무패확률보존. [SPEC](docs/SPEC-0.11.1.md). GitHub전송전.

**0.11.0 · 득점 분포 연결:** 실제 과거득점으로포아송모델을학습하고로지스틱승무패확률과조합했습니다. 고정점수대신0:0·2:1·4:2등다양한표본점수를재생합니다. 양팀평균·총4골이상확률·상위점수3개를분포에기록합니다. [SPEC](docs/SPEC-0.11.0.md). 입력기준09-20스냅샷·미래성능미검증·GitHub전송전.

**0.10.0 · 로지스틱 적용:** 전체팀111입력·1518경기학습 모델을PL/라리가예정경기와8비트시뮬레이션에연결했습니다. 입력자료기준09-20,스냅샷예측이며실시간갱신아닙니다. 득점은현재1:0/1:1/0:1연출로고정되어있으며득점예측이아닙니다. [SPEC](docs/SPEC-0.10.0.md). GitHub전송전.

**0.9.2 · 로컬 수정:** 경기 보기 → 내부 경기 분석실. 실제 점수·xG·양 팀 지표·경기 이전 최근 기록을 표시하며 계산 과정 메뉴를 제거했습니다. 학습 모델은 전체 팀 대상입니다. [SPEC](docs/SPEC-0.9.2.md). GitHub 전송 전.

# MatchDesk — AI 경기 분석실 에이전트 팀

[English](README.md) | [한국어](README.ko.md)

**0.9.1 수정:** CSS 파일의 줄바꿈을 통일해서 내용 해시를 계산하므로 Windows에서도 같은 공개 검사를 통과합니다. v23 화면·각 팀 11명 재생·모델은 변경하지 않았습니다. [수정 SPEC](docs/SPEC-0.9.1.md).

**버전 0.9.1 · 2026-10-06.** 축구 자료 수집·팀 분석·화면·독립 검증·최종 내부 판단을 연결하는 5인 에이전트 프로젝트입니다. AI 제공자와 모델은 고정하지 않습니다.

0.6.0: 완료 경기의 팀 이름은 팀 상세로, 작은 경기 링크는 Understat 경기 페이지로 연결됩니다. 상세 지표 6개 설명 말풍선 추가, 출처·경기 수 표시 제거.

0.7.0: 분석관 입력창에서 기록 비교·리그 순위·홈/원정 분석·후속 요청을 실행하고 차트·표·계산 과정을 표시합니다. 실제 실행은 JavaScript이며 AI 모델·SQL·Python·예측 도구는 미연결입니다. [도구 규격·담당](docs/ANALYSIS-TOOLS.md) · [기록 분석 스킬](skills/record-analysis/SKILL.md) · [SQL 스킬](skills/sql-analysis/SKILL.md) · [Python 스킬](skills/python-analysis/SKILL.md). 엔진 15개·한국어 화면 48개·영어 23개 검사 통과.

0.8.0: .env 기반 Gemini 서버·도구 조건 검증·한영 비동기 모드를 추가했습니다. [설정 안내](server/README.ko.md). 로컬 .env에 키를 넣고 `node --env-file=.env server/gemini.cjs` 실행 후 http://127.0.0.1:8765 접속. 실제 Gemini 인증/모델 호출은 키 설정 후 확인해야 합니다. 서버12개 포함 총98개 검사 통과(제공자 응답은 가짜).

0.9.0: 공격·수비·압박·최근 5경기와 데이터 부족 보정을 이용한 실험 확률·8비트 재생을 추가하고 **각 팀 11명(골키퍼 1명·필드 선수 10명)**으로 수정했습니다. v20 오류 안내·v21 승패 색상·v22 첫 재생·v23 인원 수정을 보존합니다. [모델](modeling/prematch-v2-2026-10-06-v01/README.ko.md) · [변수 팩트 체크](docs/feature-factcheck-2026-10-06-v01/RESULTS.ko.md) · [이번 SPEC](docs/SPEC-0.9.1.md). 확률은 **실험·정식 미채택**이며 재생은 가상 연출입니다.

승부 예측 사례와 개선 방안: [한국어](docs/prediction-research-2026-10-06-v01/README.ko.md).

**Day13 작업으로 분류했습니다.** [새 작업 위치·이동 확인](docs/DAY13-WORKSPACE.md). 저장소 내부 경로와 기존 화면 버전은 유지합니다.

## 화면 열기
- [영어 사이트](index.en.html) · [한국어 사이트](index.html): 메뉴·필터·47개 지표 이름·의미·읽는 법을 번역했습니다. 프리미어리그 27개·라리가 29개는 과거 시즌 팀을 포함한 수입니다. 상단 언어 전환 시 선택 팀 주소는 유지되고 나머지 필터는 초기화됩니다. 버전별 코드 동작 검사 결과를 보존했습니다. 실제 브라우저 화면은 확인 전입니다.


- [MatchDesk 기본 화면 — 채택된 8비트 디자인](index.html) · [v23 버전](visualization-design-2026-10-06-v23/index.html)
- [부드러운 앱 디자인 예시 — v13](visualization-design-2026-10-06-v13/index.html)
- [8비트 게임 디자인 미리보기 — v14](visualization-design-2026-10-06-v14/index.html)
- [디자인 후보 3개 비교](design-candidates-2026-10-06-v01/index.html)

HTML을 내려받아 브라우저에서 엽니다. GitHub의 코드 보기에서는 실행되지 않으며 인터넷에 서비스로 올린 상태도 아닙니다. 경기·팀·리그 메뉴와 팀 이름/로고로 탐색하고, 지표 이름을 누르면 뜻과 읽는 법이 열립니다. 한글 이름과 원본 약어 모두 검색할 수 있습니다. v11부터 출처·수집 시점 영역을 제거했고 v12부터 외부 경기 링크를 제거했습니다.

## 구현한 것과 남은 것

팀별 종합 정보·최근 기대 득점·시즌 기록·예정 경기·팀 검색·시즌/장소/결과/날짜 필터가 작동합니다. 8비트 디자인은 사용자 선택으로 기본 화면에 채택했습니다. 56개 팀 로고를 원본 비율의 24×24 격자에 표시하고 확대 시 픽셀 느낌을 줍니다. 로딩 실패 시 팀 약자가 표시됩니다. 실제 브라우저에서의 시각적 품질 확인은 아직 남아 있습니다.

[첫 예측 모델 실험](modeling/README.ko.md)의 코드·검사·독립 검토 기록도 보존했습니다. 새 시즌 적중률이 비교 기준보다 낮아 **모델 채택은 false**이며 최신 실험 v2의 확률은 미채택 표시와 함께 화면에 제공합니다. 자동 갱신·관리자 로그인·공개 서비스는 미구현입니다. Claude 실제 실행도 미검증입니다.

## 자료 범위

HTML에는 **완료 2,399경기·예정 641경기·56개 팀**, 팀별 경기 상세 4,798행과 160개 팀·시즌 × 47개 StatMuse 지표를 포함합니다. PL·라리가 합산으로 2023/24~2025/26은 시즌당 760경기, 진행된 2026/27은 119경기입니다. 마지막 완료 경기 날짜는 **2026-09-20**이며 디자인 변경 중 새로 수집하지 않았습니다.

경기·날짜·기대 득점은 Understat, 추가 시즌 통계는 StatMuse입니다. 경기 필터와 시즌 전체 통계의 범위를 구분해 표시합니다. 풋볼데이터·배당·챔스는 제외합니다. 슈팅 좌표 자료는 없으며 재생의 움직임과 득점 시간은 연출입니다.

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
node simulation/pixel-v2-2026-10-06-v01/check.cjs
node simulation/pixel-v2-2026-10-06-v01/check-roster.cjs
node simulation/pixel-v2-2026-10-06-v01/check-integration.cjs
node docs/eleven-release-review-2026-10-06-v01/independent-check.cjs
```

모델 검사는 Python 3.11 이상과 지정 NumPy가 필요합니다. 화면은 Node에서 화면 요소를 흉내 내는 검사로 계산·검색·이동·말풍선과 로고 렌더링을 확인합니다. **실제 화면 모양·모바일 터치·외부 로고/글꼴 로딩·시각적 품질 확인은 별도이며 미확인입니다.** 관리자용 로컬 파일 분리는 로그인 권한 검사가 아닙니다. 이전 화면의 출처 기록은 보존합니다. 팀 강조색의 정확한 색상 값은 디자인 선택값입니다.

이전 실행의 보조 49기록은 수집26·미수집22·접근차단1, 선수단117명·직전 선발44명입니다. 원자료 독립 대조271항목도 보존합니다. 검사 통과가 모든 제공처 사실을 인증하는 것은 아닙니다.

## 버전 관리와 SPEC

[VERSION](VERSION) · [변경 이력](CHANGELOG.md) · [요구사항·검증 SPEC](docs/SPEC-0.9.1.md) · [0.3.0 SPEC](docs/SPEC-0.3.0.md) · [버전 규칙](docs/VERSIONING.md) · [현재 화면 선택](viewer_selection.json) · [내용 해시](publication_manifest.json).
해시는 파일 내용이 바뀌었는지 비교하는 값입니다. 화면 v01~v23을 보존하며 이번 버전은 0.9.1입니다. 한국어 index.html과 영어 index.en.html은 v23의 각 언어 화면과 동일합니다. 0.2.1 파일 명세도 보관합니다. 일부 과거 생성/검증 명령은 당시 로컬 환경의 기록으로, 모든 과거 생성기가 다른 컴퓨터에서 바로 실행된다는 뜻은 아닙니다.

| UI version | Change / 변경 |
|---|---|
| [v01](visualization-design-2026-10-06-v01/index.html) | 기본 설계·좌표 자료 확인 |
| [v02](visualization-design-2026-10-06-v02/index.html) | 사이트 디자인 기준 |
| [v03](visualization-design-2026-10-06-v03/index.html) | 이용자 화면·팀 색상 |
| [v04](visualization-design-2026-10-06-v04/index-v02.html) | 56개 로고·시즌 기록 |
| [v05](visualization-design-2026-10-06-v05/index.html) | 팀 이름 연결·종합 정보 |
| [v06](visualization-design-2026-10-06-v06/index.html) | 47개 지표·경기 필터 |
| [v07](visualization-design-2026-10-06-v07/index.html) | 긴 이름·카드 넘침 수정 |
| [v08](visualization-design-2026-10-06-v08/index.html) | 설명 기본 숨김 |
| [v09](visualization-design-2026-10-06-v09/index.html) | 한글 지표 이름·뜻 |
| [v10](visualization-design-2026-10-06-v10/index.html) | 클릭 말풍선·읽는 법 |
| [v11](visualization-design-2026-10-06-v11/index.html) | 출처 관리 자료 분리 |
| [v12](visualization-design-2026-10-06-v12/index.html) | 외부 경기 링크 제거 |
| [v13](visualization-design-2026-10-06-v13/index.html) | 부드러운 앱 디자인 예시 |
| [v14](visualization-design-2026-10-06-v14/index.html) | 8비트 디자인 미리보기 |
| [v15](visualization-design-2026-10-06-v15/index.html) | 8비트 기본 디자인 채택·팀 로고 픽셀 표시 |
| [v16](visualization-design-2026-10-06-v16/index.html) · [English](visualization-design-2026-10-06-v16/index.en.html) | 한·영 8비트 화면·47개 영어 지표 설명·언어 전환 |
| [v17](visualization-design-2026-10-06-v17/index.html) | Team/match links and six detailed metric explanations / 팀·경기 연결 및 상세 지표 설명 |
| [v18](visualization-design-2026-10-06-v18/index.html) | Recorded-data workbench, extension interface, broader pixel fonts / 기록 분석창·확장 규격·픽셀 글꼴 확장 |
| [v19](visualization-design-2026-10-06-v19/index.html) | Gemini env/server bridge / Gemini .env·서버 연결 |
| [v20](visualization-design-2026-10-06-v20/index.html) · [English](visualization-design-2026-10-06-v20/index.en.html) | AI 요청 오류 안내 개선 |
| [v21](visualization-design-2026-10-06-v21/index.html) · [English](visualization-design-2026-10-06-v21/index.en.html) | 패배 붉은색·무승부 노란색 가독성 |
| [v22](visualization-design-2026-10-06-v22/index.html) · [English](visualization-design-2026-10-06-v22/index.en.html) | 실험 승부 확률·가상 재생 |
| [v23](visualization-design-2026-10-06-v23/index.html) · [English](visualization-design-2026-10-06-v23/index.en.html) | 각 팀 골키퍼 1명·필드 선수 10명 |
