# Input data

Source: the [official K League Data Portal](https://data.kleague.com/). Supply the following saved exports in `data/raw/` (or the directory selected by `KLEAGUE_DATA_DIR`).

| File | Expected rows | Purpose |
|---|---:|---|
| `kleague1_2026_round01-30_results_weather.csv` | 180 | Assigned round, actual date, teams, final scores and source URL |
| `kleague1_2026_round01-30_teamstats_raw.csv` | 360 | Provider team-match statistics; two rows per fixture |
| `official_score_reconciliation.csv` | 360 | Saved comparison against official final scores |
| `official_totals_reconciliation.csv` | 564 | Saved team-total checks, including known `GOAL_CNT` discrepancies |

`input_manifest.json` records expected file hashes, row counts and columns. Filenames and source field names are preserved to maintain lineage. Korean team identifiers and the raw score fields `home_득점` / `away_득점` are mapped to English analytical labels in v1; their presence in source-mapping code is intentional.

The raw exports are excluded from Git. Their public redistribution permission has not been established. No credentials, session cookies or personal-machine paths are needed by the analysis scripts. Do not publish credentials or assume that public website access grants a data license.

The source snapshot contains the assigned R22 Gangwon–Incheon fixture played on 2026-09-27. An earlier 179-match export is **not** an interchangeable input. The code deliberately fails if coverage changes; a season-end study needs a new scope and validation rules, not just disabling assertions.

The pipeline reads saved files only. It does not include a crawler, auto-refresh the reconciliation exports, or claim to reproduce source collection from scratch. Snapshot audit date: 2026-09-30.
