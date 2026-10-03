# Historical F1 Pre-race Prediction Prototype (2016–2025)

[English](README.md) · [한국어](README.ko.md)

This existing project uses historical result tables to build driver/team form features and explore win and Top-10 classification. It is a **pre-race experimental baseline**, not a verified production race-strategy system.

**Status: preserved for learning; leakage, labels, evaluation cohort, and portability need correction before performance claims are reused.** Historical notebook outputs were inspected, but models were not retrained in the current review.

## Existing workflow

| Stage | Notebook | Role |
|---|---|---|
| 01 | [Data preparation and EDA](notebooks/01_F1_Data_Prep_and_EDA.ipynb) | Join source tables, construct labels, inspect results. |
| 02 | [Feature engineering](notebooks/02_F1_Season_Feature_Engineering.ipynb) | Driver season totals/recent form and team features. |
| 03 | [Modeling](notebooks/03_F1_Win_Modeling_Modern_Era.ipynb) | Logistic regression, random forests, later Top-10 model comparisons, and SHAP. |

Saved features contain 4,300 rows across 2016–2025. The notebook's initial split trains on 2016–2023 and uses 2024 for validation. This time split does not by itself eliminate leakage or selection bias.

## Required corrections

- Team features shift driver rows rather than team–race rows, allowing same-race teammate results into pre-race inputs.
- DNF labels blank lapped finishers' positions. Rebuild source-faithful classification and reliability labels.
- Win/late Top-10 evaluation excludes entrants using post-race finish availability; define the pre-race cohort explicitly.
- Remove the fixed local data path and invalid bare install cell, then execute the notebooks in a clean environment.
- Re-evaluate with race-wise winner ranking, entrant coverage, a simple baseline, and probability calibration. SHAP is model interpretation, not causal evidence.

[Full code/data review and keep/remove decision](../f1/baku-2026/docs/existing_f1_review.md). The original code, data, and saved models remain unchanged. No performance figure is claimed as currently verified.

## Separate in-race analysis

The [Baku 2026 project](../f1/baku-2026) uses OpenF1 laps, race-control notices, stints, timing gaps, and locations to describe Russell–Verstappen race context. It supplies bilingual commented scripts and executed notebooks. Its final temporal pace eligibility is still pending; it does not replace or repair this historical prediction prototype.
