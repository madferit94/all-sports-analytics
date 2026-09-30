# %% Setup: resolve paths without a personal Desktop location
from pathlib import Path
import sys

# Scripts resolve from their file; notebooks resolve from their working directory.
start = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
ROOT = next((p for p in (start, *start.parents) if (p / "project_config.py").exists()), None)
if ROOT is None:
    raise FileNotFoundError("Open this notebook from inside the project folder.")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from project_config import DATA_DIR, OUTPUT_DIR, TEAM_NAMES, FOCUS_TEAMS, COLORS, save_chart
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

TABLE_DIR = OUTPUT_DIR / "v1"
TABLE_DIR.mkdir(parents=True, exist_ok=True)
BREAK_ROUND = 15
def save_table(frame, filename):
    frame.to_csv(TABLE_DIR / filename, index=False, encoding="utf-8-sig")

# %% Load inputs and translate team names
# Parse dates strictly; reject unknown names instead of creating missing team labels.
results = pd.read_csv(DATA_DIR / "kleague1_2026_round01-30_results_weather.csv", encoding="utf-8-sig")
stats = pd.read_csv(DATA_DIR / "kleague1_2026_round01-30_teamstats_raw.csv", encoding="utf-8-sig")
results["game_date"] = pd.to_datetime(results["game_date"], errors="raise")
for column in ("home_team", "away_team"):
    assert results[column].isin(TEAM_NAMES).all(), f"Unknown team in {column}"
    results[column] = results[column].map(TEAM_NAMES)
assert stats["team"].isin(TEAM_NAMES).all()
stats["team"] = stats["team"].map(TEAM_NAMES)


# %% Validate the complete R1-30 snapshot
# Require 180 fixtures and 360 team rows. Recheck saved official audits against the current inputs; this is not a fresh website check.
assert len(results) == 180 and len(stats) == 360
assert set(results.game_id) == set(range(1,181)) == set(stats.game_id)
assert not results.duplicated("game_id").any()
assert not stats.duplicated(["game_id","team"]).any()
assert results.groupby("round").size().eq(6).all()
assert results.loc[results["round"] <= 15,"game_date"].max() == pd.Timestamp("2026-05-17")
assert results.loc[results["round"] >= 16,"game_date"].min() == pd.Timestamp("2026-07-04")
late = results.loc[results.game_id == 129].iloc[0]
assert late["round"] == 22 and late.game_date == pd.Timestamp("2026-09-27") and late["home_득점"] == late["away_득점"] == 0
official = pd.read_csv(DATA_DIR / "official_totals_reconciliation.csv")
score_audit = pd.read_csv(DATA_DIR / "official_score_reconciliation.csv")
assert official.loc[official.metric != "GOAL_CNT","matches"].all()
assert len(score_audit) == 360 and score_audit["matches"].all()
for audit in official.itertuples(index=False):
    current_total = stats.loc[stats.team_id == audit.team_id, audit.metric].sum()
    assert np.isclose(current_total, audit.computed)
for audit in score_audit.itertuples(index=False):
    current_game = results.loc[results.game_id == audit.game_id].iloc[0]
    side, other = ("home", "away") if current_game.home_team_id == audit.team_id else ("away", "home")
    assert current_game[f"{side}_득점"] == audit.official_goals_for and current_game[f"{other}_득점"] == audit.official_goals_against
assert stats["ATT_AREA_ENTER"].fillna(0).eq(0).all()
METRIC_MAP = {"SHOT":"shots", "SHOT_ON_TARGET":"shots_on_target", "PASS":"pass_attempts", "PASS_ACC":"completed_passes", "EXTRA_ATT_AND_KEYPASS":"provider_key_passes", "PASS_F_CA_DEG":"forward_pass_attempts", "ATT_AREA_PASS":"attacking_area_pass_attempts", "ATT_AREA_PASS_SUCCESS":"completed_attacking_area_passes"}
assert stats[list(METRIC_MAP)].notna().all().all() and stats[list(METRIC_MAP)].ge(0).all().all()
assert stats.PASS_ACC.le(stats.PASS).all() and stats.SHOT_ON_TARGET.le(stats.SHOT).all()
print("180 fixtures; 360 team-match rows; 552 comparable stat totals and 360 score observations reconciled.")


# %% Build one row per team per match
# Use final-score goals, compute W/D/L and points, and join own/opponent statistics with one-to-one validation.
pieces = []
for side, other in [("home","away"),("away","home")]:
    part = results[["season","round","game_id","game_date",f"{side}_team",f"{other}_team",f"{side}_득점",f"{other}_득점"]].copy()
    part = part.rename(columns={f"{side}_team":"team",f"{other}_team":"opponent",f"{side}_득점":"goals_for",f"{other}_득점":"goals_against"})
    part["side"] = side
    pieces.append(part)
matches = pd.concat(pieces, ignore_index=True)
for name, condition in {"wins":matches.goals_for > matches.goals_against,"draws":matches.goals_for == matches.goals_against,"losses":matches.goals_for < matches.goals_against}.items():
    matches[name] = condition.astype(int)
matches["points"] = 3 * matches.wins + matches.draws
matches["period"] = np.where(matches["round"] <= BREAK_ROUND,"Before","After")
matches["postponed_fixture"] = matches.game_id.eq(129)
selected = stats[["game_id","team","side"] + list(METRIC_MAP)].rename(columns=METRIC_MAP)
matches = matches.merge(selected, on=["game_id","team","side"], validate="one_to_one", how="left")
opponent = selected[["game_id","team","shots","shots_on_target"]].rename(columns={"team":"opponent","shots":"opponent_shots","shots_on_target":"opponent_shots_on_target"})
matches = matches.merge(opponent, on=["game_id","opponent"], validate="one_to_one", how="left")
assert len(matches) == 360 and matches[list(METRIC_MAP.values()) + ["opponent_shots"]].notna().all().all()
assert matches.groupby(["team","period"]).size().eq(15).all()
save_table(matches, "01_team_match_dataset.csv")


# Exclude unsupported fields; all-zero does not establish a meaningful measurement.
for field in ["ATT_AREA_ENTER", "EXTRA_ATT_AND_KEYPASS_ACC", "CONTROL_UNDER_PRESSURE"]:
    assert stats[field].eq(0).all(), f"Reassess the source definition for {field}."
# Both halves must contain 15 matches for every club, including postponed game 129.
coverage = matches.groupby(["team", "period"]).size().unstack().reindex(columns=["Before", "After"])
assert coverage.eq(15).all().all()
display(coverage)
print("Saved outputs/v1/01_team_match_dataset.csv. Raw files were not modified.")
