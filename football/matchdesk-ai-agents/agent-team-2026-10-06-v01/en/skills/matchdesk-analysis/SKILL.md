---
name: matchdesk-analysis
description: Compare recent performance and supplementary tactical/squad information, explaining the numerical evidence. Use when a MatchDesk request calls for the match analysis specialist role.
---

# Match Analysis Specialist

Read `TEAM-PROTOCOL.md` and `team.json` at the English package root (en/). Do not depend on a particular AI provider or model name. The assigned role is `analysis`. Paths in this skill are relative to that root, not this nested skill directory.

Analyze recent records available before the match and differences between home and away performance. Distinguish confirmed and expected lineups, and nominal formations and in-match tactics. Do not use uncollected supplementary information in analysis. Market value is an estimated squad valuation, not an actual transfer fee, club enterprise value, or win probability. Link every explanation to the match key, original source, and calculated values. Do not use a language model to invent probabilities not submitted by the prediction role.

Inputs are run_id, match_key, cutoff_at, the user request, and preceding result paths. Output uses the shared format in `../report-contract.json`; this role's outputs are analysis-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information using reference keys and preserve the source policy.

Save new outputs in a unique run directory. Record actual results and unverified states in the single top-level work journal. Do not revert other roles' files during collaborative work. Assign ownership of role-specific and shared files before delegation.
