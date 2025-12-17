# 🏈 NFL Match Outcome Prediction & Season Simulation System (2024-2025)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-EB4034?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

## 📖 Executive Summary

This project represents an **end-to-end sports quantitative analysis system** designed to predict NFL game outcomes and simulate the 2024 season. 

Unlike traditional static models, this system implements a **Dynamic Clustering Framework** to track team momentum week-by-week and utilizes a **Monte Carlo Simulation** engine to quantify uncertainty. The core objective is to generate actionable business insights—specifically **Win Probabilities** and **Super Bowl Odds**—that are comparable to Vegas betting lines.

The system is built on a strict **Data Leakage Prevention** protocol, utilizing time-series rolling windows to ensure all predictions are based solely on information available pre-game.

---

## 🚀 Key Technical Features

### 1. Dynamic Team Style Clustering (The "Living" Metric)
Most models treat teams as static entities (e.g., "KC is a strong team"). This system treats them as **evolving entities**.
* **Static Reference (File 02):** Establishes a "Global Standard" for team tiers (Elite, Balanced, Struggling) using historical data (2019-2024).
* **Dynamic Tracking (File 03):** Applies a rolling window (last 4 games) to the global standard. This allows the model to detect if an "Elite" team is currently in a "Struggling" phase.

### 2. Leakage-Proof Feature Engineering
* **Rolling Windows:** Used `.shift(1)` logic to calculate metrics (EPA, Win Rate) strictly from *previous* games.
* **Prior Season Anchoring:** Solved the "Cold Start Problem" (Week 1-3) by incorporating previous season performance as Bayesian priors.

### 3. Explainable AI & Simulation
* **SHAP Analysis:** Deconstructed the "Black Box" to reveal that *Recent Rolling EPA* and *Prior Season Quality* are the dominant predictors.
* **Monte Carlo Simulation:** Simulated the 2024 season **10,000 times** to derive robust probability distributions for playoff berths and Super Bowl wins.

---

## 📂 Project Pipeline (File Structure)

This project follows a professional **ETL → Feature Engineering → Modeling → Application** workflow.

| Seq | Notebook Name | Role | Key Function |
| :--- | :--- | :--- | :--- |
| **01** | `01_NFL_Data_Prep_and_EDA.ipynb` | **ETL & Data QC** | Ingests raw PBP data via `nfl_data_py`, cleanses EPA metrics, and performs league-wide EDA to validate data integrity. |
| **02** | `02_NFL_Team_Style_Clustering.ipynb` | **Static Analysis** | Uses **K-Means** to define the "Global Reference" for team styles (e.g., *Defense-First*, *High-Octane Offense*). |
| **03** | `03_NFL_Dynamic_Feature_Generation.ipynb` | **Feature Eng.** | Generates **Dynamic Cluster Labels** and **Rolling EPA** features. This creates the "Pulse" of the team for every game week. |
| **04** | `04_NFL_Win_Prediction_Model.ipynb` | **Modeling Engine** | Trains the Win Probability Model (Logistic/RF/XGB) using the dynamic features. Includes **SHAP** interpretation. |
| **05** | `05_NFL_Season_Simulation.ipynb` | **Production** | Simulates the 2024 season loop (Game -> Update Stats -> Next Game) to forecast **Expected Wins** and **Super Bowl Odds**. |

---

## 📊 Model Performance & Insights

### Validation Results (2024 Test Set)
* **Accuracy:** ~65% (Competitive with market baselines)
* **Calibration:** Validated using Brier Score to ensure probability estimates reflect reality.

### Key Insights from SHAP
1.  **Momentum Matters:** *Rolling Offensive EPA (Last 4 Games)* is the single strongest predictor of future success.
2.  **Stickiness of Quality:** *Previous Season Win %* remains a significant predictor even late into the season, suggesting "Team Culture/Coaching" has a lasting impact.
3.  **Styles Make Fights:** The *Dynamic Cluster* features provided incremental lift, helping the model adjust when a team's statistical profile shifted drastically (e.g., due to QB injury).

---

## 🎲 Simulation Results (2024 Season)

*Based on 10,000 Monte Carlo Simulations (Actual Model Output):*

| Rank | Team | Projected Wins | Super Bowl Win Prob (%) |
| :---: | :--- | :---: | :---: |
| **1** | **PHI** (Eagles) | 13.5 | **42.0%** |
| **2** | **BUF** (Bills) | 12.7 | 19.2% |
| **3** | **BAL** (Ravens) | 12.4 | 15.1% |
| **4** | **KC** (Chiefs) | 11.6 | 6.4% |
| **5** | **DET** (Lions) | 10.8 | 2.9% |

> *Note: While popular consensus favors KC, the model's EPA-driven simulation heavily favors PHI and BUF due to their superior rolling efficiency metrics in the simulation dataset.*

---

## ⚠️ Limitations & Future Work

* **Injury Agnostic:** The current model is "Power-Rated" based on team performance. It does not explicitly account for real-time injury reports (e.g., QB1 out).
* **Scope:** Optimized for the "Modern Passing Era" (2019-2024).
* **Future Plan:** Integrate player-level telemetry data to adjust team ratings dynamically when key starters are missing.

---

---

## 📊 Live Interactive Dashboard

This project includes a **production-grade Streamlit dashboard** that visualizes:
- Dynamic Team EPA Landscape
- Pre-game Win Probabilities
- Team Momentum (Rolling EPA)

👉 **Try Live Dashboard:**  
🔗 https://YOUR-STREAMLIT-APP-NAME.streamlit.app

👉 **Dashboard Source Code:**  
🔗 https://github.com/madferit94/all-sports-analytics/tree/main/nfl-epa-analysis/streamlit_app

---

### 👤 Author

**MinseoB Eom**
*Sports Data Analyst & System Architect*
*(Please insert your email or LinkedIn profile link here)*

Email: wowzc@naver.com
GitHub: https://github.com/madferit94
