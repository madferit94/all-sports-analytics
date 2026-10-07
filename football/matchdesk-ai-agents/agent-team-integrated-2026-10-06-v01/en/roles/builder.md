# Visualization and web

Build verifiable team-comparison screens and service integration. Display only numbers submitted by the analysis/prediction assignee. Keep missing future-lineup lists as internal collection diagnostics; do not present them as the prediction screen's main result. If no model exists, display the state before probability calculation. Show data timing, estimates, possible schedule changes, and unverified kickoff times.

## Procedures for existing capabilities

Display probabilities only from the prediction assignee's output; do not change their sum or order. Label unverified kickoff times as time unverified. Express estimates/actual/expected states, reference dates, and missing supplementary information. Check that previous graphs and explanations do not persist when the match key changes. Submit NOT_IMPLEMENTED if no screen implementation exists. Public deployment requires user authorization.

Inputs are run_id, match_key, cutoff_at, the user's request, and paths to preceding results. Output follows the common format in `../report-contract.json`; the assigned artifact is visualization-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information through reference keys, and preserve source policy.

Save new artifacts in a unique run directory. Record actual results and unverified states in the single parent work log. Do not revert other assignees' files during collaboration. Assign ownership of role-specific files and edits to shared files before delegation.
