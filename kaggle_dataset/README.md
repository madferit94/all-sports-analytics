# 2026 FIFA World Cup Prediction Dataset

This dataset supports a 2026 FIFA World Cup match prediction workflow using historical international results, FotMob match statistics, and Transfermarkt national team profiles.

## Dataset Purpose

The dataset is designed for:

- Building pre-match team form features
- Training win/draw/loss prediction models
- Predicting group-stage match outcomes
- Simulating knockout-stage outcomes
- Comparing model outputs across multiple machine learning models

## Input Files

These files are used to rebuild the modeling dataset in the notebook.

| File | Description |
|---|---|
| `input/fotmob_match_ids_extracted.csv` | Historical international matches involving the World Cup teams, with FotMob match IDs and match results. |
| `input/fotmob_statistics_long.csv` | FotMob team-level match statistics in long format. Used to create recent 5-match rolling form features. |
| `input/transfermarkt_country_profile.csv` | National team profile data from Transfermarkt: squad size, average age, FIFA ranking, and total market value. |
| `input/worldcup48_matches_2023_plus.csv` | Filtered historical matches where at least one of the 48 World Cup teams appears. |
| `input/international_matches_2023_plus.csv` | Broader international match results from 2023 onward. |
| `input/transfermarkt_country_sources.csv` | Source URLs for Transfermarkt national team pages. |
| `input/sources.csv` | Source registry for data collection. |

## Output Files

The `outputs/` folder contains generated model results.

| Pattern | Description |
|---|---|
| `outputs/model_validation_scores.csv` | Validation scores for each candidate model. |
| `outputs/champions_by_model.csv` | Predicted champion and final matchup by model. |
| `outputs/group_predictions_*.csv` | Group-stage predictions by model. |
| `outputs/group_table_*.csv` | Predicted group table by model. |
| `outputs/qualified_teams_*.csv` | Predicted Round of 32 qualifiers by model. |
| `outputs/tournament_results_*.csv` | Predicted knockout-stage bracket by model. |

## Modeling Notes

- Prediction cutoff date: `2026-06-11`
- Training window: the year before the prediction cutoff date
- Recent-form features use only matches before the prediction date
- Rolling features use previous matches only to avoid same-match data leakage
- Transfermarkt values are used as current strength indicators

## Limitations

- Transfermarkt historical snapshots are not included.
- FotMob coverage varies across international matches.
- The knockout bracket in the notebook uses a simplified seeded bracket, not the official FIFA third-place allocation table.
- Predictions are model outputs and should not be interpreted as certain outcomes.

