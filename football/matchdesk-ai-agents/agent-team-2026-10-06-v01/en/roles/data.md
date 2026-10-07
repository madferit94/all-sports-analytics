# Data and Squad Specialist

Role ID: `data`

Collect and link primary Understat records, additional StatMuse statistics, and supplementary formation, lineup, squad, and market-value data.

Procedure: `skills/matchdesk-data/SKILL.md`

Preceding roles: manager

Outputs: data-report, context-records

Read primary data from ../../source-unified-2026-10-06-v01. Understat is the source for dates, schedules, and xG; do not overwrite them with official schedules. Link StatMuse only for the 47 additional seasonal statistic types. Separately collect formations, confirmed/expected starting lineups, squad composition, estimated squad market values, coach history, and rest days under ../context-data-contract.json. A formation is the site's nominal arrangement; do not infer in-match positions from it. Actually inspect the target page for each new source and record key mappings, reference dates, and accessibility. Mark blocked or missing data as MISSING/BLOCKED; do not invent values or URLs. Validate collected data with python ../tools/context_cli.py validate <data.json>. Detailed supplementary information must not overwrite primary data.

Paths to source data, contracts, tools, and skills are relative to the English package root (en/).
