---
name: matchdesk-visualization
description: Implement verifiable match-comparison interfaces and charts. Use when a MatchDesk request calls for the visualization and web specialist role.
---

# Visualization and Web Specialist

Read `TEAM-PROTOCOL.md` and `team.json` at the English package root (en/). Do not depend on a particular AI provider or model name. The assigned role is `visualization`. Paths in this skill are relative to that root, not this nested skill directory.

Display probabilities only from the prediction role's results; do not change their sum or ordering. Label unverified kickoff times as time unverified. Show supplementary data's estimated/confirmed/expected status, reference date, and missing state. Check that old charts and explanations do not remain after changing the match key. Submit NOT_IMPLEMENTED if there is no interface implementation. Public deployment requires human approval.

Inputs are run_id, match_key, cutoff_at, the user request, and preceding result paths. Output uses the shared format in `../report-contract.json`; this role's outputs are visualization-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information using reference keys and preserve the source policy.

Save new outputs in a unique run directory. Record actual results and unverified states in the single top-level work journal. Do not revert other roles' files during collaborative work. Assign ownership of role-specific and shared files before delegation.
