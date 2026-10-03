# 🏟️ All Sports Analytics & Simulation Hub

[English](README.md) | [한국어](README.ko.md)

NFL, F1, 축구를 비롯한 스포츠 데이터 분석·예측·시뮬레이션 프로젝트를 모은 저장소입니다.

## 목표와 접근 방법

데이터 수집에서 정제, 분석, 예측 모델과 시뮬레이션까지 이어지는 스포츠 데이터 포트폴리오입니다. 프로젝트마다 진행 단계와 재현 방법을 확인할 수 있습니다.

1. **체계적인 처리:** 수집·정제·특성 생성에서 분석과 모델링으로 이어지는 흐름을 구성합니다.
2. **데이터 누수 방지:** 경기 전 정보, 과거 기간 집계와 시간 순서에 맞는 검증을 사용합니다.
3. **모델 해석:** 중요도와 설명 도구로 모델 동작을 검토합니다.
4. **의사결정 연결:** 승리 확률, 순위표와 대회 시뮬레이션 등 해석 가능한 결과를 만듭니다.

## 완료한 프로젝트

### 🏈 NFL 경기 결과 시뮬레이션

군집화와 몬테카를로 시뮬레이션을 이용한 NFL 시즌 예측 프로젝트입니다.

- **목표:** 경기 승자를 예측하고 최근 흐름을 반영한 슈퍼볼 확률을 계산합니다.
- **상태:** 완료.
- **프로젝트:** [nfl-epa-analysis](nfl-epa-analysis)

### 🏎️ F1 현대 시대 레이스 전략 시스템

2016년 이후 하이브리드 시대를 대상으로 두 가지 목표를 다루는 예측 모델입니다.

- **목표:** 드라이버·팀 성과를 분석하고 레이스 결과와 안정적인 포인트 획득을 예측합니다.
- **상태:** 완료.
- **프로젝트:** [f1-modern-era-prediction](f1-modern-era-prediction)

### ⚽ 2026 월드컵 경기 예측과 대회 시뮬레이션

과거 국가대표 경기, FotMob 경기 통계와 Transfermarkt 국가대표 프로필을 사용한 예측 프로젝트입니다.

- **목표:** 조별리그 결과 예측, 여러 모델 비교, 단순화한 토너먼트 시뮬레이션과 모델별 우승팀 비교.
- **상태:** 기준 모델 완료.
- **Kaggle:** [2026 FIFA World Cup Prediction](https://www.kaggle.com/code/madferit/2026-fifa-world-cup-prediction)
- **프로젝트:** [football/worldcup-2026-prediction](football/worldcup-2026-prediction)
- **주요 노트북:** [2026Worldcup predict.ipynb](football/worldcup-2026-prediction/2026Worldcup%20predict.ipynb)
- **데이터 패키지:** [kaggle_dataset](football/worldcup-2026-prediction/kaggle_dataset)

## 진행 중인 프로젝트와 후속 계획

### ⚽ 유럽 5대 리그 스트라이커 프로필 — 2025/26

비페널티 슈팅 빈도와 슈팅당 평균 기회 품질을 비교하기 위한 선수 프로필 데이터입니다.

- **질문:** 중앙 공격수 후보 중 누가 슈팅을 자주 기록하며, 누가 더 높은 xG의 기회를 얻거나 선택하는가?
- **상태:** 데이터 수집·검증 완료. 산점도 분석과 경기 맥락에 따른 해석은 다음 단계입니다.
- **범위:** 1,752경기, 상세 선수 1,013명, 최소 900분 기준을 충족하고 검증을 통과한 후보 181명. 원천 중복 문제의 영향을 받은 선수·리그 기록 12행은 제외했습니다.
- **프로젝트:** [한국어 문서](football/big-five-striker-profiles/README.ko.md) · [English documentation](football/big-five-striker-profiles/README.md)
- **재현:** 공개 CSV는 Python 표준 라이브러리만으로 오프라인 검증할 수 있습니다. 원본 캐시는 로컬에 보존합니다.

### ⚽ K리그 1 2026 월드컵 휴식기 분석

1–15라운드와 16–30라운드를 비교한 네 단계의 기술적 분석입니다. 리그 전체의 공격·수비·패스 패턴에서 안양·대전·제주 사례로 이어집니다.

- **상태:** 1–30라운드 분석 완료. 2026시즌 종료 후 후속 분석 예정.
- **범위:** 연기된 강원–인천 경기를 포함한 180경기. 예측·인과 모델이 아닌 관측 기록의 비교입니다.
- **프로젝트:** [코드, 실행 노트북, 결과와 후속 계획](football/kleague-2026-world-cup-break)
- **재현:** 집계 결과와 실행된 노트북을 제공합니다. 원천 제공자의 내보내기 파일은 로컬에서 준비해야 합니다.

### ⚽ 유럽 리그 경기 예측

- **구상:** 기대득점(xG)에 기반한 경기 예측.
- **예정 요소:** 최근 팀 흐름, 홈 이점과 포아송 분포 모델.

### 🏀 NBA

- **구상:** Four Factors 분석과 포제션 단위 모델링.
- **예정 요소:** 선수 유형 군집화와 라인업 효율 분석.

### 📊 스포츠 외 분야

- **구상:** 같은 분석 흐름을 금융·마케팅 데이터에 적용.

## 기술과 도구

- **언어:** Python 3.10 이상, SQL. 스트라이커 프로젝트는 Python 3.11 이상.
- **데이터 처리:** Pandas, NumPy, Polars.
- **머신러닝:** Scikit-learn, XGBoost, LightGBM, Random Forest.
- **해석:** SHAP.
- **시뮬레이션:** 몬테카를로, 부트스트래핑, 대회 시뮬레이션.
- **시각화:** Matplotlib, Seaborn, Plotly.
- **앱:** Streamlit.

프로젝트에 따라 사용하는 도구가 다릅니다. 스트라이커 데이터 수집·검증에는 외부 패키지가 필요 없습니다.

## 저장소 구성

프로젝트별로 다음 구성을 기본으로 사용하며 실제 구조는 각 README에 설명합니다.

```text
project-name/
├── notebooks/   # 분석·모델링 노트북
├── data/        # 데이터
├── scripts/     # 재사용 코드
└── README.md    # 프로젝트 설명
```

월드컵 예측 프로젝트에는 `football/worldcup-2026-prediction/kaggle_dataset/` 아래에 README, 입력과 결과를 포함한 Kaggle용 패키지가 있습니다.

## 작성자와 연락처

- **작성자:** madferit94
- **이메일:** wowzc@naver.com
- **GitHub:** [madferit94](https://github.com/madferit94)
