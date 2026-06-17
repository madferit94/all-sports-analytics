# 2026 FIFA World Cup Match Prediction

This project builds a match prediction workflow for the 2026 FIFA World Cup.

The model combines:

- International match results from 2023 onward
- FotMob match statistics transformed into pre-match rolling form features
- Transfermarkt national team profile data such as squad size, average age, FIFA ranking, and total market value

The main goal is to avoid data leakage. For every prediction, recent form features are calculated only from matches that happened before the prediction date.

## Project Structure

```text
.
├── 2026Worldcuo predict.ipynb        # Main prediction notebook
├── WorldCup Scrape.ipynb             # Data collection and preparation notebook
├── requirements.txt
├── scripts/
│   ├── build_ml_match_dataset.py
│   ├── train_baseline_model.py
│   └── collect_sofascore.py
├── data/
│   ├── processed/
│   └── raw/                          # Excluded from Git by default
└── README_EN.md
```

## Core Input Files

The current baseline prediction workflow uses these processed files:

```text
data/processed/fotmob_match_ids_extracted.csv
data/processed/fotmob_statistics_long.csv
data/processed/transfermarkt_country_profile.csv
```

Optional supporting files:

```text
data/processed/worldcup48_matches_2023_plus.csv
data/processed/international_matches_2023_plus.csv
transfermarkt_country_sources.csv
```

Large raw crawl files are intentionally excluded from GitHub by `.gitignore`.

## Method

For each historical match, the dataset creates:

- Home and away Transfermarkt features
- Differences between home and away Transfermarkt features
- Recent 5-match rolling averages for each team
- Differences between home and away recent form features
- Match outcome label: `home_win`, `draw`, or `away_win`

The rolling features use `shift(1)`, so the current match is not included in its own pre-match features.

## Prediction Setup

The World Cup prediction workflow uses an `as_of_date`.

For example:

```python
as_of_date = pd.Timestamp("2026-06-11")
```

This means:

- Only matches before `2026-06-11` are used to calculate recent form.
- World Cup group-stage matches on or after that date are treated as future fixtures.
- Future match results and future match statistics are not used.

## Models

The notebook can compare multiple models:

- Logistic Regression
- Random Forest
- Extra Trees
- Gradient Boosting
- HistGradientBoosting
- XGBoost
- MLP neural network

Model selection can be based on validation `log_loss` and `accuracy`, or each model's World Cup prediction output can be reviewed separately.

## Outputs

The workflow can generate:

- Group-stage win/draw/loss probabilities
- Predicted scores
- Predicted group tables
- Qualified Round of 32 teams
- Knockout-stage predictions
- A predicted champion

## Important Limitations

- Transfermarkt values are treated as current team strength indicators. Historical market value snapshots are not used.
- FotMob detail coverage varies by match. Some international matches have fewer detailed statistics.
- The current knockout bracket code uses a simplified Round of 32 assignment. The official FIFA third-place allocation table should be added for an exact 2026 bracket.
- Predictions are model-based estimates, not guarantees.

## Reproducibility

Install dependencies:

```bash
pip install -r requirements.txt
```

Then run the notebooks from top to bottom.

For GitHub, commit the code, notebooks, and small processed CSV files. Avoid committing `data/raw/` unless you intentionally want to publish the full crawl cache.

