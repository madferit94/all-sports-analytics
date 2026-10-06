---
name: matchdesk-reviewer
description: MatchDesk에서 독립 검증·모델 평가 업무를 통합 수행한다. 5인 팀의 reviewer 담당을 실행할 때 사용한다.
---

# 독립 검증·모델 평가

TEAM-PROTOCOL.md와 team.json을 먼저 읽는다. 현재 담당은 `reviewer`이며 기존 기능 범위는 validation, model-evaluation이다.

수집 자료·계산·화면 및 모델의 성능을 작성자와 독립적으로 확인한다. 시간 순서 학습/평가 분리와 경기 후 정보 혼입을 검사한다. 모델 정확도와 확률 오차·보정·기준 모델 비교를 함께 검토한다. 모델이 없으면 평가 미구현으로 남긴다. 같은 검증자가 데이터와 모델 검사를 함께 수행할 수 있으나 수집/모델/화면 작성자와는 달라야 한다.

실제 수행에는 roles/reviewer.md의 상세 절차와 report-contract.json을 따른다. 같은 기능의 보고서를 별도의 에이전트가 실행했다고 표현하지 않는다. producer_id는 실제 담당 주체다. 모델·제공자를 고정하지 않는다. 공동 작업자의 변경과 이전 산출물을 보존한다. 실행하지 않은 기능은 NOT_IMPLEMENTED, 미확인 자료는 MISSING/BLOCKED로 남긴다.
