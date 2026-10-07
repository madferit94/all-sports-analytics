---
name: record-analysis
description: Translate natural-language requests about MatchDesk stored match records into conditions, aggregates, tables and charts, while distinguishing prediction requests.
---

The current record engine is browser JavaScript in `analysis/record-engine.cjs`; an LLM is not connected to that engine. This skill document is not an executable tool.

- Specify match identifiers, teams, season, range, venue and metrics. For omitted conditions, use the team/league/season selected in the viewer, all venues and the full season; show these defaults in the result.
- Currently supported: goals scored/conceded, xG/xGA, points, historical win rate, team comparisons, league rankings, home/away comparisons and goals/xG trends. Recent N means completed matches within the selected season; venue comparisons use N separately for each venue.
- State when a metric, league, season or complex condition is unsupported. Absent data is missing, not zero. Exclude future fixtures from historical aggregates.
- Win rate means historical wins divided by matches played. A win-probability tool cannot run until its model version, pre-cutoff data and performance validation are connected.
- Calculation results must show conditions, data cutoff, actual execution language, formula, per-row values and verification status. Do not record SQL/Python plans in documentation as actual execution.
- Follow the [tool contract](../../../docs/ANALYSIS-TOOLS.md) when extending tools. Distinguish implementation owners from verification owners; the work described in the original skill was implemented and automatically checked by a single Codex instance.

