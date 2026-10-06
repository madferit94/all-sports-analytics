# MatchDesk 0.7.0 · 자연어 기록 분석 작업창

## 사용자 요구와 구현

- 한·영 HTML에 `AI 분석관에게 물어보세요` / `Ask the AI analyst` 입력창, 예시 버튼, 실행 상태, 막대 차트, 수치 표, 계산 과정 펼치기를 추가합니다.
- 자유로운 모델 기반 대화의 첫 단계로 지원 표현을 해석하는 기록 분석을 구현합니다. 실제 엔진은 JavaScript이며 AI 모델·SQL·Python 실행은 연결 전입니다. 이 상태는 화면과 계산 과정에 표시합니다.
- 팀 기록·두 팀 비교·리그 순위·홈/원정·득점/xG 비교. 지표는 득점·실점·xG·xGA·승점·과거 승률입니다. 후속 요청에서 팀/시즌을 유지하고 최근 경기 수를 바꿀 수 있습니다.
- 생략한 조건: 선택된 팀/리그/시즌을 사용하고 장소는 전체, 기간은 시즌 전체입니다. 결과에 실제 조건을 표시합니다. 직접 날짜·승무패 조건·기타 지표는 지원하지 않습니다. 이전 분석 결과의 조건을 쓰는 후속 요청도 실제 조건을 출력합니다.
- 최근 N은 시즌 안의 완료 경기만입니다. 자료가 N개보다 적으면 있는 경기만 사용합니다. 홈/원정 최근 N은 장소별 N입니다. 누락 시즌은 0이 아니라 자료 없음입니다.
- 승리 확률 요청은 미연결로 안내하고 이전 차트를 지웁니다. 현재 보류된 모델 성능을 채택했다고 표현하지 않습니다. 미래 일정은 학습/집계 자료에 넣지 않습니다.
- 새 서비스의 질문 해석·실행·출력 함수를 등록할 확장 규격을 추가합니다. 실제 다른 서비스 연결은 없으며 원격 도구 연결은 비동기 실행 규격 확장이 필요합니다.
- 기존 팀/경기 링크·6개 말풍선·47개 시즌 지표·한영 데이터 동일성을 유지합니다. 메뉴·팀 이름·지표·선택/요약 요소에 Galmuri11을 확장하고 긴 설명·입력창은 읽기 쉬운 글꼴을 유지합니다.
- 프로젝트용 record-analysis/sql-analysis/python-analysis 스킬 문서를 추가합니다. 실행 도구와 문서를 구분하며 자동 설치는 하지 않았습니다. [도구 규격과 담당 기록](ANALYSIS-TOOLS.md).

## 검증 근거

- 분석 엔진 15개 검사: 자연어 조건, 한영 동일 결과, 실제 2023/24 경기에서 독립 계산한 최근 10개 득점/xG, 실제 경기 수 분모의 라리가 순위, 홈/원정 19+19, 두 팀 승점, 후속 5경기, 미래 제외, 확률 미연결, 누락 시즌, 지원 범위, 리그 불일치, 과거 승률, 확장 등록, 입력 제한.
- 한국어 화면 48개·영어 23개 Node VM 검사: 이전 동작 회귀와 작업창 차트/표/조건, 후속 요청, 확률 요청 시 이전 결과 제거, 화면 요소 연결. 총 86개 검사 통과.
- 실제 브라우저 배치·입력·새 글꼴 품질과 참가자 확인은 미확인입니다. 화면 검사를 우회하는 별도 브라우저는 실행하지 않았습니다.
- 데이터 JSON 값과 범위는 v17 그대로입니다. 마지막 완료일 2026-09-20, 자료 새 수집 없음. v18과 이전 화면 보존.

## English

The bilingual HTML workbench interprets supported natural-language phrases into recorded-match calculations and renders charts, tables and inspectable conditions. This is browser JavaScript, with no LLM, SQL or Python execution connected. Predictions are explicitly unavailable. Existing five-agent responsibilities are documented, but the actual implementation/tests were performed by primary Codex without separately executing team agents. 86 checks passed; real-browser and human visual confirmation pending.
