# Execution protocol for five agents

Director planning → research → analysis/prediction → visualization (may be omitted depending on the request) → independent verification/model evaluation → final internal approval by the same director.

The phases in team.json are work stages; its roles are the five actual assignees. Do not count the director's planning and approval as two separate AIs. The same reviewer performs data verification and model evaluation. The producer_id of analysis, collection, and screen authors must differ from those of the reviewer and approver. The final approver must also differ from the reviewer. A director who directly authored a feature must not give final approval to their own output.

Reports include agent_id, producer_id, run_id, match_key, and reports for individual capabilities. Preserve the existing ../report-contract.json format for internal capability reports so they remain compatible with the earlier validation code. Ten capability report types do not mean ten agents. Verify the integrated assignee names and the actual execution identities.

Use ../tools/integrated_gate.py to check assignment/reporting identities and apply the existing approval rules. The analysis mode requires data, analysis, validation, and operations; prediction also requires prediction and model evaluation; web also requires visualization. Record omitted optional capabilities. Even after the rules pass, the final assignee reads the actual evidence. Distinguish whether a refresh was performed in an operations report from whether automatic refresh is implemented.

Actual lineups for future matches may be unpublished before kickoff. Do not force them to be prerequisites for basic prediction. Historical training uses recent records that were knowable at the time, with actual results as training labels. Do not insert current cumulative statistics, current squads, or actual post-match lineups into historical inputs.

Actual team execution uses the current host's subagent functionality, supplying roles/<agent>.md. All five assignees need not run simultaneously. A separate automated API runner is not implemented. In environments without independent execution, do not call self-checking independent verification. Having Claude and Codex configuration files does not prove that actual execution has been verified on both.

All relative paths above are resolved from this English package directory. Shared tools and contracts remain in the parent package.
