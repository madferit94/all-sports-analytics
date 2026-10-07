---
name: sql-analysis
description: Preserve the scope and execution evidence of completed-match queries and aggregates when connecting a SQL runtime to MatchDesk. This does not mean the current HTML runtime executes SQL.
---

Before connection: the HTML queries JSON using JavaScript. Apply this skill's SQL execution procedure only in work that provides a SQL engine and database connection.

- Translate requests into team/league/season/date/venue conditions. Separate completed matches from scheduled fixtures.
- Read the actual schema first and join using match/team identifiers. Do not combine records using team-name string matches alone. Watch for duplicate counting of the two team rows for each match.
- Use read-only SELECT statements and bound parameters. Do not concatenate user sentences directly into SQL code. Set execution-time and row-count limits.
- A zero denominator or absent data produces NULL. Divide per-match averages by the team's actual match count. PPDA is the sum of numerators divided by the sum of denominators, not a simple mean of match-level ratios.
- Record the complete executed SQL, parameters, returned row count and data cutoff. When reporting SQL execution results in this workshop, include the complete executed SQL in the final response as well.
- Register tables from another service as a scope separate from the current dataset. Check new data-access permissions and whether a real connection exists first.

