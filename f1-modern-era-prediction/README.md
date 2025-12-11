# 🏎️ Formula 1 Modern-Era Race Strategy & Prediction System (2016–2025)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn)
![SHAP](https://img.shields.io/badge/SHAP-Explainable_AI-ff00ff?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

## 📖 Executive Summary

This project establishes a **production-ready machine learning pipeline** to analyze and predict Formula 1 race outcomes in the "Modern Era" (2016–Present).

Unlike generic sports models, this system recognizes that F1 is an engineering competition as much as a driver competition. It implements a **Dual-Objective Modeling approach**:
1.  **Win Prediction (`is_win`):** Identifying the singular winner (High variance, Driver/Grid focused).
2.  **Points Prediction (`is_top10`):** Identifying reliable point-scorers (Stability focused, crucial for Constructor Standings).

The system is rigorously validated on the **2024 Season** (unseen data) to ensure real-world applicability.

---

## 🚀 Key Technical Features

### 1. Domain-Specific Data Engineering ("The Modern Era")
F1 data from the 1950s is irrelevant to modern racing due to technological shifts.
* **Filtering:** Restricted analysis to the **Hybrid Era (2016–Present)** to ensure feature consistency.
* **Relational Merging:** Unified fragmented Ergast API tables (Results, Drivers, Constructors, Races) into a single analytical view.

### 2. Advanced Feature Engineering
* **Team Strength Index:** Quantified the "Car Performance" factor separate from driver skill, acknowledging that ~80% of performance comes from the machine.
* **Rolling Form Metrics:** Implemented time-series rolling windows (Last 3/5 Races) to capture driver momentum and recent upgrades.
* **Leakage Prevention:** Strictly sorted data by `Season` and `Round` before feature generation to prevent future information leakage.

### 3. Dual-Layer Modeling & Explainability (SHAP)
* **Model:** Random Forest & Logistic Regression classifiers.
* **Interpretability:** Used **SHAP (SHapley Additive exPlanations)** to deconstruct predictions.
    * *Insight:* "Grid Position" dominates Win probability, while "Team Reliability" and "Consistency" become significantly more important for Top-10 probabilities.

---

## 📂 Project Pipeline (File Structure)

This project follows a strict **ETL → Feature Engineering → Modeling** workflow.

| Seq | Notebook Name | Role | Key Function |
| :--- | :--- | :--- | :--- |
| **01** | `01_F1_Data_Prep_and_EDA.ipynb` | **ETL & Data QC** | Ingests raw data, filters for the Modern Era (2016+), and performs EDA to understand grid-to-finish correlations. |
| **02** | `02_F1_Season_Feature_Engineering.ipynb` | **Feature Eng.** | Constructs **Rolling Form**, **Cumulative Season Stats**, and **Team Strength** metrics. Handles time-series sorting. |
| **03** | `03_F1_Win_Modeling_Modern_Era.ipynb` | **Modeling & SHAP** | Trains Dual Models (Win / Top-10). Validates on the **2024 Season**. Visualizes feature importance using SHAP Beeswarm plots. |

---

## 📊 Model Performance & Insights

### Validation Strategy
* **Training Set:** Seasons 2016 – 2023
* **Validation Set:** Season **2024** (Latest complete season)
* *Note: This split mimics a real-world scenario where we predict the upcoming season based on historical patterns.*

### Key Findings (SHAP Analysis)

| Feature | Impact on **Win** Probability | Impact on **Top-10** Probability |
| :--- | :--- | :--- |
| **Grid Position** | 🔴 **Critical** (Almost impossible to win from P4+) | 🟠 **High** (But recovery is possible) |
| **Recent Form** | 🟠 **High** (Momentum matters for championships) | 🟡 **Medium** (Consistency matters more) |
| **Team Strength** | 🟡 **Medium** (Need a top car to win) | 🟢 **Very High** (Reliable cars guarantee points) |

> **Business Insight:** To win a Championship, invest in **Qualifying speed** (Grid Position). To secure Constructor points (money), invest in **Reliability** (Team Strength).

---

## ⚠️ Limitations & Disclaimer

1.  **Regulation Changes:** This model is optimized for the current Hybrid Era regulations. The major regulation overhaul in **2026** may require retraining or feature re-weighting.
2.  **In-Race Strategy:** This is a **Pre-Race** prediction model. It does not account for real-time in-race variables such as Safety Cars, Pit Stop errors, or weather changes during the race.
3.  **Tyre Compound:** Tyre strategy choices (Soft/Medium/Hard) are not included in the pre-race features.

---

### 👤 Author

**Minseob Eom**
*Sports Data Analyst & System Architect*
*(Please insert your email or LinkedIn profile link here)*

Email: wowzc@naver.com
GitHub: https://github.com/madferit94
