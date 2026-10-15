## 🏈 NFL — Match Outcome Analytics & Simulation System

[English](README.md) | [한국어](README.ko.md)

**Dynamic team momentum modeling using Rolling EPA and clustering.**

> An end-to-end NFL analytics system that models  
> *how strong a team is right now*, not just season-level averages.

---

### 🔍 What this system does
- Tracks **team momentum week-by-week** using rolling EPA (last 4 games)
- Applies **static + dynamic clustering** to capture evolving team styles
- Generates **pre-game game-level signals** under strict leakage prevention
- Visualizes insights through a **live interactive dashboard**

---

### 📊 Live Interactive Dashboard
👉 [Try Live Dashboard*](https://all-sports-analytics-guvyfdgx7gz6qsb5yqhrvq.streamlit.app)

👉 [View Source Code](https://github.com/madferit94/all-sports-analytics/tree/main/nfl-epa-analysis)

---

### 🌐 Live Dashboards
This repository also hosts other deployed analytics systems:

- 🏈 [NFL EPA & Win Probability Dashboard](https://all-sports-analytics-guvyfdgx7gz6qsb5yqhrvq.streamlit.app)

- 🏎️ [F1 Modern-Era Analytics Dashboard](https://f1-modern-era-eda.streamlit.app)

---

### 🧠 Core Technical Highlights
- **Leakage-Proof Design**  
  All features are computed strictly from information available *before kickoff*  
  (rolling windows, shifted targets).
- **Dynamic Team Representation**  
  Teams are treated as *time-varying entities*, not static season summaries.
- **Explainable Modeling**  
  Feature contributions are validated via SHAP-based analysis.
- **Simulation-Ready Outputs**  
  Model outputs are structured for downstream season simulation pipelines.

---

### 🛠 Tech Stack
`Python` · `Pandas` · `Scikit-learn` · `XGBoost` · `SHAP` · `Plotly` · `Streamlit`

---

## 📁 Project Structure

```text
nfl-epa-analysis/
├── notebooks/
│   ├── 01_Data_Prep.ipynb        # ETL & data quality checks
│   ├── 02_Clustering.ipynb       # Static team style clustering
│   ├── 03_Feature_Eng.ipynb      # Rolling EPA & dynamic features
│   ├── 04_Modeling.ipynb         # Win probability model + SHAP
│   └── 05_Simulation.ipynb       # Season-level Monte Carlo simulation
│
├── data/
│   └── processed/                # Pre-game, leakage-safe datasets
│
├── streamlit_app/
│   ├── app.py                    # Deployed Streamlit dashboard
│   └── requirements.txt          # Dashboard dependencies
│
└── README.md                     # Project documentation
