# 🏟️ All Sports Analytics & Simulation Hub

[English](README.md) | [한국어](README.ko.md)

[English MatchLab site](football/matchdesk-ai-agents/index.en.html) · PL + LaLiga, 56 clubs, Korean/English UI.

MatchLab: **Day13** · [workspace location](football/matchdesk-ai-agents/docs/DAY13-WORKSPACE.md).

## MatchLab football agent project · 0.12.2

Korean/English 8-bit viewer for PL and LaLiga: selected all-team logistic predictions, learned score distributions, moving 22-player simulations, fixture previews and 57 selectable team metrics. Input records are a fixed 2026-09-20 snapshot; retrospective evaluation does not establish future performance.

[Project / version history](football/matchdesk-ai-agents/README.md) · [Release SPEC](football/matchdesk-ai-agents/docs/SPEC-0.12.2.md) · [English agents and skills](football/matchdesk-ai-agents/docs/AGENTS-AND-SKILLS.en.md) · [Korean site](football/matchdesk-ai-agents/index.html) · [English site](football/matchdesk-ai-agents/index.en.html).

Preserved viewer versions v20–v33 and independent chart evidence are included. English packages mirror the current five-agent team, legacy ten roles and 18 skills. Tools/contracts are shared with the Korean packages; no separate Claude runtime or hosted service is claimed.


**A Unified Quantitative Analysis Repository for NFL, F1, Football, and Beyond.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-EB4034?style=for-the-badge)
![SHAP](https://img.shields.io/badge/SHAP-Explainable_AI-ff00ff?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active_Development-success?style=for-the-badge)

---

## 🎯 Vision & Purpose

This repository is a centralized **portfolio of end-to-end sports data science systems**.
Each project is designed as a full-cycle analytics pipeline, from data collection and feature engineering to predictive modeling and simulation.

### **Core Philosophy**

1. **Systematic Approach:** From ETL and data engineering to modeling and simulation.
2. **Validation Goal:** Pre-game constraints and time-aware validation; known F1 leakage and target defects are documented in the project review.
3. **Explainable AI:** Going beyond accuracy to understand model behavior with feature importance and explainability tools.
4. **Business Value:** Turning model outputs into actionable insights such as win probabilities, ranking tables, and tournament simulations.

---

## 🏆 Completed Projects

### 🏈 **[NFL] Match Outcome Simulation System**
A dynamic prediction engine for the NFL season, featuring clustering and Monte Carlo simulations.

* **Goal:** Predict game winners and simulate Super Bowl probabilities based on momentum.
* **Status:** ✅ Completed
* **View Project:** [👉 Go to NFL Project](https://github.com/madferit94/all-sports-analytics/tree/main/nfl-epa-analysis)

### 🏎️ **[F1] Race Context and Historical Prototypes**

* **Baku 2026:** Russell–Verstappen timing gaps, Safety Car context, and track replay. [Bilingual scripts, executed notebooks, data, and outputs](f1/baku-2026).
* **Current status:** Reproducible exploratory visuals; final temporal lap eligibility and public pace conclusions remain pending.
* **Historical work:** [EDA dashboard](f1-modern-era-eda) remains a prototype requiring DNF and scope corrections. The pre-race prediction prototype has been moved to a separate private repository pending corrections and revalidation.
* **Start here:** [F1 project index](f1) · [Existing-work review](f1/baku-2026/docs/existing_f1_review.md).

### ⚽ **[World Cup 2026] Match Prediction and Tournament Simulation**
A 2026 FIFA World Cup prediction workflow using historical international matches, FotMob match statistics, and Transfermarkt national team profiles.

* **Goal:** Predict group-stage results, compare multiple ML models, simulate a simplified knockout bracket, and compare predicted champions by model.
* **Status:** ✅ Completed baseline
* **Kaggle Notebook:** https://www.kaggle.com/code/madferit/2026-fifa-world-cup-prediction
* **Project Folder:** [`football/worldcup-2026-prediction`](football/worldcup-2026-prediction)
* **Main Notebook:** [`football/worldcup-2026-prediction/2026Worldcup predict.ipynb`](football/worldcup-2026-prediction/2026Worldcup%20predict.ipynb)
* **Dataset Package:** [`football/worldcup-2026-prediction/kaggle_dataset`](football/worldcup-2026-prediction/kaggle_dataset)

---

### ⚽ Beyond Goals — Big Five Striker Profiles, 2025/26

* **Question:** How do shot volume, chance quality and scoring conversion differ across striker profiles?
* **Status:** Descriptive analysis, bilingual scripts/executed notebooks and a 13-slide English deck complete; 77 saved-data/analysis/PPT checks pass.
* **Coverage:** 181 validated central-forward candidates; 8,847 non-penalty shots. Context and league strength are not adjusted.
* **Project:** [English](football/big-five-striker-profiles/README.md) · [한국어](football/big-five-striker-profiles/README.ko.md)
* **View:** [LinkedIn PDF](football/big-five-striker-profiles/presentation/Beyond_Goals_EN_Landscape_verified.pdf) · [Analysis code and notebooks](football/big-five-striker-profiles/analysis)

## 🚧 Upcoming & Planned Projects

### ⚽ K League 1 2026: World Cup Break Analysis

An English, four-stage descriptive analysis comparing rounds 1–15 with rounds 16–30, from league-wide attack, defense and passing patterns to Anyang, Daejeon and Jeju case studies.

* **Status:** Completed R1–30 analysis; season-end follow-up planned after the 2026 season concludes.
* **Scope:** 180 fixtures, including the postponed Gangwon–Incheon match; not a prediction or causal model.
* **Project:** [Code, executed notebooks, results and future work](football/kleague-2026-world-cup-break)
* **Reproducibility:** Public aggregate results and executed notebooks are included; raw provider exports must be supplied locally.

### **⚽ Football: European Leagues**
* **Concept:** Expected Goals based match prediction.
* **Features:** Rolling team form, home advantage dynamics, Poisson distribution modeling.

### **🏀 NBA**
* **Concept:** Four Factors analytics and possession-based modeling.
* **Features:** Player archetype clustering and lineup efficiency analysis.

### **📊 Beyond Sports**
* **Concept:** Applying the same rigorous modeling pipelines to financial or marketing data.

---

## 🛠️ Tech Stack & Toolkit

* **Languages:** Python 3.10+, SQL
* **Data Manipulation:** Pandas, NumPy, Polars
* **Machine Learning:** Scikit-learn, XGBoost, LightGBM, Random Forest
* **Interpretability:** SHAP
* **Simulation:** Monte Carlo methods, bootstrapping, tournament simulation
* **Visualization:** Matplotlib, Seaborn, Plotly
* **Apps:** Streamlit

---

## 📌 Repository Structure

Project folders and notebooks follow this general structure:

```text
/project-name/
│
├── notebooks/               # Analysis and modeling notebooks
├── data/                    # Raw and processed datasets
├── scripts/                 # Reusable data/model scripts
└── README.md                # Project-specific documentation
```

The current World Cup project also includes a Kaggle-ready dataset package:

```text
football/worldcup-2026-prediction/kaggle_dataset/
├── README.md
├── input/
└── outputs/
```

---

## 👤 Author

madferit94
Sports Data Analyst & System Architect

> Transforming raw data into strategic foresight.

## 📬 Contact

Email: wowzc@naver.com
GitHub: https://github.com/madferit94
