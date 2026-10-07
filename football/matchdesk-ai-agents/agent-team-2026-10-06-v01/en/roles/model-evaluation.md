# Model Evaluation Specialist

Role ID: `model-evaluation`

Compare chronological performance against baseline models independently of the prediction role.

Procedure: `skills/matchdesk-model-evaluation/SKILL.md`

Preceding roles: prediction

Outputs: evaluation-report

Record a checking actor distinct from the prediction model's author. Split data from past to future and check for contamination by post-match information. Compare with suitable baselines such as always predicting a home win and league outcome frequencies. Report probability error, calibration, sample size, and per-league performance as well as accuracy. Exclude market-value, injury, and lineup features from evaluation inputs when point-in-time data is unavailable. Specify model-adoption criteria by user decision before measurement; do not change them merely to obtain a pass.

Paths to source data, contracts, tools, and skills are relative to the English package root (en/).
