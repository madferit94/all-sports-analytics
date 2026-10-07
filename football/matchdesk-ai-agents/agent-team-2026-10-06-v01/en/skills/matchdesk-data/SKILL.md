---
name: matchdesk-data
description: Collect and link primary Understat records, additional StatMuse statistics, and supplementary formation, lineup, squad, and market-value data. Use when a MatchDesk request calls for the data and squad specialist role.
---

# Data and Squad Specialist

Read `TEAM-PROTOCOL.md` and `team.json` at the English package root (en/). Do not depend on a particular AI provider or model name. The assigned role is `data`. Paths in this skill are relative to that root, not this nested skill directory.

Read primary data from ../../source-unified-2026-10-06-v01. Understat is the source for dates, schedules, and xG; do not overwrite them with official schedules. Link StatMuse only for the 47 additional seasonal statistic types. Separately collect formations, confirmed/expected starting lineups, squad composition, estimated squad market values, coach history, and rest days under ../context-data-contract.json. A formation is the site's nominal arrangement; do not infer in-match positions from it. Actually inspect the target page for each new source and record key mappings, reference dates, and accessibility. Mark blocked or missing data as MISSING/BLOCKED; do not invent values or URLs. Validate collected data with python ../tools/context_cli.py validate <data.json>. Detailed supplementary information must not overwrite primary data.

Inputs are run_id, match_key, cutoff_at, the user request, and preceding result paths. Output uses the shared format in `../report-contract.json`; this role's outputs are data-report, context-records. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information using reference keys and preserve the source policy.

Save new outputs in a unique run directory. Record actual results and unverified states in the single top-level work journal. Do not revert other roles' files during collaborative work. Assign ownership of role-specific and shared files before delegation.
