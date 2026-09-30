# How to read the outputs

- `outputs/v1/`: one row per team per fixture. Local only.
- `outputs/v2/`: team-period KPIs, cumulative standings, metric ranks, league means and medians.
- `outputs/v2/categories/`: 43 metric definitions, category changes, five-round profiles and an extended match table.
- `outputs/v3/`: club W/D/L accounting, period summaries and median-based match-review groups.
- `outputs/v4/`: distributions, individual omission trials, concentration, venue splits and PPG sensitivity.
- `results/`: selected aggregate reference tables for reading without the raw inputs.
- `figures/`: seven static English charts also embedded in the notebooks.

## Units

In the core KPI tables, `pass_completion_rate`, `shot_accuracy`, `attacking_area_pass_share` and `shot_share` are fractions from 0 to 1. Multiply a rate difference by 100 to express percentage points.

In the category tables, rows with `unit=percent` use a 0–100 scale; their `delta` is in percentage points. `relative_change_pct` is always a relative percentage change, not a percentage-point difference. Undefined relative changes remain missing when the baseline is zero.

`positions_gained = rank_r15 - rank_r30`, so positive values mean a rise in the cumulative table. A metric rank may only mean more or fewer recorded events; it is not automatically a better or worse tactical performance.

For v4, `loo_min` and `loo_max` are the smallest and largest changes after removing one observation from one period. There are 30 trials per team/metric: 15 before-period exclusions and 15 after-period exclusions. Each trial compares 14 with 15 matches. No baseline match is permanently dropped.

## Learning prompts

1. Trace one fixture through final-score rows, own statistics and opponent statistics.
2. Explain why league goals scored and goals conceded necessarily have equal totals.
3. Distinguish a club's post-break PPG from its cumulative R30 league position.
4. Compare mean and median changes without treating either as a causal explanation.
5. Explain what the Anyang R24 exclusion changes, and what it cannot establish.

The notebooks are runnable analysis companions. Future work is described in the README; no additional model or season-end result has been fitted yet.
