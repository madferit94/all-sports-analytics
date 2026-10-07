# Data and trends research

Collect and link primary match records and supplementary information, and check club news. Preserve team names, match keys, sources, retrieval dates, and valuation dates. Distinguish the timing difference between current squads and historical values, and confirmed facts from reporting/estimates. If cup and national-team records have not been checked, do not describe gaps between league matches as actual rest days.

## Procedures for existing capabilities

Read primary data from ../../source-unified-2026-10-06-v01. Understat is the source for dates, schedules, and xG; do not overwrite it with official schedules. Link StatMuse only for the 47 supplementary seasonal statistics. Separately collect formations, actual/expected lineups, squad composition, estimated squad market value, coach history, and rest days using ../context-data-contract.json. A formation is the site's nominal arrangement; do not infer it from in-match positions. For new sources, actually inspect the target page and record key mapping, reference date, and accessibility. Leave blocked or missing information as MISSING/BLOCKED; do not invent values or URLs. Check collected data with ../tools/context_cli.py validate. Detailed supplementary information must not overwrite primary data.

Inputs are run_id, match_key, cutoff_at, the user's request, and paths to preceding results. Output follows the common format in `../report-contract.json`; the assigned artifact is data-report, context-records. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information through reference keys, and preserve source policy.

Save new artifacts in a unique run directory. Record actual results and unverified states in the single parent work log. Do not revert other assignees' files during collaboration. Assign ownership of role-specific files and edits to shared files before delegation.

Check official club and league announcements first. Record verified source URLs, publication times, and observation times. Distinguish confirmed facts, expected lineups, and reports/rumors. Do not automatically confirm an injured player's absence from the next match. Supply only information publicly available at the time for historical predictions. Hand information to the data capability using the availability/coach/transfer/news formats in ../context-data-contract.json. Do not treat completed-match results or post-match lineup information as pre-match information.

Inputs are run_id, match_key, cutoff_at, the user's request, and paths to preceding results. Output follows the common format in `../report-contract.json`; the assigned artifact is trends-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information through reference keys, and preserve source policy.

Save new artifacts in a unique run directory. Record actual results and unverified states in the single parent work log. Do not revert other assignees' files during collaboration. Assign ownership of role-specific files and edits to shared files before delegation.
