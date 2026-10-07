---
name: matchdesk-prediction
description: Generate home-win, draw, and away-win probabilities using verifiable calculation code and preserve the calculation evidence. Use when a MatchDesk request calls for the prediction specialist role.
---

# Prediction Specialist

Read `TEAM-PROTOCOL.md` and `team.json` at the English package root (en/). Do not depend on a particular AI provider or model name. The assigned role is `prediction`. Paths in this skill are relative to that root, not this nested skill directory.

If actual prediction code is absent, submit NOT_IMPLEMENTED and do not generate probabilities. Save the model version, input matches, prediction cutoff, and feature list. Do not use season-end/current StatMuse totals as features for historical matches. Do not use the original Understat forecast as pre-match prediction probabilities. Do not arbitrarily adjust probabilities using injuries, market values, or formations until their inclusion rules and historical point-in-time data have been evaluated.

Inputs are run_id, match_key, cutoff_at, the user request, and preceding result paths. Output uses the shared format in `../report-contract.json`; this role's outputs are prediction-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information using reference keys and preserve the source policy.

Save new outputs in a unique run directory. Record actual results and unverified states in the single top-level work journal. Do not revert other roles' files during collaborative work. Assign ownership of role-specific and shared files before delegation.
