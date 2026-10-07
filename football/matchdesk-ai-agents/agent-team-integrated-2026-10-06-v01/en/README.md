# MatchDesk — integrated five-agent team

[한국어 / Korean](../README.md)

The previous ten roles are consolidated into five execution assignees. Capabilities are preserved while reducing handoffs between assignees.

| Agent | Previous roles combined | Responsibilities |
|---|---|---|
| Director and final approver | Manager + operations + final approval | Assign work, manage refresh status, give internal approval after verification |
| Data and trends research | Data + recent trends | Collect match records, squads, formations, values, injuries, and news |
| Analysis and prediction | Analysis + prediction | Compare teams, train on historical matches, calculate probabilities for future matches |
| Visualization and web | Visualization | Charts, web screens, and connecting prediction outputs |
| Independent verification and model evaluation | Validation + model evaluation | Independently check data, calculations, screens, and predictive performance |

Work proceeds as **director → research → analysis/prediction → visualization → verification → director approval**. The director does not author the results, preserving independence of final approval. Directing and final approval are two stages performed by one agent. The user retains the final business decision.

The parent package includes five common skills, five Codex copies, five Claude copies, and five Claude subagent definitions. This English directory provides translated common instructions, five roles, five common skills, five identical Codex skill copies under .agents/skills, five identical Claude skill copies under .claude/skills, five Claude agent definitions under .claude/agents, and team routing. Model selection is not fixed. The existing capability report format, including operations status, and approval rules are preserved; ../tools/integrated_gate.py additionally checks integrated assignment and independence.

Future matches are prediction targets, not training examples. Unpublished actual future lineups do not block basic model prediction. The original 2026-10-06 package recorded the actual prediction model as not implemented; this is a historical configuration statement. Consolidating roles did not itself create a model. The wider project now includes implemented logistic modeling with 111 features and a goal-distribution model, outside this team configuration, in project version 0.12.1. See the [111-feature logistic model](../../modeling/logistic-111-2026-10-07-v01/README.en.md) and [goal-distribution model](../../modeling/goal-distribution-2026-10-07-v01/README.en.md). These implementations do not prove that the complete integrated five-agent workflow has executed or grant model-adoption approval.

This version contains a new configuration and checking code. The existing actual team execution for two representative matches used the earlier ten-role assignment; do not relabel it as a five-agent execution. Actual Claude execution remains unverified, and an automated API runner remains unimplemented. The previous agent-team-2026-10-06-v01 package and actual collection results are preserved.

To review: inspect the role consolidation in the table above. Future work uses the configuration selected by team_selection_2026-10-06-v02.json in the repository root.

Start with [TEAM-PROTOCOL.md](TEAM-PROTOCOL.md), [team.json](team.json), and the corresponding [role](roles/) and [skill](skills/). Shared tools are in ../tools/, shared contracts are ../*.json, and primary data is ../../source-unified-2026-10-06-v01. Relative paths in role and skill instructions are resolved from this English package directory.
