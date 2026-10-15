# 2026 FIFA 월드컵 경기 예측

[English](README.md) | [한국어](README.ko.md)

2026 FIFA 월드컵 경기 결과를 예측하는 작업 흐름을 만든 프로젝트입니다.

모델은 다음 데이터를 함께 사용합니다:

- 2023년 이후 국가대표 경기 결과
- FotMob 경기 기록을 경기 전 최근 폼 특성으로 바꾼 값
- Transfermarkt 국가대표 정보 (선수단 규모, 평균 나이, FIFA 랭킹, 총 시장 가치 등)

가장 중요한 목표는 미래 정보가 섞이지 않게(데이터 누수 방지) 하는 것입니다. 모든 예측에서 최근 폼 특성은 예측 날짜 이전에 열린 경기로만 계산합니다.

## 폴더 구성

```text
.
├── 2026Worldcuo predict.ipynb        # 메인 예측 노트북
├── WorldCup Scrape.ipynb             # 데이터 수집·준비 노트북
├── requirements.txt
├── scripts/
│   ├── build_ml_match_dataset.py
│   ├── train_baseline_model.py
│   └── collect_sofascore.py
├── data/
│   ├── processed/
│   └── raw/                          # 기본적으로 Git에서 제외
└── README_EN.md
```

## 핵심 입력 파일

현재 기본 예측 흐름은 아래 정리된 파일을 사용합니다:

```text
data/processed/fotmob_match_ids_extracted.csv
data/processed/fotmob_statistics_long.csv
data/processed/transfermarkt_country_profile.csv
```

선택 보조 파일:

```text
data/processed/worldcup48_matches_2023_plus.csv
data/processed/international_matches_2023_plus.csv
transfermarkt_country_sources.csv
```

용량이 큰 원본 수집 파일은 `.gitignore`로 일부러 GitHub에서 제외했습니다.

## 방법

과거 경기마다 다음 값을 만듭니다:

- 홈·원정 팀의 Transfermarkt 특성
- 홈·원정 Transfermarkt 특성의 차이
- 팀별 최근 5경기 평균
- 홈·원정 최근 폼 특성의 차이
- 경기 결과 정답값: `home_win`, `draw`, `away_win`

최근 경기 평균은 `shift(1)`을 사용하므로, 해당 경기 자체는 그 경기의 경기 전 특성에 들어가지 않습니다.

## 예측 설정

월드컵 예측은 `as_of_date`(기준 날짜)를 사용합니다.

예시:

```python
as_of_date = pd.Timestamp("2026-06-11")
```

뜻:

- `2026-06-11` 이전 경기만 최근 폼 계산에 사용합니다.
- 그날 이후의 월드컵 조별리그 경기는 미래 경기로 취급합니다.
- 미래 경기의 결과와 기록은 사용하지 않습니다.

## 모델

노트북에서 여러 모델을 비교할 수 있습니다:

- Logistic Regression
- Random Forest
- Extra Trees
- Gradient Boosting
- HistGradientBoosting
- XGBoost
- MLP 신경망

검증 데이터의 `log_loss`와 `accuracy`로 모델을 고르거나, 모델별 월드컵 예측 결과를 따로 살펴볼 수 있습니다.

## 결과물

이 흐름으로 만들 수 있는 것:

- 조별리그 승·무·패 확률
- 예상 스코어
- 예상 조별 순위표
- 32강 진출 팀
- 토너먼트 단계 예측
- 예상 우승팀

## 꼭 알아둘 한계

- Transfermarkt 값은 현재 팀 전력 지표로 사용합니다. 과거 시점의 시장 가치는 쓰지 않았습니다.
- FotMob 상세 기록은 경기마다 차이가 있습니다. 일부 국가대표 경기는 상세 기록이 적습니다.
- 현재 토너먼트 대진 코드는 32강 배정을 단순화했습니다. 정확한 2026 대진을 만들려면 FIFA 공식 3위 팀 배정표를 추가해야 합니다.
- 예측은 모델이 계산한 추정치이며, 결과를 보장하지 않습니다.

## 다시 실행하기

패키지 설치:

```bash
pip install -r requirements.txt
```

그다음 노트북을 위에서 아래로 실행합니다.

GitHub에는 코드, 노트북, 작은 정리 CSV 파일만 올립니다. 전체 수집 캐시를 일부러 공개하려는 경우가 아니면 `data/raw/`는 올리지 마세요.
