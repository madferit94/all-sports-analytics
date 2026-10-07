# Analysis and prediction

Handle both recent-performance comparisons and prediction-model development/execution. Future matches are prediction targets, and training labels are historical match results. Historical training inputs contain only information knowable before that match started. Unpublished actual future lineups are not a prerequisite that blocks basic model prediction. If inputs required by the chosen model are missing, record the rationale for handling their absence. Do not give final approval to your own model's performance.

## Procedures for existing capabilities

Analyze recent pre-match records and home/away differences. Distinguish actual from expected lineups, and nominal formations from in-match tactics. Do not use uncollected supplementary data in analysis. Market value is an estimated squad value; it is not actual transfer fees, a club's enterprise value, or win probability. Connect every explanation to match keys, original sources, and calculated values. Do not use a language model to invent probabilities that the prediction assignee has not submitted.

Inputs are run_id, match_key, cutoff_at, the user's request, and paths to preceding results. Output follows the common format in `../report-contract.json`; the assigned artifact is analysis-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information through reference keys, and preserve source policy.

Save new artifacts in a unique run directory. Record actual results and unverified states in the single parent work log. Do not revert other assignees' files during collaboration. Assign ownership of role-specific files and edits to shared files before delegation.

If actual prediction code does not exist, submit NOT_IMPLEMENTED and do not generate probabilities. Save the model version, input matches, prediction cutoff, and feature list. Do not use end-of-season/current StatMuse totals as historical match features. Do not use the forecast in the original Understat source as pre-match prediction probabilities. Do not use injuries, market value, or formations to arbitrarily adjust probabilities before their integration rules and historical-time data have been evaluated.

Inputs are run_id, match_key, cutoff_at, the user's request, and paths to preceding results. Output follows the common format in `../report-contract.json`; the assigned artifact is prediction-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information through reference keys, and preserve source policy.

Save new artifacts in a unique run directory. Record actual results and unverified states in the single parent work log. Do not revert other assignees' files during collaboration. Assign ownership of role-specific files and edits to shared files before delegation.
