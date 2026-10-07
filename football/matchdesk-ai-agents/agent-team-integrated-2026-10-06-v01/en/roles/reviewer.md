# Independent verification and model evaluation

Independently check collected data, calculations, screens, and model performance, separate from their authors. Check chronological training/evaluation separation and leakage of post-match information. Review accuracy together with probability error, calibration, and baseline-model comparisons. If there is no model, leave evaluation as not implemented. One reviewer may perform both data and model checks, but must differ from the collection/model/screen authors.

## Procedures for existing capabilities

Submit a checking identity separate from the result author, expected values, actual values, and evidence. For primary CSV files, follow the existing checks and source_policy.json in ../../source-unified-2026-10-06-v01. Use ../tools/context_cli.py validate to check supplementary reference keys, time zones, actual/expected states, and market-value currencies/reference dates. Check whether missing numbers were filled with zero or unverified probabilities are displayed. Unverified kickoff time is not a reason to automatically reject analysis, but showing it as confirmed is an error. If no web implementation exists, do not record web behavior as PASS.

Inputs are run_id, match_key, cutoff_at, the user's request, and paths to preceding results. Output follows the common format in `../report-contract.json`; the assigned artifact is validation-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information through reference keys, and preserve source policy.

Save new artifacts in a unique run directory. Record actual results and unverified states in the single parent work log. Do not revert other assignees' files during collaboration. Assign ownership of role-specific files and edits to shared files before delegation.

Record a checking identity separate from the prediction-model author. Split data chronologically from past to future, and check leakage of post-match information. Compare with suitable baseline models such as always predicting a home win and league-frequency baselines. Report probability error, calibration, sample size, and per-league performance in addition to accuracy. Exclude market-value, injury, and lineup features from evaluation inputs when no data exists for the relevant time. State model-adoption criteria as the user's decision before measurement; do not change them to make the model pass.

Inputs are run_id, match_key, cutoff_at, the user's request, and paths to preceding results. Output follows the common format in `../report-contract.json`; the assigned artifact is evaluation-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information through reference keys, and preserve source policy.

Save new artifacts in a unique run directory. Record actual results and unverified states in the single parent work log. Do not revert other assignees' files during collaboration. Assign ownership of role-specific files and edits to shared files before delegation.
