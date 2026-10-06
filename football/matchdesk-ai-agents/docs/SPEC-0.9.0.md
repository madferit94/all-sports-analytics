# MatchDesk 0.9.0 · Experimental prediction and eleven-player replay

## 요구사항 / Requirements

- 한글·영어 기본 화면을 v23과 동일하게 제공합니다. v19~v22와 첫 시뮬레이션은 과거 버전으로 보존합니다.
- 양 팀은 각각 골키퍼 1명·필드 선수 10명, 총 22명입니다. 두 팀이 같은 인원 배열에서 위치·유니폼·움직임을 그리도록 구현합니다. 11명이 화면 안에 있으며 골키퍼와 필드 선수가 구분되는지 자동 검사합니다.
- 재생은 실험 확률을 이용한 가상 연출입니다. 실제 경기 영상·정확한 득점 시간·선수별 예측·실제 포메이션으로 표시하지 않습니다. 동일한 입력과 난수 시작값은 같은 가상 결과를 만듭니다.
- 패배는 붉은 배경/짙은 붉은 글자, 무승부는 노란 배경/짙은 갈색 글자로 구분합니다. 승리 초록 표시는 유지합니다.
- AI 분석관 요청 오류를 인증·사용량·제공자 오류·응답 지연·서버 연결 상태로 구분합니다. `.env`와 API 키는 공개하지 않습니다.

## 모델 / Model

경기 전 승부 예측 v2는 공격·수비·압박·최근 최대 5경기·관측량을 사용합니다. 경기 날짜보다 엄격하게 이전인 기록만 특징으로 사용하고 같은 날짜 결과를 먼저 넣지 않습니다. 시즌 초반/이전 기록 없는 팀은 이전 시즌과 리그 평균으로 완화합니다. 이전 기록이 없다고 승격팀으로 확정하지 않습니다. 실제 패스 성공률은 경기 이전 자료가 없어 제외합니다.

2023/24 학습·2024/25 설정 선택 후 고정 평가 모델로 2025/26과 진행 2026/27을 평가합니다. 미래 확률 모델은 저장된 2,399경기로 별도 재학습했습니다. 2025/26 적중률 50.92% 대 리그 결과빈도 기준 45.79%, 확률 오차 1.0111 대 1.0680입니다. 진행 LaLiga 적중률은 기준보다 낮습니다. **모델 채택 false / EXPERIMENTAL_NOT_ADOPTED** 상태를 유지합니다.

전 시즌 승점 순위 대용값 추가는 2025/26 적중률 49.87%로 개선되지 않았습니다. 공식 순위·당시 선수단 시장가치 효과를 검증한 실험이 아닙니다. 새 변수 채택은 보류합니다.

## 실행 근거와 한계 / Evidence and limits

자동 검사는 실제 저장 데이터 계산·모델 지표 재계산·화면 요소를 흉내 낸 검사·가짜 제공자 응답을 이용한 실제 로컬 HTTP 검사로 구분합니다. 실제 브라우저의 영상 재생 품질과 참가자 확인은 별도이며 확인 전입니다. 외부 로고/글꼴 로딩도 자동 DOM 검사로 보장하지 않습니다. 실제 제공자 호출과 가짜 응답 검사는 서로 다른 근거입니다. API 인증값이나 계정별 결제 상태는 공개 검증 자료에 포함하지 않습니다. GitHub 검사 실행 성공을 주장하지 않습니다.

Stored records were not refreshed: 2,399 completed matches, 641 scheduled fixtures and last completed date 2026-09-20. The animation is a probability-driven illustration, not player-level forecasting or footage. The experimental model is displayed but is not formally adopted. Official standings and time-correct market values remain candidate features. Local serving is not public hosting.

## 파일 / Files

- [Korean site](../index.html) · [English site](../index.en.html) · [v23](../visualization-design-2026-10-06-v23/index.html)
- [Prediction model KO](../modeling/prematch-v2-2026-10-06-v01/README.ko.md) · [Prediction model EN](../modeling/prematch-v2-2026-10-06-v01/README.md)
- [Feature fact check](feature-factcheck-2026-10-06-v01/RESULTS.ko.md)
- [Simulation source](../simulation/pixel-v2-2026-10-06-v01/pixel-simulation.js) · [Simulation checks](../simulation/pixel-v2-2026-10-06-v01/check.cjs)
- [Version history](../CHANGELOG.md) · [Current selection](../viewer_selection.json) · [Content hashes](../publication_manifest.json)
