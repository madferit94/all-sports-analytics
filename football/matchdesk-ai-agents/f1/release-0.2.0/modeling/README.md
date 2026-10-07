# MatchLab F1 historical-result model · 0.2.0

Actual training: 24 OpenF1 2025 race records plus 16 completed 2026 races. The first five races provide warm-up history; incomplete target results exclude the entire race from model fitting. Train races: 29; chronological holdout: 6. Held-out session keys: [11342, 11353, 11361, 11369, 11377, 11731]. Incomplete-result exclusions: [].

## Indicators
- Last-five finishing score
- Last-five mean points
- Last-five win rate
- Last-five podium rate
- Last-five DNF/DNS/DSQ rate
- Season-to-date finishing score
- Team last-five GP finishing score
- Team last-five GP win rate per entrant
- Earlier same-circuit finishing score
- Earlier same-circuit win rate

Ranking score is (field size − finish position)/(field size − 1), so higher means stronger earlier finish. Means and rates have two fixed neutral pseudo-observations. No earlier history: neutral prior; absent same-circuit records: neutral circuit prior. Team histories are matched by recorded team name; no assumed corporate/team alias continuity. Driver identities use normalized full names, never permanent car numbers. Circuit history uses the actual circuit_key, not the GP marketing title. Only completed source races whose end precedes target start are allowed. History support counts are disclosed separately, not input features.

## Model and untouched time test
Standardized binary logistic regression supplies driver scores, normalized with softmax within each GP to one winner distribution. Ridge regression estimates finish percentile and maps it to the expected field rank. C=1, ridge alpha=10 fixed before evaluation; no holdout tuning. All six holdout predictions use a frozen trained model, with earlier holdout results becoming history only after completion, reproducing sequential deployment. Target timing, target laps, target standings, grid and future weather are absent. Missing finish positions are excluded from ranking labels. Historical driver metadata defines retrospective participants; its publication timestamp is not independently verified, so this is a result-history model evaluation, not proof of a fully archived live pre-race information set.

| Model | Log loss ↓ | Brier ↓ | Top-1 |
|---|---:|---:|---:|
| model | 3.1195 | 0.8646 | 33.3% |
| recent_win_baseline | 2.9699 | 0.9713 | 11.7% |
| uniform | 3.0910 | 0.9545 | 4.5% |


Expected-rank MAE: 2.530 places. Top-1 means winner chosen correctly, never accuracy across all losing drivers. Tied maximum probabilities share winner credit equally rather than using the arbitrary first driver. Small six-race test cannot establish stable performance. Brier here is the sum across entrants, without dividing by field size. The model's log loss is worse than both baselines; although Brier and top-1 improve, this does not justify claiming superior probabilistic forecasting. Treat this release as an experimental result-history model.

## Future races
Seven scheduled races receive a final model refit after holdout reporting. All predictions share the observed snapshot; later future races do not consume invented results from earlier future races. Latest completed GP supplies the 22-driver assumed list, not a confirmed future entry list. Expected rank is a continuous estimate and not a permutation of finishing positions. Probability normalization does not demonstrate calibration. The 2026 regulation change, limited sample, missing grid/weather and roster changes limit applicability. Cancelled GP has no prediction. No live API/model service is necessary for these cached predictions.

Source: [OpenF1 documentation](https://openf1.org/docs/). Reproduce with collect-history.py, then train.py and check-model.py in Python 3.12 using requirements.txt. The collection preserves cache files and uses 4.7-second spacing and 429 backoff; source hashes are in source-manifest.json. modelmetrics.json captures input hashes. producer-check.json is self-check evidence; final approval belongs to the independent reviewer/director.
