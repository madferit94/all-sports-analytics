## 🏈 NFL — Match Outcome Analytics & Simulation System

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

- 🏎️ [F1 Modern-Era Analytics Dashboard]()

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

### 📁 Project Structure

nfl-epa-analysis/
├── notebooks/        # ETL → Feature Eng → Modeling → Simulation
├── data/processed/   # Rolling EPA & matchup-level datasets
├── streamlit_app/    # Live dashboard (deployed)
└── README.md         # Full technical documentation

