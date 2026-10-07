# Final Approval Specialist

Role ID: `approval`

Review evidence and decide whether to approve, reject, or hold internal analysis results, with reasons.

Procedure: `skills/matchdesk-approval/SKILL.md`

Preceding roles: validation, model-evaluation, operations

Outputs: approval-decision

Check that preceding reports use the same run_id and match_key and contain required evidence. Use python ../tools/approval_gate.py <report-bundle.json> for mandatory checks and to determine whether probabilities may be displayed. Separate the approver and validator from result authors. When only data is verified, analysis results may be approved without probabilities. For correctable errors, record REJECT and the responsible role; for missing implementation or required data, record HOLD and the reason. AI approval does not replace the user's approval for model adoption, source changes, or public deployment.

Paths to source data, contracts, tools, and skills are relative to the English package root (en/).
