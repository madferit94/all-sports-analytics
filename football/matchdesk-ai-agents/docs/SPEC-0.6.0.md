# MatchDesk 0.6.0 · 경기 연결과 지표 설명

## 요청과 동작

- 수치 보기, 최근 경기, 팀 경기 기록: 팀 이름/로고는 기존 팀 상세 주소로 이동합니다.
- 각 완료 경기 행에 작은 `경기 보기 ↗` / `Match ↗` 링크를 별도로 제공합니다. 저장된 해당 경기의 Understat 주소를 새 탭으로 엽니다. 수치 보기 토글 자체는 외부 페이지를 열지 않습니다.
- 외부 링크와 팀 링크를 중첩하지 않습니다. 외부 링크는 Understat의 숫자 경기 주소만 허용하고 새 탭이라는 접근성 설명과 안전한 rel 속성을 포함합니다.
- 선택 경기 상세 지표의 `Understat · N경기` 표시는 제거합니다.
- 페널티 제외 기대 득점/실점, 기대 승점, Deep/Deep 허용, PPDA 총 6개 지표에 한국어·영어 설명 말풍선을 추가합니다. 기존 클릭·Escape·바깥 클릭·닫기·초점 복귀 방식을 재사용합니다.
- Deep 설명은 골문 가까운 위험 지역의 성공 패스로 표현하되 공식 지역 경계·제외 조건의 세부 정의 미확인을 읽는 법에 명시합니다. 출처 페이지 https://understat.com/league/EPL 에서 이번 웹 읽기로 세부 정의를 확인하지 못했으므로 특정 거리 수치를 단정하지 않습니다.
- 통계 수치와 범위는 변경하지 않습니다. PPDA는 기존 분자 합/분모 합이며 분모 0이면 누락값입니다. 기대 승점은 미래 승리 확률로 표시하지 않습니다.

## 실행 근거

v17 한국어 44개·영어 19개 Node VM 검사 통과. 원본 경기 주소와 상대 팀 연결, 세 표의 링크 중첩 없음, 잘못된 주소 제외, 6개 말풍선 개폐·설명, 표시 제거·기존 수치 유지, 과거 55개 회귀 검사를 포함합니다.

검사는 가짜 화면 객체를 사용한 코드 검사입니다. 실제 브라우저 화면·외부 페이지 로딩·참가자 직접 확인 전입니다. v16과 이전 화면을 보존하며 기본 두 언어 파일은 v17과 동일합니다.

## English

Completed-match rows separate internal club links from a small explicit Understat match link opening a new tab. Six selected-match metrics reuse the accessible explanation popover; the provider/count badge is removed. Statistical data and aggregate-ratio calculations are unchanged. 44 Korean and 19 English Node VM checks passed; real-browser rendering remains unverified.
