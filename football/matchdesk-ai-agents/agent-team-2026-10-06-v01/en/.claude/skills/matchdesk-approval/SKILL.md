---
name: matchdesk-approval
description: Review evidence and decide whether to approve, reject, or hold internal analysis results, with reasons. Use when a MatchDesk request calls for the final approval specialist role.
---

# Final Approval Specialist

Read `TEAM-PROTOCOL.md` and `team.json` at the English package root (en/). Do not depend on a particular AI provider or model name. The assigned role is `approval`. Paths in this skill are relative to that root, not this nested skill directory.

Check that preceding reports use the same run_id and match_key and contain required evidence. Use python ../tools/approval_gate.py <report-bundle.json> for mandatory checks and to determine whether probabilities may be displayed. Separate the approver and validator from result authors. When only data is verified, analysis results may be approved without probabilities. For correctable errors, record REJECT and the responsible role; for missing implementation or required data, record HOLD and the reason. AI approval does not replace the user's approval for model adoption, source changes, or public deployment.

Inputs are run_id, match_key, cutoff_at, the user request, and preceding result paths. Output uses the shared format in `../report-contract.json`; this role's outputs are approval-decision. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information using reference keys and preserve the source policy.

Save new outputs in a unique run directory. Record actual results and unverified states in the single top-level work journal. Do not revert other roles' files during collaborative work. Assign ownership of role-specific and shared files before delegation.
