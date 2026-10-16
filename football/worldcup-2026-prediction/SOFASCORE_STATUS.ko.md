# SofaScore 수집 현황

[English](SOFASCORE_STATUS.md) | [한국어](SOFASCORE_STATUS.ko.md)

목표: 국가대표 경기의 결과, 기록, 선발 명단, 포메이션, 경기 중 사건을 수집합니다.

현재 환경에서의 결과:

- `requests`로 `https://www.sofascore.com/api/v1/...`에 접근하면 `403 Forbidden`이 돌아옵니다.
- Chrome headless로는 공개 축구 페이지가 가끔 열리지만, 날짜별 페이지와 API 주소는 불안정하거나 `403`을 돌려줍니다.
- 그래서 불완전하거나 왜곡된 데이터를 피하려고 SofaScore 대량 수집은 실행하지 않았습니다.

대신 수집해서 쓰는 데이터:

- `data/processed/international_matches_2023_plus.csv`
- `data/processed/worldcup48_matches_2023_plus.csv`

SofaScore 재시도 스크립트:

- `scripts/collect_sofascore.py`

이 스크립트는 `event_id` 열이 있는 `data/processed/sofascore_event_ids.csv`를 기대합니다. 유효한 SofaScore 이벤트 ID가 준비되면 다음을 수집할 수 있습니다:

- 경기 요약
- 경기 기록
- 선발 명단과 포메이션
- 경기 중 사건
