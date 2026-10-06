# Analysis tool contract / 분석 도구 규격

Offline mode executes browser JavaScript over unchanged completed-match JSON. Release 0.8.0 also provides a local Gemini server: with a locally configured key, the model selects validated conditions and server JavaScript computes records. Live Gemini success is unverified until the user supplies a key. SQL and Python runtimes remain unconnected. The skills are project workflow documents, not automatically installed global Codex skills.

## Current pipeline

`question → parse → plan → registered calculation → result → renderer`

Plan: `tool, teams, league, season, last, venue, metric, perMatch, question`. Result: `status, tool, plan, rows, metric, formula, engine, datasetThrough, verification`. Missing records produce `empty`, unsupported conditions produce `unsupported`, missing prediction produces `unavailable`. In particular, historical win rate is not a predicted win probability.

Built-in tools: team, comparison, ranking, venue, trend. Metrics: gf, ga, xg, xga, p, w. Recent counts 1–38 within a season. No custom-date, match-result, player, shot-coordinate or seasonal StatMuse metric analysis is connected in this workbench. The separate team screen still exposes its existing 47 season metrics.

## Extending to another service

`recordAnalyst.register(name, execute, optionalMatch)` adds a synchronous handler and optional question matcher. A matcher returns explicit parameters or null when inapplicable. It runs before football parsing. The handler must provide `tool:name` in its result for custom rendering.

`registerAnalysisService({name, parse, execute, render})` additionally registers the service renderer. Renderers must escape untrusted strings and distinguish failure/missing data. No new service is connected in this release. The record handler contract is synchronous. Release 0.8.0 adds an asynchronous same-origin /api/analyze transport for Gemini planning. Other remote/SQL/Python services still require their own authenticated adapters and tests.

Prediction adapter should return home/draw/away probabilities, model version, fixture ID, data cutoff, actual validation performance and adoption state. It must not turn arbitrary LLM text into probabilities. Current model adoption remains false.

## Ownership and execution evidence

| Role | Responsibility | This release |
|---|---|---|
| Analyst | Conditions, calculation, tool routing | Implemented by primary Codex |
| Builder | Workbench, chart/table, bilingual UI, fonts | Implemented by primary Codex |
| Reviewer | Independent expected-value comparisons and regression checks | Automated checks by primary Codex; no separate reviewer agent executed |
| Director | Record scope, evidence and human confirmation | Primary Codex records; human visual confirmation pending |

Existing five-agent roles are reused; no extra agents are required. Future runs may assign these responsibilities separately. Documentation does not prove a multi-agent execution occurred.
