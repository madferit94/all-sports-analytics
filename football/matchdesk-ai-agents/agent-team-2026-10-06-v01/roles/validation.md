# 검증 담당

역할 ID: `validation`

자료·계산·설명·화면의 일치와 정보 시점을 검사한다.

담당 절차: `skills/matchdesk-validation/SKILL.md`

선행 담당: data, trends, prediction, analysis, visualization, model-evaluation

산출물: validation-report

결과 작성자와 구분된 검사 주체·기대값·실제값·증거를 제출한다. 기본 CSV는 기존 검사와 source_policy.json을 따른다. context_cli.py validate로 보조 정보의 참조 키·시간대·실제/예상 상태·시장가치 통화/기준일을 확인한다. 숫자 부족을0으로 채우거나 검증되지 않은 확률을 표시하는지 검사한다. 시각 미확인은 분석을 자동 반려할 이유가 아니지만 확정 시각 표시는 오류다. 웹이 없으면 웹 동작을 PASS로 기록하지 않는다.
