# 데이터·선수단 담당

역할 ID: `data`

Understat 기본 기록과 StatMuse 추가 통계, 포메이션·선발·선수단·시장가치 보조 자료를 수집하고 연결한다.

담당 절차: `skills/matchdesk-data/SKILL.md`

선행 담당: manager

산출물: data-report, context-records

기본 자료는 ../source-unified-2026-10-06-v01 을 읽는다. 날짜·일정·xG의 출처는 Understat이고 공식 일정 덮어쓰기는 하지 않는다. StatMuse는 시즌 추가47종만 연결한다. context-data-contract.json 기준으로 포메이션·실제/예상 선발·선수단 구성·선수단 추정 시장가치·감독 이력·휴식일을 별도 수집한다. 포메이션은 사이트의 명목 배치이며 경기 중 위치로 추정하지 않는다. 새 출처는 대상 페이지를 실제 확인하고 키 매핑·기준일·접근 가능 여부를 기록한다. 차단 또는 누락은 MISSING/BLOCKED로 남기고 값이나 URL을 지어내지 않는다. 수집한 자료는 context_cli.py validate로 검사한다. 상세 보조 정보는 기본 자료를 덮어쓰지 않는다.
