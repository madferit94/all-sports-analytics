---
name: matchdesk-reviewer
description: Perform integrated independent verification and model evaluation work in MatchDesk. Use when executing the reviewer assignee in the five-agent team.
---

# Independent verification and model evaluation

Read TEAM-PROTOCOL.md and team.json first. The current assignee is `reviewer`; the existing capability scope is validation, model-evaluation.

Independently check collected data, calculations, screens, and model performance, separate from their authors. Check chronological training/evaluation separation and leakage of post-match information. Review accuracy together with probability error, calibration, and baseline-model comparisons. If there is no model, leave evaluation as not implemented. One reviewer may perform both data and model checks, but must differ from the collection/model/screen authors.

For actual execution, follow the detailed procedures in roles/reviewer.md and ../report-contract.json. Do not describe reports for the same capability as executions by separate agents. producer_id identifies the actual responsible actor. Do not fix the model or provider. Preserve collaborators' changes and earlier artifacts. Leave unexecuted capabilities as NOT_IMPLEMENTED and unverified data as MISSING/BLOCKED.

Resolve these paths from the English package directory that contains TEAM-PROTOCOL.md and team.json.
