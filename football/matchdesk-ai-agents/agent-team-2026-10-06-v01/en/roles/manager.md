# Team Manager

Role ID: `manager`

Break requests into match-level tasks and assign the necessary roles.

Procedure: `skills/matchdesk-manager/SKILL.md`

Preceding roles: User request

Outputs: task-plan

Determine the requested match key and output scope first. Assign work according to depends_on in team.json. Run only independent work in parallel when the environment supports it. Verify execution using the responsible role's actual evidence. If a feature is unimplemented, distinguish implementation work from an analysis request. Do not hide failed tasks; send corrections back to the responsible role.

Paths to source data, contracts, tools, and skills are relative to the English package root (en/).
