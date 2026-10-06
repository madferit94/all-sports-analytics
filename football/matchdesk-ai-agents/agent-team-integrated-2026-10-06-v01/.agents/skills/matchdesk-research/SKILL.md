---
name: matchdesk-research
description: MatchDesk에서 데이터·동향 수집 업무를 통합 수행한다. 5인 팀의 research 담당을 실행할 때 사용한다.
---

# 데이터·동향 수집

TEAM-PROTOCOL.md와 team.json을 먼저 읽는다. 현재 담당은 `research`이며 기존 기능 범위는 data, trends이다.

기본 경기 기록과 보조 정보를 수집·연결하고 구단 소식을 확인한다. 팀명·경기 키·출처·조회일·평가일을 보존한다. 현재 선수단과 과거 가치의 시점 차이, 확정 사실과 보도/추정을 구분한다. 컵·대표팀 기록을 확인하지 못했으면 리그 경기 간격을 실제 휴식일로 표현하지 않는다.

실제 수행에는 roles/research.md의 상세 절차와 report-contract.json을 따른다. 같은 기능의 보고서를 별도의 에이전트가 실행했다고 표현하지 않는다. producer_id는 실제 담당 주체다. 모델·제공자를 고정하지 않는다. 공동 작업자의 변경과 이전 산출물을 보존한다. 실행하지 않은 기능은 NOT_IMPLEMENTED, 미확인 자료는 MISSING/BLOCKED로 남긴다.
