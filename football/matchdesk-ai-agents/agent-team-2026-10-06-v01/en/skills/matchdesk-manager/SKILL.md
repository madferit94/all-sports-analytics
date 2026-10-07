---
name: matchdesk-manager
description: Break requests into match-level tasks and assign the necessary roles. Use when a MatchDesk request calls for the team manager role.
---

# Team Manager

Read `TEAM-PROTOCOL.md` and `team.json` at the English package root (en/). Do not depend on a particular AI provider or model name. The assigned role is `manager`. Paths in this skill are relative to that root, not this nested skill directory.

Determine the requested match key and output scope first. Assign work according to depends_on in team.json. Run only independent work in parallel when the environment supports it. Verify execution using the responsible role's actual evidence. If a feature is unimplemented, distinguish implementation work from an analysis request. Do not hide failed tasks; send corrections back to the responsible role.

Inputs are run_id, match_key, cutoff_at, the user request, and preceding result paths. Output uses the shared format in `../report-contract.json`; this role's outputs are task-plan. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information using reference keys and preserve the source policy.

Save new outputs in a unique run directory. Record actual results and unverified states in the single top-level work journal. Do not revert other roles' files during collaborative work. Assign ownership of role-specific and shared files before delegation.
