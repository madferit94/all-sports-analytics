# Existing F1 work: keep or remove?

[한국어](existing_f1_review.ko.md)

**2026-10-05 preservation update:** The prediction prototype is now stored separately in a private repository and excluded from the current public tree. Original file contents are unchanged. Earlier public commits remain accessible.

Reviewed on 3 October 2026 against repository base commit `8d5a583e655b24d83f3f8666afbc5f753aed7c42`. This is a code/data review; historical models were not retrained and the live Streamlit deployment was not tested.

**Recommendation: preserve both historical projects. Correct the EDA and rebuild the prediction baseline before using its performance claims as portfolio evidence.** The Baku project answers an in-race question and does not replace a historical pre-race project.

| Existing work | Decision | Reason and required correction |
|---|---|---|
| `f1-modern-era-eda` | Keep, revise | A usable dashboard foundation. Its CSV covers 1950–2025; the app does not enforce a 2016 start and defaults to 2000. “Races” currently counts distinct GP names, not season/race instances. Correct the scope and count races by season + round. |
| Historical pre-race prediction | Preserve privately; excluded from the current public tree | Original notebooks, data, and model artifacts are preserved in a separate private repository. Corrections and revalidation remain pending. Earlier public commits still contain the original folder. |
| Saved model binaries | Preserve for historical reference | No need to delete now. They should not power a public forecast until features/labels are corrected. Retraining should create clearly versioned artifacts. |
| Duplicate cleaned CSV | Keep for now; later consider a shared input | EDA and prediction CSVs are byte-identical. Consolidation can reduce maintenance, but requires updating every dependent path and testing. |
| Baku exploratory outputs | Keep with status labels | Useful for showing the workflow. They are not the final pace analysis because temporal eligibility remains pending. |

## Confirmed defects

1. **Same-race teammate leakage.** In feature-engineering notebook cell index 12 (zero-based), `add_team_features` groups driver rows by season/team and shifts by one **row**. A teammate's current-race result can therefore enter the next driver's pre-race feature. In the committed feature CSV, 2016 round 1 Haas driver GRO has 8 points; GUT already has `team_points_before=8` and `team_points_last_3=8` in that same first race. Aggregate to one team–race row first, shift by race, and merge that prior state back to both drivers.
2. **DNF definition rejects lapped finishers.** Data-preparation notebook cell index 9 sets DNF if the status does not contain `Finished`, then blanks finish position. The clean CSV contains **7,572** rows with statuses matching `+N Lap(s)` and `is_dnf=True`; **1,260** are from 2016 onward. Such status labels describe lapped completion, not necessarily retirement. Rebuild classification/reliability labels from the source's definitions and preserve original finish fields.
3. **Post-outcome sample selection.** The win-modeling notebook filters on nonmissing finish position and positive grid. The committed 2024 feature table has **479** rows; this filter keeps **284**. A pre-race model needs an entrant cohort independent of the eventual result and an explicit treatment of pit-lane starts. The later Top-10 block reuses the filtered `train_df`/`valid_df` and additionally drops missing features, so its evaluation cohort differs from the earlier full-field block.
4. **Portability.** The first notebook includes a fixed `/Users/.../Desktop/F1_analysis` path. The initial bare `pip install kagglehub` code cell is not valid Python in an ordinary kernel. Use a project-relative root, a pinned/raw source snapshot, and a separate environment setup or `%pip` cell.
5. **Claims exceed evidence.** “Production-ready,” leakage prevention, a quantified car contribution, and causal strategy advice are not justified by this implementation. Time-based validation is a useful start, but leakage, target construction, cohort coverage, race-wise winner evaluation, and calibration must be addressed first. SHAP describes the model's associations, not engineering causality.

Notebook outputs were inspected as saved historical outputs; their performance numbers were not regenerated. The original notebooks, data, model binaries, and dashboard code are unchanged by this update. README descriptions now distinguish the prototype's status from the Baku exploratory workflow.

## What could be retired later?

After a corrected version reproduces and supersedes the old baseline, move obsolete generated binaries and redundant CSVs to a documented legacy location or stop tracking reproducible artifacts. Do not delete raw inputs or notebooks simply because the new project looks more polished. Keep the current historical version until the replacement has passed validation.
