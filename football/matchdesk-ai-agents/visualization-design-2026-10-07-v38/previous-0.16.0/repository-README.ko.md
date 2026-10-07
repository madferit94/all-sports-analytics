# MatchLab0.16.0 · F1 서킷 지도 비교

# MatchLab 0.15.0 · F1 경기 전 예측과 실제 진행 비교

# MatchLab 0.14.0 · F1 기록 재생 및 실험 예측

# 🏟️ All Sports Analytics & Simulation Hub

[English](README.md) | [한국어](README.ko.md)

[MatchDesk 영어 화면](football/matchdesk-ai-agents/index.en.html) · PL + LaLiga, 56 clubs, Korean/English UI.

MatchDesk: **Day13 작업** · [폴더 이동 기록](football/matchdesk-ai-agents/docs/DAY13-WORKSPACE.md).

## MatchLab AI 경기 분석실 · 0.13.0

PL·라리가 한영8비트 화면: 전체팀 로지스틱 승부예측, 학습한 득점분포, 움직이는22명경기연출, 일정더보기·경기프리뷰,57지표선택차트. 입력은2026-09-20고정자료이며과거검증결과로미래성능을보장하지않습니다.

[프로젝트·버전이력](football/matchdesk-ai-agents/README.ko.md) · [릴리스SPEC](football/matchdesk-ai-agents/docs/SPEC-0.13.0.md) · [에이전트·스킬영어판](football/matchdesk-ai-agents/docs/AGENTS-AND-SKILLS.en.md) · [한글화면](football/matchdesk-ai-agents/index.html) · [영어화면](football/matchdesk-ai-agents/index.en.html).

v20~v32이전버전과독립차트검증근거를보존합니다. 현재5인팀·이전10역할및18개스킬의영어판을제공하며, 도구·계약은한글패키지와공유합니다. 별도Claude실행환경검증또는인터넷서비스호스팅을완료했다는뜻은아닙니다.


NFL, F1, 축구를 비롯한 스포츠 데이터 분석·예측·시뮬레이션 프로젝트를 모은 저장소입니다.

## 목표와 접근 방법

데이터 수집에서 정제, 분석, 예측 모델과 시뮬레이션까지 이어지는 스포츠 데이터 포트폴리오입니다. 프로젝트마다 진행 단계와 재현 방법을 확인할 수 있습니다.

1. **체계적인 처리:** 수집·정제·특성 생성에서 분석과 모델링으로 이어지는 흐름을 구성합니다.
2. **검증 목표:** 경기 전 정보와 시간 순서 검증을 지향하며, 기존 F1의 누수·정답 문제는 프로젝트 검토에 명시합니다.
3. **모델 해석:** 중요도와 설명 도구로 모델 동작을 검토합니다.
4. **의사결정 연결:** 승리 확률, 순위표와 대회 시뮬레이션 등 해석 가능한 결과를 만듭니다.

## 완료한 프로젝트

### 🏈 NFL 경기 결과 시뮬레이션

군집화와 몬테카를로 시뮬레이션을 이용한 NFL 시즌 예측 프로젝트입니다.

- **목표:** 경기 승자를 예측하고 최근 흐름을 반영한 슈퍼볼 확률을 계산합니다.
- **상태:** 완료.
- **프로젝트:** [nfl-epa-analysis](nfl-epa-analysis)

### 🏎️ F1 경기 맥락과 과거 탐색 분석

- **바쿠 2026:** 러셀–베르스타펜 공식 시간 차이·세이프티카·이동 영상. [영어·한글 주석 코드, 실행 노트북, 자료와 결과](f1/baku-2026/README.ko.md).
- **현재 상태:** 탐색 시각화 재현 완료. 시간 기반 최종 비교 랩 선정과 공개 페이스 결론은 남아 있습니다.
- **과거 작업:** [EDA](f1-modern-era-eda/README.ko.md)는 유지하며 DNF·범위 수정이 필요합니다. 경기 전 예측 프로토타입은 수정·재검증을 위해 별도 비공개 저장소로 옮겼습니다.
- **시작하기:** [F1 전체 목록](f1/README.ko.md) · [기존 작업 검토](f1/baku-2026/docs/existing_f1_review.ko.md).

### ⚽ 2026 월드컵 경기 예측과 대회 시뮬레이션

과거 국가대표 경기, FotMob 경기 통계와 Transfermarkt 국가대표 프로필을 사용한 예측 프로젝트입니다.

- **목표:** 조별리그 결과 예측, 여러 모델 비교, 단순화한 토너먼트 시뮬레이션과 모델별 우승팀 비교.
- **상태:** 기준 모델 완료.
- **Kaggle:** [2026 FIFA World Cup Prediction](https://www.kaggle.com/code/madferit/2026-fifa-world-cup-prediction)
- **프로젝트:** [football/worldcup-2026-prediction](football/worldcup-2026-prediction)
- **주요 노트북:** [2026Worldcup predict.ipynb](football/worldcup-2026-prediction/2026Worldcup%20predict.ipynb)
- **데이터 패키지:** [kaggle_dataset](football/worldcup-2026-prediction/kaggle_dataset)

### ⚽ Beyond Goals — 유럽 5대 리그 공격수 프로필, 2025/26

- **질문:** 슈팅 빈도·기회 품질·실제 득점 전환은 선수별로 어떻게 다른가?
- **상태:** 기술적 분석, 영어·한글 주석 코드와 실행 노트북, 영어 발표 자료 13장 완료. 저장 자료·분석·PPT 교차 검증 77개 통과.
- **범위:** 검증된 중앙 공격수 후보 181명, 비페널티 슈팅 8,847개. 리그 수준과 경기 맥락은 보정하지 않았습니다.
- **프로젝트:** [한국어](football/big-five-striker-profiles/README.ko.md) · [English](football/big-five-striker-profiles/README.md)
- **보기:** [LinkedIn PDF](football/big-five-striker-profiles/presentation/Beyond_Goals_EN_Landscape_verified.pdf) · [분석 코드·노트북](football/big-five-striker-profiles/analysis)

## 진행 중인 프로젝트와 후속 계획

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

프로젝트에 따라 사용하는 도구가 다릅니다. 스트라이커 데이터 수집·CSV 검증은 표준 라이브러리를 사용하며, 분석·발표 교차 검증은 별도 requirements를 확인하세요.

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

[F1 분석실](football/matchdesk-ai-agents/f1/index.html)
