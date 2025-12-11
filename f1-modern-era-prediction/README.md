🏎️ F1 Modern-Era Race Prediction (2016–Latest)

Machine learning models predicting race win probability and Top-10 finish probability using modern-era Formula 1 data.

⸻

🔍 Overview

This project builds two classification models:

1) Win Probability (is_win)
	•	Predicts the probability a driver wins a Grand Prix
	•	Evaluated using: ROC-AUC, Brier Score, classification report
	•	Race-level metric: Top-1 winner accuracy
“Does the driver with the highest predicted probability actually win?”

2) Top-10 Probability (is_top10)
	•	Predicts whether a driver finishes inside the Top-10
	•	Evaluated using: Precision@10, Recall@10

Both tasks use a time-based split:
Train on seasons 2016 → (latest−1), validate on the latest season only.

01_F1_Data_Prep_and_EDA.ipynb
02_F1_Season_Feature_Engineering.ipynb
03_F1_Win_Modeling_Modern_Era.ipynb

Workflow:
	1.	Data cleaning & merging (drivers, constructors, race results)
	2.	Rolling driver & team feature engineering
	3.	Season-aware train/validation split
	4.	Models: Logistic Regression, Random Forest (+ XGBoost / LightGBM if installed)
	5.	SHAP interpretation for feature importance

📊 Model Results (Summary)

Win Model (Random Forest)
	•	ROC-AUC: ~0.89
	•	Good probability calibration (low Brier)
	•	Winner prediction remains difficult due to extreme imbalance (~7%)
	•	Best used for ranking winning potential, not exact winner classification

Top-10 Model (Random Forest)
	•	ROC-AUC: ~0.89
	•	Precision@10 ≈ 0.62
	•	Recall@10 ≈ 0.99
	•	Captures nearly every actual Top-10 finisher

⸻

🧠 SHAP Insights
	•	Grid position is the strongest predictor for both tasks
	•	Team rolling strength & driver recent form add consistent value
	•	Reliability features (DNF rate) matter especially for Top-10 predictions

⸻

🚀 Applications
	•	Race simulations & probability forecasts
	•	Podium/Top-5/Top-10 modeling
	•	Driver comparison & season-long form tracking
	•	ML interpretability studies (SHAP)

⸻

📌 Notes
	•	Designed to extend automatically when new F1 seasons are added
	•	All modeling is leakage-free using time-based validation
	•	Fully reproducible as a portable research or portfolio project
