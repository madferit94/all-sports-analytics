---
name: matchdesk-data
description: Understat 기본 기록과 StatMuse 추가 통계, 포메이션·선발·선수단·시장가치 보조 자료를 수집하고 연결한다. MatchDesk에서 데이터·선수단 담당 역할 작업을 요청할 때 사용한다.
---

# 데이터·선수단 담당

패키지 루트의 `TEAM-PROTOCOL.md`와 `team.json`을 읽는다. 특정 AI 제공자나 모델 이름에 의존하지 않는다. 담당 역할은 `data`이다.

기본 자료는 ../source-unified-2026-10-06-v01 을 읽는다. 날짜·일정·xG의 출처는 Understat이고 공식 일정 덮어쓰기는 하지 않는다. StatMuse는 시즌 추가47종만 연결한다. context-data-contract.json 기준으로 포메이션·실제/예상 선발·선수단 구성·선수단 추정 시장가치·감독 이력·휴식일을 별도 수집한다. 포메이션은 사이트의 명목 배치이며 경기 중 위치로 추정하지 않는다. 새 출처는 대상 페이지를 실제 확인하고 키 매핑·기준일·접근 가능 여부를 기록한다. 차단 또는 누락은 MISSING/BLOCKED로 남기고 값이나 URL을 지어내지 않는다. 수집한 자료는 context_cli.py validate로 검사한다. 상세 보조 정보는 기본 자료를 덮어쓰지 않는다.

입력은 run_id, match_key, cutoff_at, 사용자 요청, 선행 결과 경로다. 출력은 `report-contract.json`의 공통 형식이며 담당 산출물은 data-report, context-records이다. 증거 파일이 없는 실제 실행을 DONE/PASS로 기록하지 않는다. 기본 데이터와 보조 정보는 참조 키로 연결하고 출처 정책을 유지한다.

새 산출물은 고유한 실행 폴더에 저장한다. 상위 작업일지 하나에 실제 결과·미확인 상태를 기록한다. 공동 작업 중 다른 담당자의 파일을 되돌리지 않는다. 역할 소유 파일과 공유 파일의 수정 담당을 배정 전에 정한다.
