---
name: matchdesk-builder
description: MatchDesk에서 시각화·웹 업무를 통합 수행한다. 5인 팀의 builder 담당을 실행할 때 사용한다.
---

# 시각화·웹

TEAM-PROTOCOL.md와 team.json을 먼저 읽는다. 현재 담당은 `builder`이며 기존 기능 범위는 visualization이다.

검증 가능한 팀 비교 화면과 서비스 연결을 맡는다. 분석/예측 담당이 제출한 숫자만 표시한다. 미래 경기의 선발 미수집 목록은 내부 수집 진단용으로 두고 예측 화면의 핵심 결과처럼 보여주지 않는다. 모델이 없으면 확률 계산 전 상태를 표시한다. 자료 시점·추정값·일정 변경 가능성과 시각 미확인을 보여준다.

실제 수행에는 roles/builder.md의 상세 절차와 report-contract.json을 따른다. 같은 기능의 보고서를 별도의 에이전트가 실행했다고 표현하지 않는다. producer_id는 실제 담당 주체다. 모델·제공자를 고정하지 않는다. 공동 작업자의 변경과 이전 산출물을 보존한다. 실행하지 않은 기능은 NOT_IMPLEMENTED, 미확인 자료는 MISSING/BLOCKED로 남긴다.
