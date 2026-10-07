---
name: matchdesk-operations
description: Verify actual collection/refresh execution times and failures, and manage reruns. Use when a MatchDesk request calls for the operations and refresh specialist role.
---

# Operations and Refresh Specialist

Read `TEAM-PROTOCOL.md` and `team.json` at the English package root (en/). Do not depend on a particular AI provider or model name. The assigned role is `operations`. Paths in this skill are relative to that root, not this nested skill directory.

Refresh into new versions without overwriting originals. Distinguish refresh times of primary Understat data and separate supplementary data. Recheck news and injuries before the match and preserve market-value valuation dates. If no refresh occurred, do not claim the data is current or unchanged. Do not register automations or external notifications without a user request. Mark collection functionality with no actual connection as NOT_IMPLEMENTED.

Inputs are run_id, match_key, cutoff_at, the user request, and preceding result paths. Output uses the shared format in `../report-contract.json`; this role's outputs are operations-report. Do not record actual execution as DONE/PASS without evidence files. Link primary data and supplementary information using reference keys and preserve the source policy.

Save new outputs in a unique run directory. Record actual results and unverified states in the single top-level work journal. Do not revert other roles' files during collaborative work. Assign ownership of role-specific and shared files before delegation.
