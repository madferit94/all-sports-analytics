# 팀 지표 차트 독립 검증
완료 범위: 저장 KO/EN HTML 내장 엔진·화면 코드를 Node와 격리된 가상 화면 요소에서 실행. 시즌 47종×56팀×4시즌 및 경기별 10종 대조. 292 PASS / 0 FAIL.

## 실행 전 기대값
- season: Four snapshots 2023/24..2026/27; raw totals preserved, percentage bars and paired aerial/duel stacked counts; missing remains null; current season ongoing.
- recent: Home/away orientation from completed match plus team detail; PPDA att/def, zero or absent denominator null; under four observations bars; WDL counts only observed finite scores.
- filters: Actual HTML selectedGames applies season, venue, result, date and recent bounds. Recent chart inherits that subset then chart window; season snapshot independent of match subset.
- ui: Actual embedded engine/UI source executes, data table accompanies chart, missing line point breaks connection, paired missing season says no data; no non-finite SVG dimensions.
- unknown: Browser appearance, keyboard, touch, external assets and user acceptance delegated to root; no model evaluation or final approval.

## 실제 대조값
- index.html recent count: PASS; 기대 10 / 실제 10
- index.html recent xg_for: PASS; 기대 [[0.639189],[4.09079],[1.42953],[1.22695],[3.90645],[1.85424],[1.52441],[2.80555],[1.98905],[1.23979]] / 실제 [[0.639189],[4.09079],[1.42953],[1.22695],[3.90645],[1.85424],[1.52441],[2.80555],[1.98905],[1.23979]]
- index.html recent type xg_for: PASS; 기대 "line" / 실제 "line"
- index.html recent xg_against: PASS; 기대 [[0.868897],[0.696714],[1.32011],[0.194884],[1.00492],[0.558336],[0.281925],[0.430508],[2.07033],[2.11268]] / 실제 [[0.868897],[0.696714],[1.32011],[0.194884],[1.00492],[0.558336],[0.281925],[0.430508],[2.07033],[2.11268]]
- index.html recent type xg_against: PASS; 기대 "line" / 실제 "line"
- index.html recent goals: PASS; 기대 [[1,0],[3,0],[1,0],[1,0],[2,1],[3,0],[1,0],[2,1],[2,0],[0,3]] / 실제 [[1,0],[3,0],[1,0],[1,0],[2,1],[3,0],[1,0],[2,1],[2,0],[0,3]]
- index.html recent type goals: PASS; 기대 "grouped" / 실제 "grouped"
- index.html recent deep: PASS; 기대 [[10,7],[14,3],[9,7],[20,2],[8,3],[18,2],[8,5],[17,5],[5,5],[10,6]] / 실제 [[10,7],[14,3],[9,7],[20,2],[8,3],[18,2],[8,5],[17,5],[5,5],[10,6]]
- index.html recent type deep: PASS; 기대 "grouped" / 실제 "grouped"
- index.html recent npxg_for: PASS; 기대 [[0.639189],[4.09079],[1.42953],[1.22695],[3.90645],[1.85424],[1.52441],[2.80555],[1.22788],[1.23979]] / 실제 [[0.639189],[4.09079],[1.42953],[1.22695],[3.90645],[1.85424],[1.52441],[2.80555],[1.22788],[1.23979]]
- index.html recent type npxg_for: PASS; 기대 "line" / 실제 "line"
- index.html recent npxg_against: PASS; 기대 [[0.868897],[0.696714],[1.32011],[0.194884],[1.00492],[0.558336],[0.281925],[0.430508],[1.30916],[2.11268]] / 실제 [[0.868897],[0.696714],[1.32011],[0.194884],[1.00492],[0.558336],[0.281925],[0.430508],[1.30916],[2.11268]]
- index.html recent type npxg_against: PASS; 기대 "line" / 실제 "line"
- index.html recent expected_points: PASS; 기대 [[1.0522],[2.915],[1.4258],[2.3346],[2.8347],[2.3738],[2.6457],[2.7935],[1.2985],[0.6937]] / 실제 [[1.0522],[2.915],[1.4258],[2.3346],[2.8347],[2.3738],[2.6457],[2.7935],[1.2985],[0.6937]]
- index.html recent type expected_points: PASS; 기대 "line" / 실제 "line"
- index.html recent ppda: PASS; 기대 [[14.88888888888889],[14.5],[6],[12.4375],[9.88888888888889],[9.647058823529411],[9.941176470588236],[8.904761904761905],[11.307692307692308],[12.642857142857142]] / 실제 [[14.88888888888889],[14.5],[6],[12.4375],[9.88888888888889],[9.647058823529411],[9.941176470588236],[8.904761904761905],[11.307692307692308],[12.642857142857142]]
- index.html recent type ppda: PASS; 기대 "line" / 실제 "line"
- index.html recent ppda_allowed: PASS; 기대 [[8.818181818181818],[13.681818181818182],[15.4375],[13.764705882352942],[17.75],[27.25],[18.75],[9.833333333333334],[10.380952380952381],[8.083333333333334]] / 실제 [[8.818181818181818],[13.681818181818182],[15.4375],[13.764705882352942],[17.75],[27.25],[18.75],[9.833333333333334],[10.380952380952381],[8.083333333333334]]
- index.html recent type ppda_allowed: PASS; 기대 "line" / 실제 "line"
- index.html recent results: PASS; 기대 [[9,0,1]] / 실제 [[9,0,1]]
- index.html recent type results: PASS; 기대 "stacked" / 실제 "stacked"
- index.html raw total not per-game: PASS; 기대 123 / 실제 123
- index.html missing score must not be draw: PASS; 기대 [null,null,null] / 실제 [null,null,null]
- index.html missing score count: PASS; 기대 1 / 실제 1
- index.html current season filters: PASS; 기대 ["understat:31180","understat:31199","understat:31209","understat:31216","understat:31224"] / 실제 ["understat:31180","understat:31199","understat:31209","understat:31216","understat:31224"]
- index.html home wins filters: PASS; 기대 ["understat:31180","understat:31209"] / 실제 ["understat:31180","understat:31209"]
- index.html date filters: PASS; 기대 ["understat:31209","understat:31216","understat:31224"] / 실제 ["understat:31209","understat:31216","understat:31224"]
- index.html recent five filters: PASS; 기대 ["understat:31180","understat:31199","understat:31209","understat:31216","understat:31224"] / 실제 ["understat:31180","understat:31199","understat:31209","understat:31216","understat:31224"]
- index.html recent ten filters: PASS; 기대 ["understat:29049","understat:29060","understat:29068","understat:29092","understat:29104","understat:29109","understat:29119","understat:29137","understat:29139","understat:29150"] / 실제 ["understat:29049","understat:29060","understat:29068","understat:29092","understat:29104","understat:29109","understat:29119","understat:29137","understat:29139","understat:29150"]
- index.en.html recent count: PASS; 기대 10 / 실제 10
- index.en.html recent xg_for: PASS; 기대 [[0.639189],[4.09079],[1.42953],[1.22695],[3.90645],[1.85424],[1.52441],[2.80555],[1.98905],[1.23979]] / 실제 [[0.639189],[4.09079],[1.42953],[1.22695],[3.90645],[1.85424],[1.52441],[2.80555],[1.98905],[1.23979]]
- index.en.html recent type xg_for: PASS; 기대 "line" / 실제 "line"
- index.en.html recent xg_against: PASS; 기대 [[0.868897],[0.696714],[1.32011],[0.194884],[1.00492],[0.558336],[0.281925],[0.430508],[2.07033],[2.11268]] / 실제 [[0.868897],[0.696714],[1.32011],[0.194884],[1.00492],[0.558336],[0.281925],[0.430508],[2.07033],[2.11268]]
- index.en.html recent type xg_against: PASS; 기대 "line" / 실제 "line"
- index.en.html recent goals: PASS; 기대 [[1,0],[3,0],[1,0],[1,0],[2,1],[3,0],[1,0],[2,1],[2,0],[0,3]] / 실제 [[1,0],[3,0],[1,0],[1,0],[2,1],[3,0],[1,0],[2,1],[2,0],[0,3]]
- index.en.html recent type goals: PASS; 기대 "grouped" / 실제 "grouped"
- index.en.html recent deep: PASS; 기대 [[10,7],[14,3],[9,7],[20,2],[8,3],[18,2],[8,5],[17,5],[5,5],[10,6]] / 실제 [[10,7],[14,3],[9,7],[20,2],[8,3],[18,2],[8,5],[17,5],[5,5],[10,6]]
- index.en.html recent type deep: PASS; 기대 "grouped" / 실제 "grouped"
- index.en.html recent npxg_for: PASS; 기대 [[0.639189],[4.09079],[1.42953],[1.22695],[3.90645],[1.85424],[1.52441],[2.80555],[1.22788],[1.23979]] / 실제 [[0.639189],[4.09079],[1.42953],[1.22695],[3.90645],[1.85424],[1.52441],[2.80555],[1.22788],[1.23979]]
- index.en.html recent type npxg_for: PASS; 기대 "line" / 실제 "line"
- index.en.html recent npxg_against: PASS; 기대 [[0.868897],[0.696714],[1.32011],[0.194884],[1.00492],[0.558336],[0.281925],[0.430508],[1.30916],[2.11268]] / 실제 [[0.868897],[0.696714],[1.32011],[0.194884],[1.00492],[0.558336],[0.281925],[0.430508],[1.30916],[2.11268]]
- index.en.html recent type npxg_against: PASS; 기대 "line" / 실제 "line"
- index.en.html recent expected_points: PASS; 기대 [[1.0522],[2.915],[1.4258],[2.3346],[2.8347],[2.3738],[2.6457],[2.7935],[1.2985],[0.6937]] / 실제 [[1.0522],[2.915],[1.4258],[2.3346],[2.8347],[2.3738],[2.6457],[2.7935],[1.2985],[0.6937]]
- index.en.html recent type expected_points: PASS; 기대 "line" / 실제 "line"
- index.en.html recent ppda: PASS; 기대 [[14.88888888888889],[14.5],[6],[12.4375],[9.88888888888889],[9.647058823529411],[9.941176470588236],[8.904761904761905],[11.307692307692308],[12.642857142857142]] / 실제 [[14.88888888888889],[14.5],[6],[12.4375],[9.88888888888889],[9.647058823529411],[9.941176470588236],[8.904761904761905],[11.307692307692308],[12.642857142857142]]
- index.en.html recent type ppda: PASS; 기대 "line" / 실제 "line"
- index.en.html recent ppda_allowed: PASS; 기대 [[8.818181818181818],[13.681818181818182],[15.4375],[13.764705882352942],[17.75],[27.25],[18.75],[9.833333333333334],[10.380952380952381],[8.083333333333334]] / 실제 [[8.818181818181818],[13.681818181818182],[15.4375],[13.764705882352942],[17.75],[27.25],[18.75],[9.833333333333334],[10.380952380952381],[8.083333333333334]]
- index.en.html recent type ppda_allowed: PASS; 기대 "line" / 실제 "line"
- index.en.html recent results: PASS; 기대 [[9,0,1]] / 실제 [[9,0,1]]
- index.en.html recent type results: PASS; 기대 "stacked" / 실제 "stacked"
- index.en.html raw total not per-game: PASS; 기대 123 / 실제 123
- index.en.html missing score must not be draw: PASS; 기대 [null,null,null] / 실제 [null,null,null]
- index.en.html missing score count: PASS; 기대 1 / 실제 1
- index.en.html current season filters: PASS; 기대 ["understat:31180","understat:31199","understat:31209","understat:31216","understat:31224"] / 실제 ["understat:31180","understat:31199","understat:31209","understat:31216","understat:31224"]
- index.en.html home wins filters: PASS; 기대 ["understat:31180","understat:31209"] / 실제 ["understat:31180","understat:31209"]
- index.en.html date filters: PASS; 기대 ["understat:31209","understat:31216","understat:31224"] / 실제 ["understat:31209","understat:31216","understat:31224"]
- index.en.html recent five filters: PASS; 기대 ["understat:31180","understat:31199","understat:31209","understat:31216","understat:31224"] / 실제 ["understat:31180","understat:31199","understat:31209","understat:31216","understat:31224"]
- index.en.html recent ten filters: PASS; 기대 ["understat:29049","understat:29060","understat:29068","understat:29092","understat:29104","understat:29109","understat:29119","understat:29137","understat:29139","understat:29150"] / 실제 ["understat:29049","understat:29060","understat:29068","understat:29092","understat:29104","understat:29109","understat:29119","understat:29137","understat:29139","understat:29150"]

