# Big Five Striker Data — 2025/26

[English](README.md) | [한국어](README.ko.md)

Understat data collected for a player-profile study comparing **non-penalty shot frequency** and **average non-penalty shot quality**. This package contains reproducible collection code, a processed season snapshot, original-response hashes and internal reconciliation checks. Full raw responses remain in the local cache.

## Problem and analysis question

Goal totals alone combine shooting opportunities, shot selection and finishing outcomes. For an initial scouting comparison, the question is: **which central-forward candidates generate frequent non-penalty shots, and which receive or select higher-xG chances per attempt?**

The proposed two-axis profile separates shot frequency from average model-estimated chance quality. Its next use is to identify contrasting profiles for closer contextual review. It does not establish a player's overall quality or transfer suitability.

**Project status:** data collection and validation complete; scatterplot analysis, contextual interpretation and scouting conclusions are still to be developed. Counts below describe data coverage, not football findings.

## Collected snapshot

Collected on 3 October 2026 (Asia/Seoul). The snapshot contains 1,752 league fixtures, 2,775 player-league summary rows and detailed responses for 1,013 unique players. The scoped event table contains 24,185 entries, including 8 OwnGoal entries excluded from attacking shot metrics.

The default scatter input contains **181 unique players / 181 player-league rows**: EPL 33, La Liga 38, Bundesliga 30, Serie A 50 and Ligue 1 30. All selected rows pass source reconciliation. Twelve other candidate rows are quarantined because of a source duplication issue described below. Download failures: zero. Saved CSV joins, metric identities, selection and all 1,018 raw-file hashes pass the independent verification script.

## Read these files first

| File | Purpose | One row represents |
|---|---|---|
| `data/processed/striker_scatter_ready.csv` | Default chart inputs: internally reconciled central-forward candidates with at least 900 minutes | Player × league × season |
| `data/processed/forward_candidate_audit.csv` | All detailed candidates, role classification, inclusion flags and validation checks | Player × league × season |
| `data/processed/all_players_league_season.csv` | Original league-summary fields for every listed player, including players outside the detailed scope | Player × league × season |
| `data/processed/shot_events.csv` | Source shot-event xG, penalty flags, coordinates and match IDs; `OwnGoal` entries retained and flagged | One source event |
| `data/processed/player_match_records.csv` | Minutes, recorded position and statistical totals | Player × match |
| `data/processed/position_summary.csv` | Minutes attributed to recorded match-position codes | Player × league × position |
| `data/processed/league_matches.csv` | League fixture coverage and the authoritative inclusion list | One match |
| `data/processed/league_coverage.csv` | Coverage counts for each league | One league |
| `data/processed/minutes_threshold_counts.csv` | Candidate counts at 450, 600, 900, 1,200 and 1,500 minutes | League × minutes threshold |
| `data/processed/reconciliation_exceptions.csv` | Rows failing one or more internal reconciliation checks | Player × league × season |
| `data/processed/source_duplicate_appearances.csv` | Source duplicate records and retained/duplicate roster IDs | One removed duplicate appearance |
| `data_dictionary.csv` | Definitions of the main analytical columns | One field |
| `validation.json` | Machine-readable collection and validation summary | — |
| `saved_data_verification.json` | Independent checks of saved CSV joins, selection, metric identities and original raw-file hashes | — |
| `csv_verification.json` | Verification of the public CSV snapshot without the local raw cache | — |
| `raw_manifest.json` | SHA-256 hashes and sizes of source snapshots | One source file |

## Scope and row identity

- Competitions: Premier League (`EPL`), La Liga (`La_liga`), Bundesliga, Serie A (`Serie_A`) and Ligue 1 (`Ligue_1`).
- Season: **2025/26**, encoded as `2025` by Understat.
- All players listed in the five league summaries are preserved.
- Player details are collected for everyone whose source position flags include `F`, plus players flagged only `S` (substitute-only, starting role unknown). **There is no minutes cutoff at collection time.**
- Players without either flag retain their league summaries only. This is not a shot-event dataset for every player in Europe.
- Player API responses contain historical seasons. Processed tables include only match IDs present in the five 2025/26 league fixture lists, not a calendar-year date filter.
- Transfers within a league are aggregated by the source. Transfers between leagues are separate rows in league-season tables. Therefore, **a player may appear twice in the five-league scatter input**; keep this distinction or explicitly aggregate the underlying counts before plotting one point per player. Never average per-90 rates without exposure weights.
- Source player IDs, names, position labels and team names are preserved. There is no name-based join.
- No raw source file is overwritten on a repeat run. To collect a new snapshot, copy the script into a new dated output directory instead of mixing downloads with this snapshot.

## Default central-forward candidate rule

League flags such as `F M S` are too broad to identify central strikers on their own. For detailed candidates, match-position codes distinguish `FW`, `FWR`, `FWL`, `AMC`, etc.

The default rule is deliberately explicit:

1. Exclude `Sub` from the denominator used to measure the share of known recorded positions. Do not impute substitute appearances as centre-forward appearances.
2. Require non-`Sub` recorded minutes to represent at least 50% of total minutes.
3. Require `FW` to account for at least 50% of non-`Sub` recorded minutes.
4. For the default scatter input, also require at least 900 total league minutes, at least one non-penalty shot and all reconciliation checks to pass.

