# 🏟️ All Sports Analytics & Simulation Hub
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
2. **Leakage-Proof Modeling:** Strict use of pre-game constraints, rolling windows, and time-aware validation.
3. **Explainable AI:** Going beyond accuracy to understand model behavior with feature importance and explainability tools.
4. **Business Value:** Turning model outputs into actionable insights such as win probabilities, ranking tables, and tournament simulations.

---

## 🏆 Completed Projects

### 🏈 **[NFL] Match Outcome Simulation System**
A dynamic prediction engine for the NFL season, featuring clustering and Monte Carlo simulations.

* **Goal:** Predict game winners and simulate Super Bowl probabilities based on momentum.
* **Status:** ✅ Completed
* **View Project:** [👉 Go to NFL Project](https://github.com/madferit94/all-sports-analytics/tree/main/nfl-epa-analysis)

### 🏎️ **[F1] Modern-Era Race Strategy System**
A dual-objective predictive model for Formula 1, optimized for the post-2016 hybrid era.

* **Goal:** Analyze driver/team performance and forecast race outcomes vs. consistent point scoring.
* **Status:** ✅ Completed
* **View Project:** [👉 Go to F1 Project](https://github.com/madferit94/all-sports-analytics/tree/main/f1-modern-era-prediction)

### ⚽ **[World Cup 2026] Match Prediction and Tournament Simulation**
A 2026 FIFA World Cup prediction workflow using historical international matches, FotMob match statistics, and Transfermarkt national team profiles.

* **Goal:** Predict group-stage results, compare multiple ML models, simulate a simplified knockout bracket, and compare predicted champions by model.
* **Status:** ✅ Completed baseline
* **Kaggle Notebook:** https://www.kaggle.com/code/madferit/2026-fifa-world-cup-prediction
* **Project Folder:** [`football/worldcup-2026-prediction`](football/worldcup-2026-prediction)
* **Main Notebook:** [`football/worldcup-2026-prediction/2026Worldcup predict.ipynb`](football/worldcup-2026-prediction/2026Worldcup%20predict.ipynb)
* **Dataset Package:** [`football/worldcup-2026-prediction/kaggle_dataset`](football/worldcup-2026-prediction/kaggle_dataset)

---

## 🚧 Upcoming & Planned Projects

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
