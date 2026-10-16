# 2026 FIFA 월드컵 예측 데이터셋

[English](README.md) | [한국어](README.ko.md)

과거 국가대표 경기 결과, FotMob 경기 기록, Transfermarkt 국가대표 정보를 사용해 2026 FIFA 월드컵 경기 결과를 예측하는 작업 흐름을 뒷받침하는 데이터셋입니다.

## 데이터셋 용도

이 데이터셋은 다음 용도로 만들었습니다:

- 경기 전 팀 폼 특성 만들기
- 승·무·패 예측 모델 학습
- 조별리그 경기 결과 예측
- 토너먼트 단계 결과 시뮬레이션
- 여러 머신러닝 모델의 결과 비교

## 입력 파일

노트북에서 모델링 데이터셋을 다시 만들 때 쓰는 파일입니다.

| 파일 | 설명 |
|---|---|
| `input/fotmob_match_ids_extracted.csv` | 월드컵 참가팀이 포함된 과거 국가대표 경기. FotMob 경기 ID와 결과 포함. |
| `input/fotmob_statistics_long.csv` | 세로 형식의 FotMob 팀 단위 경기 기록. 최근 5경기 평균 폼 특성을 만드는 데 사용. |
| `input/transfermarkt_country_profile.csv` | Transfermarkt 국가대표 정보: 선수단 규모, 평균 나이, FIFA 랭킹, 총 시장 가치. |
| `input/worldcup48_matches_2023_plus.csv` | 월드컵 48개 팀 중 한 팀 이상이 나온 경기만 추린 과거 경기. |
| `input/international_matches_2023_plus.csv` | 2023년 이후의 더 넓은 범위의 국가대표 경기 결과. |
| `input/transfermarkt_country_sources.csv` | Transfermarkt 국가대표 페이지의 원본 URL. |
| `input/sources.csv` | 데이터 수집 출처 목록. |

## 결과 파일

`outputs/` 폴더에 모델 결과가 들어 있습니다.

| 파일 이름 형식 | 설명 |
|---|---|
| `outputs/model_validation_scores.csv` | 후보 모델별 검증 점수. |
| `outputs/champions_by_model.csv` | 모델별 예상 우승팀과 결승 대진. |
| `outputs/group_predictions_*.csv` | 모델별 조별리그 예측. |
| `outputs/group_table_*.csv` | 모델별 예상 조별 순위표. |
| `outputs/qualified_teams_*.csv` | 모델별 예상 32강 진출팀. |
| `outputs/tournament_results_*.csv` | 모델별 예상 토너먼트 대진 결과. |

## 모델링 참고

- 예측 기준 날짜: `2026-06-11`
- 학습 구간: 예측 기준 날짜 이전 1년
- 최근 폼 특성은 예측 날짜 이전 경기만 사용
- 최근 경기 평균 특성은 이전 경기만 써서 같은 경기 정보가 새어 들어가지 않게 함
- Transfermarkt 값은 현재 전력 지표로 사용

## 한계

- Transfermarkt의 과거 시점 값은 포함하지 않았습니다.
- FotMob 기록 범위는 국가대표 경기마다 다릅니다.
- 노트북의 토너먼트 대진은 단순화한 시드 방식이며, FIFA 공식 3위 팀 배정표가 아닙니다.
- 예측은 모델 결과이며 확정된 결과로 해석하면 안 됩니다.
