# MatchDesk Agent Team — Tool-Independent Structure (English)

This is the English translation of the earlier 10-role package in the parent folder. It is not the current active five-person team configuration. Preserve the original role IDs and report keys when exchanging reports with the shared tools.

**Historical scope:** statements below about absent prediction-model implementation and original verification/collection results describe the package record dated 2026-10-06. They are not a statement of the entire project's current implementation. As of project version 0.12.1, the project has selected a logistic model and a learned goal-distribution model outside these agent-configuration documents. See [logistic model](../../modeling/logistic-111-2026-10-07-v01/README.en.md) and [learned goal-distribution model](../../modeling/goal-distribution-2026-10-07-v01/README.en.md). This annotation does not establish that the historical 10-role team ran those models. Native Claude execution and automatic discovery remain unverified here; the API-based automatic agent runner remains unimplemented.

Rest days belong to the supplementary collection contract's scope. Their inclusion in that contract does not mean the currently selected models use a rest-days feature; those models do not currently use it.

**The original package created 10 roles, 10 shared skills, Codex and Claude Code connection files, and executable data-validation and approval-checking code.** It does not pin an AI provider or model. Full collection automation, prediction-model implementation, and web implementation are separate stages. Awaiting participant confirmation.

| Role | Responsibility |
|---|---|
| Team Manager | Task assignment, dependencies, and reassignment of failed tasks |
| Data and Squad Specialist | Primary data and supplementary formations, lineups, squads, and market values |
| Recent Team Trends Specialist | Injuries, suspensions, transfers, managerial changes, and official announcements |
| Prediction Specialist | Home-win/draw/away-win probabilities based on calculation code |
| Match Analysis Specialist | Performance, tactics, and squad comparisons and explanations |
| Visualization and Web Specialist | Match-comparison interfaces, charts, and missing-data states |
| Model Evaluation Specialist | Independent evaluation on historical matches |
| Validation Specialist | Actual checks of data, calculations, explanations, and interfaces |
| Operations and Refresh Specialist | Collection execution, freshness, and failure checks |
| Final Approval Specialist | Approval, rejection, or hold after reviewing evidence |

The human user makes final decisions on source-policy changes, model adoption, and public deployment. AI approval concerns internal analysis results.

## Additional Collection Fields

The shared `../context-data-contract.json` defines formations, starting lineups, squad composition, squad market values, injury/suspension/availability states, coaches, transfers, news, and rest days. The data/squad and recent-trends skills are connected to collect and check this material.

- Keep the existing Understat choice for primary matches, schedules, and xG. The additional 47 StatMuse statistic types and supplementary information remain separate.
- Distinguish confirmed and expected lineups. Confirmed lineups must contain 11 distinct starting players.
- Distinguish nominal starting formations and expected formations. Do not claim that actual in-match positions were verified.
- Save market-value valuation date, currency, amount, and player/squad scope. Values are estimates; do not use them as club enterprise values or actual transfer fees.
- Attach team keys, source URLs, observation times, and information states to every item. Injury information does not automatically confirm absence from a future match.
- Record MISSING/BLOCKED and reasons for unavailable supplementary material. Do not replace it with zero.
- Supplementary information is initially for explanation. Do not add it to historical prediction features until point-in-time data and evaluation are available.

Candidate sources are FotMob for formations/lineups, Transfermarkt for market values, and official club/league announcements for trends. The original session read [FotMob match information](https://www.fotmob.com/matches/liverpool-vs-west-ham-united/2h59kq) to inspect functionality. The Transfermarkt definition page could not be retrieved during that lookup. Collection connections for all teams and matches were not verified. Candidates and statuses are in `../source-routing.json`. **The original package reports zero newly collected supplementary records; test players and amounts were used only as synthetic validation inputs.** Translation does not establish a new collection result.

## Using the Two Tools

Open this English folder (en/) as the project working folder. Canonical English skills are in `skills/`, role documents in `roles/`, and task connections in `team.json`.

- Codex: `AGENTS.md` and shared skill copies in `.agents/skills/`. Assign roles using the actual subagent tools available in the host. [OpenAI official skill documentation](https://learn.chatgpt.com/docs/build-skills)
- Claude Code: `CLAUDE.md`, 10 subagent definitions in `.claude/agents/`, and skill copies in `.claude/skills/`. [Claude skills documentation](https://code.claude.com/docs/en/skills), [subagent documentation](https://code.claude.com/docs/en/sub-agents)
- Model/provider choices are not fixed. Follow the host's defaults and record the actual tool/model in reports when known.
- If parallel capability is unavailable, execute sequentially with the same input/output format. Do not label sequential self-checking as independent validation.

**Actual Claude Code execution and automatic discovery in either tool were not tested in the original session.** Load this package by opening its folder; do not claim automatic installation into the currently open parent workshop folder. There is no API-based unattended runner.

English documents share the original executable tools and contracts; they do not duplicate or modify them. All shared paths below, and in nested role/skill documents, are relative to the English package root. Primary data is `../../source-unified-2026-10-06-v01`.

## Executable Shared Checks

From en/, run `python ../tools/context_cli.py validate <data.json>` to check supplementary keys, sources, time zones, information states, confirmed/expected lineups, and market-value formats. This checks structure; it does not certify factual correctness.

Run `python ../tools/approval_gate.py <report-bundle.json>` to check required reports for analysis/prediction/web modes, existence of actual evidence files, separation of checking actors, mandatory errors, and probability sums/ranges. Missing models or required evidence yield HOLD; errors yield REJECT; satisfied mandatory conditions yield APPROVE. The final approval agent must review both this code's result and evidence contents. The code does not determine whether file contents are true or certify human deployment approval.

See TEAM-PROTOCOL.md and `../report-contract.json` for execution order and contracts. A report bundle includes run_id, match_key, mode, reviewer_id, and reports; reports uses role IDs as keys. Prediction reports add probabilities.home/draw/away; evaluation reports add model_accepted. Do not create completion reports without files and results.

## Verification Status Preserved from the Original Package

The following are original-package results, not claims that the English translation ran the team:

- `../tests/test_team.py`: seven behavior tests passed. Checks covered incorrect match references, zero-filled missing data, expected lineups presented as confirmed, currency errors, invalid values, approval of probabilities without a model, incorrect probability sums, self-validation, and out-of-scope evidence.
- No cycles in the 10-role dependency graph; the original skill files were identical in their three locations.
- The original quick_validate.py run failed because PyYAML was missing. A simplified format check verified required frontmatter, names, descriptions, and paths for 10 skills. This was not reported as a pass of the standard validator.
- The primary-data source was not changed. No claim was made that prediction models, web interfaces, automatic refresh, or new supplementary collection were complete.

The original test script checks the parent Korean package. English file parity and reference paths must be checked separately; translation alone does not verify live collection, tool discovery, or independent team execution.

First review the team table and additional collection fields. An example request is: “Check data and recent trends for Arsenal's next match and analyze it without probabilities.” The manager then assigns the necessary roles in analysis mode. If required sources cannot be accessed, leave the corresponding fields held/missing.