The classification is **central-forward candidate**, not a confirmed tactical-role label. Match-position codes are not a continuous record of where a player played during a match. All season appearances contribute to the shot and per-90 metrics, including appearances in other recorded positions. The thresholds are analysis choices, not official Understat definitions.

`insufficient_known_position` and `other_forward_or_mixed_role` remain available in the audit file. Missing positional evidence is not evidence of poor performance.

## Axis definitions

```text
non_penalty_shots = count(events where situation != 'Penalty' and result != 'OwnGoal')
shot_sum_npxg     = sum(xG for those same non-penalty shot events)
npshots_per90     = non_penalty_shots / league minutes * 90
npxg_per_shot     = shot_sum_npxg / non_penalty_shots
npxg_per90        = shot_sum_npxg / league minutes * 90
```

Penalties are excluded whether scored or missed. Source `OwnGoal` events remain in `shot_events.csv` with `counts_as_attempt=False` but are excluded from analytical shot counts and xG sums. The source includes these zero-xG entries in player event lists while excluding them from player attacking shot totals; this was identified by reconciling source summaries with event lists. Corners, other set pieces and direct free kicks remain included. **Non-penalty is not the same as open play.**

Zero denominators produce empty CSV cells, not fabricated zeros. `npxg` is the source aggregate; `shot_sum_npxg` is the independently summed value from the same provider's shot records. Their agreement is checked with absolute tolerance `0.0001`.

The identity `npshots_per90 * npxg_per_shot = npxg_per90` should hold for nonzero shot counts. Average xG per shot measures the model's estimated chance quality, not finishing skill or individual causal contribution.

## Validation

The pipeline checks:

- Completed fixture coverage: 380 matches each in EPL, La Liga and Serie A; 306 each in Bundesliga and Ligue 1.
- Unique league-player keys, match IDs, player-match keys and shot IDs.
- Every retained shot maps to a retained player appearance and a scoped league match.
- Shot xG and coordinates fall in `[0, 1]`.
- Source league totals reconcile with detailed records for appearances, minutes, shots, xG, non-penalty xG, goals and non-penalty goals.
- Assigned position minutes sum to the player's league minutes.

Rows that fail reconciliation remain in the audit and exceptions tables and are excluded from the default scatter. Source discrepancies are not silently corrected. These checks establish internal consistency, **not independent validation of every event or of the provider's xG model**.

### Observed source duplication

For Real Oviedo–Villarreal, match `29482` on 23 April 2026, 12 collected players each have two appearance records identical except for `roster_id`. The provider's season appearance and minutes totals also include the extra entry. Raw responses and source summary totals remain untouched. `player_match_records.csv` retains the record with the lowest roster ID, and the duplicate IDs are listed in `source_duplicate_appearances.csv`. Conflicting duplicates would stop the pipeline rather than be arbitrarily selected.

All 12 affected player-league rows fail `no_source_duplicate_appearances` and are excluded from the chart input. `unique_appearance_count` and `unique_appearance_minutes` expose deduplicated totals alongside the unchanged source totals. Metrics on failed audit rows must not be treated as validated. Deduplication alone does not establish the correctness of the source's other match statistics.

League-strength, team possession, tactical instructions, game state and quality of teammate service are not adjusted. Do not interpret the chart as a league-adjusted talent ranking.

## Reproduce or resume

Python 3.11 or later; only the Python standard library is required.

From this project folder, verify the published CSVs without downloading anything:

```bash
python3 verify_saved_data.py
```

This writes `csv_verification.json`. The original full-cache validation receipt is preserved in `saved_data_verification.json`.

To collect a fresh snapshot, copy `collect_understat.py` and `verify_saved_data.py` to a new empty directory and run:

```bash
python3 collect_understat.py
python3 verify_saved_data.py --verify-raw
```

Fresh source responses may differ from the published snapshot. To resume an existing local collection, rerun the collector in that collection folder; existing raw files are reused and processed CSVs are rebuilt. To verify the original snapshot's raw hashes, supply the original local cache; a fresh download cannot guarantee the same bytes.

The script uses two download workers, globally spaced requests, bounded retries and raw caching. A rerun resumes missing responses and rebuilds processed tables. CSVs are UTF-8 with BOM for convenient spreadsheet use. `data/raw/**/*.meta.json` records source URLs, UTC retrieval timestamps, HTTP metadata and hashes; `raw_manifest.json` covers the decoded source JSON bytes.

The read-only endpoints were identified in the site's own `league.min.js` and `player.min.js`; they are website endpoints rather than a guaranteed stable, documented public API.

## Sources

- [EPL 2025/26](https://understat.com/league/EPL/2025)
- [La Liga 2025/26](https://understat.com/league/La_liga/2025)
- [Bundesliga 2025/26](https://understat.com/league/Bundesliga/2025)
- [Serie A 2025/26](https://understat.com/league/Serie_A/2025)
- [Ligue 1 2025/26](https://understat.com/league/Ligue_1/2025)

Keep Understat attribution with any derived chart. This repository includes season-scoped processed tables, code and validation records. Full historical raw responses are excluded according to the repository's raw-cache convention; they remain preserved locally. No redistribution license for the provider's raw data is asserted.
