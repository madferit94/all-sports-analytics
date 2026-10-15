## 🏈 NFL — 경기 결과 분석 & 시뮬레이션 시스템

[English](README.md) | [한국어](README.ko.md)

**최근 경기 EPA(Rolling EPA)와 군집 분석으로 팀의 흐름(모멘텀)을 모델링합니다.**

> 시즌 평균이 아니라  
> *지금 이 팀이 얼마나 강한지*를 모델링하는 NFL 분석 시스템입니다.

---

### 🔍 이 시스템이 하는 일
- 최근 4경기 EPA로 **주차별 팀 흐름**을 추적합니다
- **고정 군집 + 변화 군집**을 함께 써서 바뀌는 팀 스타일을 잡아냅니다
- 미래 정보가 섞이지 않도록 엄격히 막은 상태에서 **경기 전 신호**를 만듭니다
- 결과를 **실시간 대화형 대시보드**로 보여줍니다

---

### 📊 실시간 대화형 대시보드
👉 [대시보드 열기*](https://all-sports-analytics-guvyfdgx7gz6qsb5yqhrvq.streamlit.app)

👉 [소스 코드 보기](https://github.com/madferit94/all-sports-analytics/tree/main/nfl-epa-analysis)

---

### 🌐 공개 대시보드
이 저장소에서 배포 중인 다른 분석 대시보드도 있습니다:

- 🏈 [NFL EPA & 승리 확률 대시보드](https://all-sports-analytics-guvyfdgx7gz6qsb5yqhrvq.streamlit.app)

- 🏎️ [F1 역대 기록 분석 대시보드](https://f1-modern-era-eda.streamlit.app)

---

### 🧠 핵심 기술 포인트
- **미래 정보 차단 설계**  
  모든 특성은 *경기 시작 전*에 알 수 있는 정보로만 계산합니다  
  (최근 경기 구간, 한 칸 미룬 정답값).
- **변하는 팀 표현**  
  팀을 시즌 요약 한 줄이 아니라 *시간에 따라 바뀌는 대상*으로 다룹니다.
- **설명 가능한 모델**  
  각 특성이 결과에 준 영향은 SHAP 분석으로 확인합니다.
- **시뮬레이션에 바로 쓰는 결과**  
  모델 결과를 시즌 시뮬레이션 단계에서 바로 쓸 수 있는 형태로 정리합니다.

---

### 🛠 사용 기술
`Python` · `Pandas` · `Scikit-learn` · `XGBoost` · `SHAP` · `Plotly` · `Streamlit`

---

## 📁 폴더 구성

```text
nfl-epa-analysis/
├── notebooks/
│   ├── 01_Data_Prep.ipynb        # 데이터 정리와 품질 점검
│   ├── 02_Clustering.ipynb       # 고정 팀 스타일 군집
│   ├── 03_Feature_Eng.ipynb      # 최근 경기 EPA와 변화 특성
│   ├── 04_Modeling.ipynb         # 승리 확률 모델 + SHAP
│   └── 05_Simulation.ipynb       # 시즌 단위 몬테카를로 시뮬레이션
│
├── data/
│   └── processed/                # 경기 전 기준, 미래 정보가 없는 데이터
│
├── streamlit_app/
│   ├── app.py                    # 배포된 Streamlit 대시보드
│   └── requirements.txt          # 대시보드 실행 패키지
│
└── README.md                     # 프로젝트 문서 (영어)
