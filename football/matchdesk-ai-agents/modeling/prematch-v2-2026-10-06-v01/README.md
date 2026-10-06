# Pre-match model v2: experimental, not adopted

The analyst producer `/root/prediction_v2` applied the project `matchdesk-analyst` skill and role protocol. This folder preserves the previous baseline and creates a separate model experiment. Independent review and human acceptance remain separate from author checks.

The model uses 2,399 collected PL/LaLiga matches through **2026-09-20** and forecasts the 641 stored scheduled fixtures from the **2026-10-06** cutoff snapshot. No dataset refresh occurred. Source fixture dates do not imply verified official kickoff times.

Inputs include attack (goals, xG, non-penalty xG, deep), defense (goals conceded, xG conceded, non-penalty xG conceded, deep allowed), pressing proxies (PPDA and opponent PPDA), points and sample counts. PPDA is not passing accuracy. Current-season/final StatMuse passing snapshots are excluded because their pre-match historical values are unavailable. Missing data is not assigned fake zero values.

All history dates must be strictly earlier than the target date. Same-day inputs are computed before any same-day results become available. Prior-season means shrink toward the expanding league mean with eight pseudo-matches; current-season means shrink toward that prior with eight pseudo-matches; the current-season last five matches shrink toward that season mean with three pseudo-matches. Unknown-history teams use a league prior. Missing previous-season history is not proof of promotion, and no lower-division records are invented. Initial neutral assumptions are listed in `input-manifest.json`.

2023/24 trains the model, 2024/25 selects regularization (0.1), and a frozen model trained on those two seasons evaluates 2025/26 and monitors 2026/27. Test outcomes do not select hyperparameters or update evaluation weights. Previously played matches can become history inputs for later evaluation matches. The separate future model is fitted on all observed records after evaluation.

| Evaluation | Matches | Accuracy | Frequency baseline | Log loss | Baseline log loss |
|---|---:|---:|---:|---:|---:|
|2025/26 held-out|760|50.92%|45.79%|1.0111|1.0680|
|2026/27 monitoring|119|42.86%|41.18%|1.0313|1.0897|

Lower log loss is better. Current LaLiga accuracy (43.48%) is below its frequency baseline (44.93%). Overall monitoring calibration error is about 0.112, versus 0.040 on the held-out season. Performance improvement is not universal; this is not automatic deployment approval or a claim of superiority over v1.

`train.py` exposes feature generation and fitting; `check.py` runs 11 author checks, including strict chronology, target-result invariance, order invariance, missing PPDA denominator handling and prediction reproduction. `model.json` contains future weights; `evaluation-model.json` contains frozen evaluation weights. `metrics.json` contains full scores; `historical-features.json` contains per-match evidence. `future-predictions.json` contains home/draw/away probabilities for every fixture and status `EXPERIMENTAL_NOT_ADOPTED`.

All future forecasts share the stored data snapshot, so later fixtures become stale without fresh records. The model predicts outcomes, not scorelines. Pixel playback and displayed illustrative scores are simulated presentation, not actual footage or predicted scorelines. See [the Korean specification](README.ko.md) for full assumptions and file details. Regeneration writes into a new version folder; existing generated artifacts are preserved.
