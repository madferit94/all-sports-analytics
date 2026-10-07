# MatchDesk agents and analysis skills

Open the [English application](../index.en.html) to view the project. The agent packages and skills below describe responsibilities and workflows; reading them does not start agents or install tools.

## Agent packages

- [Current five-agent package](../agent-team-integrated-2026-10-06-v01/en/README.md): Director plans and assigns work, Research collects evidence, Analyst compares teams and evaluates models, Builder implements the viewer and service, and Reviewer checks evidence independently.
- [Preserved ten-role package](../agent-team-2026-10-06-v01/en/README.md): the earlier, more granular role arrangement. The [archived representative run](../team-run-2026-10-06-v01/README.md) used that earlier arrangement; it must not be relabelled as a five-agent execution.

Reviewer and final Director responsibilities stay separate from authors and each other. Human users retain model-adoption and business decisions. Package descriptions alone do not prove that separate agents executed a task.

## English analysis skills

| Skill | Canonical English entry point | Purpose |
|---|---|---|
| record-analysis | [skills/record-analysis/en/SKILL.md](../skills/record-analysis/en/SKILL.md) | Scope stored-record questions and report calculations, missing data and evidence. |
| sql-analysis | [skills/sql-analysis/en/SKILL.md](../skills/sql-analysis/en/SKILL.md) | Use safe completed-match queries and retain execution evidence when a SQL runtime is provided. |
| python-analysis | [skills/python-analysis/en/SKILL.md](../skills/python-analysis/en/SKILL.md) | Verify calculations, tables, charts and model outputs when a Python tool is provided. |

The Korean entry points remain at `skills/<skill-name>/SKILL.md`. Each English translation preserves the original skill name in its frontmatter. These project documents are not automatically installed global Codex skills.

To use an English skill in this checkout, explicitly ask Codex to read its canonical `skills/<skill-name>/en/SKILL.md` path. The nested English folder is the language-specific entry point; do not assume normal discovery of the parent skill automatically selects it.

If copying an English entry point into an installed skill folder, place its contents at that folder's `SKILL.md` and preserve its name. Review relative links after moving it. The record-analysis translation shares [the project's tool contract](ANALYSIS-TOOLS.md) through `../../../docs/ANALYSIS-TOOLS.md`, resolved from its canonical `en/` folder. A standalone copy needs that reference copied and its link updated, or a path back to the original project. The SQL and Python skills currently have no separate scripts, references or assets to copy.

## Actual implementation and connection status

The [record engine](../analysis/record-engine.cjs) runs JavaScript over stored match JSON. Offline requests use browser JavaScript. The [local Gemini adapter](../server/gemini.cjs) can plan validated conditions and compute records in server JavaScript with a locally configured key; [its setup guide](../server/README.ko.md) is preserved in Korean. Live authentication/model success must be verified separately; documentation is not evidence of a successful live call.

SQL and Python runtimes are not connected to the HTML analysis workbench. Their skills are connection workflows, not evidence that either language executed. The [analysis tool contract](ANALYSIS-TOOLS.md) describes registration, result fields, missing/unsupported states and adapter requirements. Its historical prediction-adoption statements describe the release that created that contract; consult the [current model-scope document](MODEL-SCOPE-2026-10-07-v02.ko.md) and current release specifications before making a current model-adoption claim.

Historical win rate is wins divided by completed matches, and is distinct from predicted win probability. A prediction adapter needs a model version, fixture identifier, data cutoff, validation evidence and adoption state. Record actual code/queries and verification results when tools really execute; do not describe proposed SQL or Python procedures as completed runs.

