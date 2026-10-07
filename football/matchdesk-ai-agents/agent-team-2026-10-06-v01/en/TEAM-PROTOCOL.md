# Shared Team Contract

Primary-data responsibilities follow ../../source-unified-2026-10-06-v01/source_policy.json. Classify new supplementary information using ../context-data-contract.json. Missing supplementary information does not block existing primary-data analysis, but do not use material that has not actually been obtained in explanations.

Execute in this order: manager → data/trends/operations → prediction/analysis → model-evaluation/visualization → validation → approval. team.json defines dependencies. Requests limited to lookups or data can skip unnecessary model or interface work; record what was skipped.

Submit results using the shared ../report-contract.json. Use consistent run_id and match_key. producer_id identifies the actual checking actor. Even when using the same model, separate the author and reviewer as different work actors. Sequential self-checking without a separate actor must not be described as independent review. State the limitation if the environment does not support independent execution.

Manage role outputs and report evidence in unique run directories, preserving retry results. Append work records only to the single 작업일지.md in the top-level workshop folder. Do not create separate work journals or todo logs.

The final approver reviews mandatory-evidence checks from ../tools/approval_gate.py and the actual reports. APPROVE authorizes display of internal analysis results. REJECT means a correctable error; HOLD means required data or implementation is missing. Internal AI approval is not human approval for source changes, model adoption, or public deployment.

Codex: open this English folder as the working folder to use AGENTS.md and .agents/skills. Pass roles/<role>.md as instructions to the subagent capability supported by the current host. If unavailable, read the skills and execute sequentially, stating the limits of independent review.

Claude Code: open this English folder as the project to use CLAUDE.md, .claude/agents, and .claude/skills. No model is specified, so use the host environment's selection. Do not require simultaneous parallel execution in both tools or claim completed live API integration.

The canonical English skills are in skills/; the two tool-specific copies are identical. When editing, update all three English locations together. The original ../tests/test_team.py checks the Korean package; it does not establish parity of the English copies. Check English-copy parity separately. Other models may later be connected using the same role documents and JSON inputs/outputs. An API-based automatic runner has not been implemented.

All paths to shared tools, contracts, and source data in these instructions are relative to this English package root (en/), rather than to the individual nested document. Run the shared tools from this root with python ../tools/context_cli.py or python ../tools/approval_gate.py.
