# Rank proxy ablation SPEC

Run: rank-ablation-2026-10-06-v01. Producer: /root/rank_ablation. Agent role: analyst.

Required: distinguish official positions from derived raw standings; only preceding completed seasons; explicit unknown ranks; same rows, original model family and fixed regularization; preserve v2 and viewer; report accuracy, log loss, multiclass Brier sum and ECE; do not turn larger probabilities into a quality claim.

Actual: four columns appended: normalized prior raw rank for each team (1→0, 20→1), then each team's missing flag. Missing rank=0.5, flag=1. League table requires 380 unique games, 20 teams, 38 games each. Order is raw points, goal difference, goals scored, then team key if exactly tied. No deductions or official tiebreakers applied. Previous table's latest source date must be strictly before each target date. Incomplete 2026/27 tables excluded. Transfermarkt values absent.

Training: original 2023/24 initial train; 2024/25 initial validation; original regularization 0.1 fixed; final refit on 2023/24+2024/25. Original evaluation-model probabilities reproduced within 1e-12. Initial additional coefficients exactly zero, because 2022/23 missing causes constant inputs. Rank observations exist in only one final-training season; both teams known in 544 of its 760 matches.

Evaluation: 2025/26 760 games and 2026/27 119 games reused after hypothesis. Retrospective exploratory ablation; not a fresh untouched test. Existing model remains experimental. No adoption or UI change. Formula implementation and all exact metrics in experiment.py and analyst-report.json.

Observed: 2025/26 accuracy 50.92%→49.87%, log loss 1.011080→1.011412, Brier 0.606261→0.606555, ECE 0.039827→0.026639. Monitoring accuracy 42.86%→43.70%, log loss 1.031313→1.030708, Brier 0.617871→0.617131, ECE 0.112095→0.128125. Evidence does not establish a general improvement.

Self-check evidence: check-result.json. Independent reviewer and director handle approval outside this owned folder. Participant screen confirmation is not applicable to this non-UI experiment; no user confirmation claimed.
