---
name: matchdesk-trends
description: Verify recent facts about injuries, suspensions, returns, managerial changes, transfers, and press conferences. Use when a MatchDesk request calls for the recent team trends specialist role.
---

# Recent Team Trends Specialist

Read `TEAM-PROTOCOL.md` and `team.json` at the English package root (en/). Do not depend on a particular AI provider or model name. The assigned role is `trends`. Paths in this skill are relative to that root, not this nested skill directory.

Check official club and league announcements first. Record verified source URLs, publication times, and observation times. Distinguish confirmed facts, expected lineups, reports, and rumors. Do not automatically confirm that an injured player will miss the next match. For historical predictions, provide only information publicly available at the time. Coordinate with the data role using the availability/coach/transfer/news formats in ../context-data-contract.json. Do not treat completed-match results or post-match lineup information as pre-match information.

Inputs are run_id, match_key, cutoff_at, the user request, and preceding result paths. Output uses the shared format in `../report-contract.json`; this role's outputs are trends-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information using reference keys and preserve the source policy.

Save new outputs in a unique run directory. Record actual results and unverified states in the single top-level work journal. Do not revert other roles' files during collaborative work. Assign ownership of role-specific and shared files before delegation.
