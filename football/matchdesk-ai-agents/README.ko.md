# MatchDesk — AI 경기 분석실 에이전트 팀

[English](README.md) | [한국어](README.ko.md)

**버전 0.7.0 · 2026-10-06.** 축구 자료 수집·팀 분석·화면·독립 검증·최종 내부 판단을 연결하는 5인 에이전트 프로젝트입니다. AI 제공자와 모델은 고정하지 않습니다.

0.6.0: 완료 경기의 팀 이름은 팀 상세로, 작은 경기 링크는 Understat 경기 페이지로 연결됩니다. 상세 지표 6개 설명 말풍선 추가, 출처·경기 수 표시 제거.

0.7.0: 분석관 입력창에서 기록 비교·리그 순위·홈/원정 분석·후속 요청을 실행하고 차트·표·계산 과정을 표시합니다. 실제 실행은 JavaScript이며 AI 모델·SQL·Python·예측 도구는 미연결입니다. [도구 규격·담당](docs/ANALYSIS-TOOLS.md) · [기록 분석 스킬](skills/record-analysis/SKILL.md) · [SQL 스킬](skills/sql-analysis/SKILL.md) · [Python 스킬](skills/python-analysis/SKILL.md). 엔진 15개·한국어 화면 48개·영어 23개 검사 통과.

## 화면 열기
- [영어 사이트](index.en.html) · [한국어 사이트](index.html): 메뉴·필터·47개 지표 이름·의미·읽는 법을 번역했습니다. 프리미어리그 27개·라리가 29개는 과거 시즌 팀을 포함한 수입니다. 상단 언어 전환 시 선택 팀 주소는 유지되고 나머지 필터는 초기화됩니다. 한국어 44개·영어 19개 코드 동작 검사 통과. 실제 브라우저 화면은 확인 전입니다.


- [MatchDesk 기본 화면 — 채택된 8비트 디자인](index.html) · [v18 버전](visualization-design-2026-10-06-v18/index.html)
- [부드러운 앱 디자인 예시 — v13](visualization-design-2026-10-06-v13/index.html)
- [8비트 게임 디자인 미리보기 — v14](visualization-design-2026-10-06-v14/index.html)
- [디자인 후보 3개 비교](design-candidates-2026-10-06-v01/index.html)

HTML을 내려받아 브라우저에서 엽니다. GitHub의 코드 보기에서는 실행되지 않으며 인터넷에 서비스로 올린 상태도 아닙니다. 경기·팀·리그 메뉴와 팀 이름/로고로 탐색하고, 지표 이름을 누르면 뜻과 읽는 법이 열립니다. 한글 이름과 원본 약어 모두 검색할 수 있습니다. v11부터 출처·수집 시점 영역을 제거했고 v12부터 외부 경기 링크를 제거했습니다.

## 구현한 것과 남은 것

팀별 종합 정보·최근 기대 득점·시즌 기록·예정 경기·팀 검색·시즌/장소/결과/날짜 필터가 작동합니다. 8비트 디자인은 사용자 선택으로 기본 화면에 채택했습니다. 56개 팀 로고를 원본 비율의 24×24 격자에 표시하고 확대 시 픽셀 느낌을 줍니다. 로딩 실패 시 팀 약자가 표시됩니다. 실제 브라우저에서의 시각적 품질 확인은 아직 남아 있습니다.

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
node visualization-design-2026-10-06-v18/check.cjs
node visualization-design-2026-10-06-v18/check-en.cjs
```

모델 검사는 Python 3.11 이상과 지정 NumPy가 필요합니다. 화면은 Node에서 화면 요소를 흉내 내는 검사로 계산·검색·이동·말풍선과 로고 렌더링 40항목을 확인합니다. **실제 화면 모양·모바일 터치·외부 로고/글꼴 로딩·시각적 품질 확인은 별도이며 미확인입니다.** 관리자용 로컬 파일 분리는 로그인 권한 검사가 아닙니다. 이전 화면의 출처 기록은 보존합니다. 팀 강조색의 정확한 색상 값은 디자인 선택값입니다.

이전 실행의 보조 49기록은 수집26·미수집22·접근차단1, 선수단117명·직전 선발44명입니다. 원자료 독립 대조271항목도 보존합니다. 검사 통과가 모든 제공처 사실을 인증하는 것은 아닙니다.

## 버전 관리와 SPEC

[VERSION](VERSION) · [변경 이력](CHANGELOG.md) · [요구사항·검증 SPEC](docs/SPEC-0.7.0.md) · [0.3.0 SPEC](docs/SPEC-0.3.0.md) · [버전 규칙](docs/VERSIONING.md) · [현재 화면 선택](viewer_selection.json) · [내용 해시](publication_manifest.json).
해시는 파일 내용이 바뀌었는지 비교하는 값입니다. 화면 v01~v18을 보존하며 이번 버전은 0.7.0입니다. 한국어 index.html과 영어 index.en.html은 v18의 각 언어 화면과 동일합니다. 0.2.1 파일 명세도 보관합니다. 일부 과거 생성/검증 명령은 당시 로컬 환경의 기록으로, 모든 과거 생성기가 다른 컴퓨터에서 바로 실행된다는 뜻은 아닙니다.

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
