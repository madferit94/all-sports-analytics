# 🏟️ All Sports Analytics

[English](README.md) | [한국어](README.ko.md)

**축구, F1, NFL 데이터를 분석한 프로젝트 모음입니다.**
각 프로젝트는 질문에서 출발해 데이터와 방법을 기록하고, 한계를 함께 적습니다.

> 🏎️⚽ **MatchLab을 찾으시나요?** AI 에이전트로 만든 축구·F1 웹 서비스는 별도 저장소에서 관리합니다: [madferit94/matchlab](https://github.com/madferit94/matchlab) ([사이트 바로가기](https://matchlab-zeta.vercel.app))

---

## 📂 프로젝트 목록

| 종목 | 프로젝트 | 질문 | 상태 |
|---|---|---|---|
| ⚽ | [Beyond Goals — 빅5 리그 공격수 프로필](football/big-five-striker-profiles) | 공격수 유형별로 슈팅 수, 기회의 질, 결정력은 어떻게 다른가? | ✅ 완료 |
| ⚽ | [K리그1 2026: 월드컵 휴식기 분석](football/kleague-2026-world-cup-break) | 월드컵 휴식기 전후로 공격·수비·패스 패턴은 어떻게 바뀌었나? | ✅ 1~30라운드 완료 |
| ⚽ | [2026 월드컵 예측](football/worldcup-2026-prediction) | 과거 경기와 팀 지표로 조별리그 결과를 예측할 수 있을까? | ✅ 기본 모델 |
| ⚽ | [2026 월드컵 공식 기록 분석](football/worldcup-2026-official-stats-analysis) | 팀들은 어떻게 슈팅을 만들고, 전진하고, 막아냈나? | ✅ 기술 분석 |
| 🏎️ | [F1 바쿠 2026](f1/baku-2026) | 세이프티카 전후로 러셀–베르스타펜 간격은 어떻게 변했나? | 🔄 탐색 단계 |
| 🏎️ | [F1 역대 기록 EDA](f1-modern-era-eda) | 시대별 완주율, 포인트, 신뢰성은 어떻게 달라졌나? | 🛠️ 프로토타입, 수정 필요 |
| 🏈 | [NFL 모멘텀 & 시뮬레이션](nfl-epa-analysis) | 최근 경기 EPA로 팀의 *현재* 전력을 잡아낼 수 있을까? | ✅ 완료 |

---

## ⚽ 축구

### Beyond Goals — 빅5 리그 공격수 프로필 (2025/26)
- **범위:** 중앙 공격수 후보 181명, 페널티 제외 슈팅 8,847개. 리그 수준과 경기 상황은 보정하지 않았습니다.
- **결과물:** 한영 스크립트와 실행된 노트북, 영문 발표자료 13장, 저장 데이터·분석 검증 77개.
- **링크:** [English](football/big-five-striker-profiles/README.md) · [한국어](football/big-five-striker-profiles/README.ko.md) · [발표자료 (PDF)](football/big-five-striker-profiles/presentation/Beyond_Goals_EN_Landscape_verified.pdf)

### K리그1 2026: 월드컵 휴식기 분석
- **범위:** 180경기, 1~15라운드와 16~30라운드 비교. 안양·대전·제주 사례 분석 포함. 기술 분석이며 인과 분석은 아닙니다.
- **다음 단계:** 2026 시즌 종료 후 후속 분석 예정.
- **참고:** 집계 결과와 실행된 노트북은 포함되어 있고, 원본 데이터는 직접 준비해야 합니다.

### 2026 월드컵 예측
- **데이터:** 역대 국가대표 경기, FotMob 경기 기록, Transfermarkt 대표팀 정보.
- **방법:** 여러 머신러닝 모델 비교, 간소화한 토너먼트 시뮬레이션.
- **링크:** [Kaggle 노트북](https://www.kaggle.com/code/madferit/2026-fifa-world-cup-prediction) · [메인 노트북](football/worldcup-2026-prediction/2026Worldcup%20predict.ipynb) · [데이터셋 패키지](football/worldcup-2026-prediction/kaggle_dataset)

### 2026 월드컵 공식 기록 분석
- FIFA Match Centre 팀 데이터로 필드 틸트, 전진 패스, 파이널 서드 진입, 오프더볼 움직임, 슈팅 억제를 분석한 노트북 8개.
- 정제된 입력 CSV는 포함되어 있지 않아, 다시 실행하려면 직접 추가해야 합니다.

---

## 🏎️ F1

- **[바쿠 2026](f1/baku-2026):** OpenF1 데이터로 타이밍 간격, 세이프티카 상황, 트랙 재생을 분석. 한영 주석이 달린 스크립트와 실행된 노트북 포함. 최종 페이스 비교 기준은 아직 검토 중입니다.
- **[역대 기록 EDA 대시보드](f1-modern-era-eda):** 기존 Streamlit 프로토타입을 보존. 포트폴리오로 쓰기 전에 리타이어 정의와 경기 수 계산을 고쳐야 합니다.
- 이전 경기 전 예측 프로토타입은 데이터 누수 수정과 재검증을 위해 비공개 저장소로 옮겼습니다. [검토 기록](f1/baku-2026/docs/existing_f1_review.md)

---

## 🏈 NFL

- **[모멘텀 & 시뮬레이션](nfl-epa-analysis):** 주간 Rolling EPA, 정적·동적 팀 군집화, 데이터 누수를 막은 경기 전 지표, Streamlit 대시보드.

---

## 🛠️ 사용한 도구

- **언어:** Python, SQL
- **데이터 처리:** pandas, NumPy
- **모델링:** scikit-learn, XGBoost, SHAP
- **시각화:** Matplotlib, Seaborn, Plotly, mplsoccer
- **앱:** Streamlit

---

## 👤 만든 사람

**엄민섭 (madferit94)** — 스포츠 AI·빅데이터 석사, 데이터 품질·운영 실무 경험을 가진 데이터 분석가.

- Email: wowzc@naver.com
- GitHub: [@madferit94](https://github.com/madferit94)
