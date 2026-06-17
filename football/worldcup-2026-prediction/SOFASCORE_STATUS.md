# SofaScore Collection Status

Goal: collect match results, statistics, lineups, formations, and incidents for international matches.

Current environment result:

- `requests` access to `https://www.sofascore.com/api/v1/...` returns `403 Forbidden`.
- Chrome headless can sometimes load the public football page, but date pages and API URLs are unstable or return `403`.
- Because of that, bulk SofaScore collection was not run to avoid incomplete or distorted data.

Working data collected instead:

- `data/processed/international_matches_2023_plus.csv`
- `data/processed/worldcup48_matches_2023_plus.csv`

The SofaScore retry script is available at:

- `scripts/collect_sofascore.py`

It expects `data/processed/sofascore_event_ids.csv` with an `event_id` column. Once valid SofaScore event IDs are available, it can collect:

- event summary
- match statistics
- lineups and formations
- incidents