## 발견과 조치

## 근거 파일
- reviewer-check.cjs: 실행 전 기준과 재현 코드
- reviewer-report.json: 모든 기대값·실제값·원본 SHA256 및 실행 시점
- 재현: 지정된 Node로 visualization-design-2026-10-07-v31/reviewer-check.cjs 실행

## 미확인과 필요한 사용자 판단
- Actual browser visual/keyboard/narrow-screen behavior delegated to root
- User screen acceptance
- Source-provider factual authenticity beyond stored data
- Prediction model performance outside chart scope
- Final approval is not issued by reviewer

검증 주체: /root/chart_reviewer, 작성자와 독립. 가상 화면 요소 실행은 실제 브라우저 화면 확인과 다릅니다. 최종 결재 아님.

## 최초 발견과 후속 대조
- 최초 정적 검토: 득점 null/null을 gf===ga로 비교하여 무승부로 세는 조건을 상위 담당자에게 보고했습니다. 상위 작성자가 수정한 뒤 최초 자동 검사했으므로 이전 앱 오류의 실행 재현을 주장하지 않습니다.
- 최종 동일 결측 입력: 기대 [null,null,null] / 실제 [null,null,null], missingCount 기대 1 / 실제 1. 관찰 가능한 경기만 결과 집계.
- 검사기 최초 실패 2건: 기대 [0,0,0]이 결측값 0 대체 금지와 충돌했습니다. 검사기 기대값을 null로 정정하고 같은 입력으로 재실행했습니다. 이전 FAIL 기대·실제·원인은 JSON prior_runs에 보존했습니다.
- 최종 결과: 292 PASS / 0 FAIL, 종료 코드 0.
- 시즌 원본 값 대조 수: 22848 (KO/EN 포함). 실제 제공처 재수집·사실 인증은 범위 밖.
