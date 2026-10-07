# 0.9.2 — 내부 경기 분석 연결 / Internal match analysis

실행 전 요구사항: 경기 보기 링크를 외부 Understat 대신 내부 #match=ID로 연결합니다. 완료 경기 실제 점수·xG·양 팀 상세 지표·해당 경기 이전 최근 5경기를 표시합니다. 팀 이동·뒤로 가기·영어 전환을 지원합니다. AI 분석 결과의 계산 과정 details를 제거하되 계산 기능은 보존합니다. 전체 팀 대상 학습과 승격팀 보정을 구분합니다.

기존 0.9.1 파일은 visualization-design-2026-10-07-v24에 보존합니다. 모델 재학습·웹 모델 교체·유료 API 호출은 이 변경에 포함하지 않습니다. 검증 결과는 실행 후 추가합니다. 참가자 확인 전.

## 실제 검증
- KO/EN 모든 inline JavaScript 구문 검사 PASS.
- localhost 브라우저 PL Brighton–Arsenal, 라리가 Alaves–Valencia에서 경기 보기 클릭 → 내부 #match 경로·실제 점수·xG·양 팀 6개 지표 확인.
- 팀 클릭·뒤로 가기·언어 전환 시 경기 ID 유지, 지표 말풍선 확인. 경기 상세에서 리그 변경 시 다가오는 경기 화면으로 전환 확인.
- KO/EN 저장 기록 분석을 실제 실행: 그래프·표 유지, #analystresult details 0개. 유료 AI 호출은 실행하지 않음.
- 경기 링크는 내부 #match 경로, 현재 화면 가로 넘침 없음. verified-match-analysis.png 저장.
- 과거 흐름은 games(..., before=선택 경기 날짜)로 선택 경기 및 미래 경기 제외. 모델은 변경하지 않음.
- 새 화면은 visualization-design-2026-10-07-v24/index.html 및 index.en.html, 이전 파일은 해당 폴더 previous-0.9.1/에 보존.
- 참가자 확인 전. GitHub 푸시·머지 미실행.
