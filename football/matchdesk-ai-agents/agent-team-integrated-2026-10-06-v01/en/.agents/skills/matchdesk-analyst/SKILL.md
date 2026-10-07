---
name: matchdesk-analyst
description: Perform integrated analysis and prediction work in MatchDesk. Use when executing the analyst assignee in the five-agent team.
---

# Analysis and prediction

Read TEAM-PROTOCOL.md and team.json first. The current assignee is `analyst`; the existing capability scope is analysis, prediction.

Handle both recent-performance comparisons and prediction-model development/execution. Future matches are prediction targets, and training labels are historical match results. Historical training inputs contain only information knowable before that match started. Unpublished actual future lineups are not a prerequisite that blocks basic model prediction. If inputs required by the chosen model are missing, record the rationale for handling their absence. Do not give final approval to your own model's performance.

For actual execution, follow the detailed procedures in roles/analyst.md and ../report-contract.json. Do not describe reports for the same capability as executions by separate agents. producer_id identifies the actual responsible actor. Do not fix the model or provider. Preserve collaborators' changes and earlier artifacts. Leave unexecuted capabilities as NOT_IMPLEMENTED and unverified data as MISSING/BLOCKED.

Resolve these paths from the English package directory that contains TEAM-PROTOCOL.md and team.json.
