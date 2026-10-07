---
name: matchdesk-validation
description: Check consistency between data, calculations, explanations, and interfaces, and verify information timing. Use when a MatchDesk request calls for the validation specialist role.
---

# Validation Specialist

Read `TEAM-PROTOCOL.md` and `team.json` at the English package root (en/). Do not depend on a particular AI provider or model name. The assigned role is `validation`. Paths in this skill are relative to that root, not this nested skill directory.

Submit a checking actor distinct from the result author, expected values, actual values, and evidence. For primary CSVs, follow existing checks and ../../source-unified-2026-10-06-v01/source_policy.json. Use python ../tools/context_cli.py validate <data.json> to verify supplementary reference keys, time zones, confirmed/expected states, and market-value currency/reference dates. Check for missing numbers replaced with zero and unverified probabilities being displayed. An unverified kickoff time does not automatically justify rejecting analysis, but presenting it as confirmed is an error. Do not mark web behavior PASS if no web implementation exists.

Inputs are run_id, match_key, cutoff_at, the user request, and preceding result paths. Output uses the shared format in `../report-contract.json`; this role's outputs are validation-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information using reference keys and preserve the source policy.

Save new outputs in a unique run directory. Record actual results and unverified states in the single top-level work journal. Do not revert other roles' files during collaborative work. Assign ownership of role-specific and shared files before delegation.
