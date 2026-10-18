# 🏟️ All Sports Analytics

[English](README.md) | [한국어](README.ko.md)

**A collection of sports data analysis projects across football, F1 and the NFL.**
Each project starts from a question, documents its data and method, and states its limitations.

> 🏎️⚽ **Looking for MatchLab?** The football & F1 web app built with AI agents now lives in its own repository: [madferit94/matchlab](https://github.com/madferit94/matchlab) ([live site](https://matchlab-zeta.vercel.app)).

---

## 📂 Projects

| Sport | Project | Question | Status |
|---|---|---|---|
| ⚽ | [Beyond Goals — Big Five Striker Profiles](football/big-five-striker-profiles) | How do shot volume, chance quality and conversion differ across striker profiles? | ✅ Complete |
| ⚽ | [K League 1 2026: World Cup Break](football/kleague-2026-world-cup-break) | How did attack, defense and passing change before and after the World Cup break? | ✅ R1–30 complete |
| ⚽ | [World Cup 2026 Prediction](football/worldcup-2026-prediction) | Can historical results and team stats predict group-stage outcomes? | ✅ Baseline |
| ⚽ | [World Cup 2026 Official Stats](football/worldcup-2026-official-stats-analysis) | How did teams create, progress and suppress shots? | ✅ Descriptive |
| 🏎️ | [F1 Baku 2026](f1/baku-2026) | How did Russell–Verstappen gaps evolve around Safety Cars? | 🔄 Exploratory |
| 🏎️ | [F1 Historical EDA](f1-modern-era-eda) | How do finishing, points and reliability vary historically? | 🛠️ Prototype, corrections needed |
| 🏈 | [NFL Momentum & Simulation](nfl-epa-analysis) | Can rolling EPA capture how strong a team is *right now*? | ✅ Complete |

---

## ⚽ Football

### Beyond Goals — Big Five Striker Profiles, 2025/26
- **Coverage:** 181 central-forward candidates, 8,847 non-penalty shots. League strength and context are not adjusted.
- **Output:** Bilingual scripts and executed notebooks, a 13-slide English deck, 77 saved-data/analysis checks.
- **Links:** [English](football/big-five-striker-profiles/README.md) · [한국어](football/big-five-striker-profiles/README.ko.md) · [Deck (PDF)](football/big-five-striker-profiles/presentation/Beyond_Goals_EN_Landscape_verified.pdf)

### K League 1 2026: World Cup Break Analysis
- **Scope:** 180 fixtures, rounds 1–15 vs 16–30, with Anyang, Daejeon and Jeju case studies. Descriptive, not causal.
- **Next:** Season-end follow-up after the 2026 season.
- **Note:** Aggregate results and executed notebooks are included; raw provider exports must be supplied locally.

### World Cup 2026 Prediction
- **Data:** Historical international matches, FotMob match stats, Transfermarkt team profiles.
- **Method:** Multiple ML models compared, simplified knockout bracket simulation.
- **Links:** [Kaggle notebook](https://www.kaggle.com/code/madferit/2026-fifa-world-cup-prediction) · [Main notebook](football/worldcup-2026-prediction/2026Worldcup%20predict.ipynb) · [Dataset package](football/worldcup-2026-prediction/kaggle_dataset)

### World Cup 2026 Official Stats Analysis
- Eight descriptive notebooks on field tilt, progression, final-third access, off-ball movement and shot suppression, using FIFA Match Centre team data.
- The cleaned input CSV is not included; add it locally to rerun.

---

## 🏎️ Formula 1

- **[Baku 2026](f1/baku-2026):** Timing gaps, Safety Car context and track replay using OpenF1. Bilingual commented scripts and executed notebooks. Final pace eligibility is still pending.
- **[Historical EDA dashboard](f1-modern-era-eda):** Preserved Streamlit prototype. DNF definitions and race counts need correction before portfolio use.
- The earlier pre-race prediction prototype was moved to a private repository for leakage fixes and revalidation. [Review](f1/baku-2026/docs/existing_f1_review.md)

---

## 🏈 NFL

- **[Momentum & Simulation](nfl-epa-analysis):** Week-by-week rolling EPA, static and dynamic team clustering, pre-game signals with leakage prevention, and a Streamlit dashboard.

---

## 🛠️ Tools used in these projects

- **Languages:** Python, SQL
- **Data:** pandas, NumPy
- **Modeling:** scikit-learn, XGBoost, SHAP
- **Visualization:** Matplotlib, Seaborn, Plotly, mplsoccer
- **Apps:** Streamlit

---

## 👤 Author

**Minseob Eom (madferit94)** — Data analyst with a master's degree in Sport AI and Big Data, and hands-on experience in data quality and operations.

- Email: wowzc@naver.com
- GitHub: [@madferit94](https://github.com/madferit94)
