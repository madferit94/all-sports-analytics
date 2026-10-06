# First pre-match prediction baseline — local development

[English](README.md) | [한국어](README.ko.md)

This is a new **unreleased experiment after pulling 0.2.1**. It does not change the archived ten-role run or mean the five-agent workflow has been fully executed. Source and tests are currently local changes; generated runs are ignored by Git. No prediction service is deployed.

## Method

A three-class logistic model learns home-win/draw/away-win probabilities from the previous five recorded league matches per team. Features include points, goals, xG, available history counts and calendar gaps between league matches. Calendar gap is not actual rest. No-history values are fixed neutral priors with an explicit zero history count; they are not collected facts. Neither current season totals nor auxiliary squad/news/value snapshots are used.

All inputs for one calendar date are generated before any result from that date is added to history. This conservative rule avoids treating an unverified kickoff time as established. All historical inputs use earlier-date evidence; the current match outcome is a label. Future target outcomes are ignored.

The initial fit uses2023/24, regularization is selected on2024/25, and the2025/26 test uses a model refit on the first two seasons.2026/27 is a separate follow-up evaluation. The final exploratory model refits all completed matches for the two future targets. Preprocessing statistics use the corresponding training partition only. Class order is home, draw, away.

## Execute

Python3.12.14 and NumPy2.3.5 were used. The pinned NumPy version requires Python3.11+. From the MatchDesk project directory:

```sh
python -m unittest discover -s modeling/tests -v
python modeling/train_baseline.py --dataset /path/to/full/source-unified-2026-10-06-v01 --cutoff-date 2026-10-06 --out modeling/runs/new-unique-run
```

The dataset must be the full local historical package, not the public20-fixture demonstration subset. Choose a new output directory every time; existing results are never overwritten. If NumPy is unavailable, `modeling/requirements.txt` records the version; no package was installed during this run.

## Executed development result

The run `2026-10-06-v01` contains2,399 completed fixtures and two forecast targets.2025/26 held-out test:760 fixtures; accuracy49.21% versus45.79% for smoothed training-league outcome frequencies. Log loss1.0280 versus1.0680; lower means less probability error. **The2026/27 follow-up119-fixture cohort is worse: accuracy39.50% versus41.18% and top-confidence calibration error15.16% versus3.48%. This model has not established generalization or calibrated probabilities and remains unadopted.** The multiclass Brier score sums all three squared errors. The calibration diagnostic is top-class confidence ECE over ten equal-width bins; it is not an independently adopted calibration method or calibration guarantee.

Five temporal/parser/numerical tests pass. A first execution encountered integral decimal goal strings such as `0.0`; the parser was corrected to accept integral decimals while rejecting fractional/negative/nonfinite goals. Original input files were unchanged. Independent review is recorded separately in `review-2026-10-06-v01` when available.

## Limits

Data was not refreshed and the last completed source date is2026-09-20. The generated probabilities are **experimental stored-snapshot outputs, not an adopted live prediction**. User model-adoption criteria are not set. Player availability, formation, squad value, opponent-strength adjustments and probability calibration are future work. Small league-specific follow-up cohorts and new/promoted-team cold starts require caution. These numbers are performance of this saved evaluation, not a promised success rate.

Evidence: [pre-execution specification](SPEC.md), generated `metrics.json`, `model.json`, `historical_features.json`, `future_inputs.json`, `predictions.csv`, and `input_manifest.json` under the local ignored run folder.
