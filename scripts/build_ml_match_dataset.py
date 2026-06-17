from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "data" / "processed"


MATCHES_PATH = PROCESSED / "fotmob_match_ids_extracted.csv"
STATS_PATH = PROCESSED / "fotmob_statistics_long.csv"
TRANSFERMARKT_PATH = PROCESSED / "transfermarkt_country_profile.csv"
OUTPUT_PATH = PROCESSED / "ml_match_dataset.csv"

ROLLING_WINDOWS = (5, 10)


def normalize_team_name(value: object) -> str:
    if pd.isna(value):
        return ""
    text = unicodedata.normalize("NFKC", str(value)).strip()
    return re.sub(r"\s+", " ", text)


def to_number(value: object) -> float:
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value)
    text = str(value).replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group(0)) if match else np.nan


def safe_stat_key(row: pd.Series) -> str:
    group = str(row.get("group_key") or row.get("group_title") or "stat")
    stat = str(row.get("stat_key") or row.get("stat_title") or "value")
    raw = f"{group}_{stat}".lower()
    return re.sub(r"[^a-z0-9]+", "_", raw).strip("_")


def load_base_matches() -> pd.DataFrame:
    matches = pd.read_csv(MATCHES_PATH)
    matches["date"] = pd.to_datetime(matches["date"])
    matches["home_team"] = matches["home_team"].map(normalize_team_name)
    matches["away_team"] = matches["away_team"].map(normalize_team_name)
    matches = matches.dropna(subset=["home_score", "away_score"])
    matches["fotmob_match_id"] = pd.to_numeric(matches["fotmob_match_id"], errors="coerce")
    matches = matches.dropna(subset=["fotmob_match_id"]).copy()
    matches["fotmob_match_id"] = matches["fotmob_match_id"].astype("int64")
    return matches.sort_values(["date", "fotmob_match_id"]).reset_index(drop=True)


def build_stats_wide() -> pd.DataFrame:
    stats = pd.read_csv(STATS_PATH)
    stats = stats[stats["period"].fillna("").str.lower().eq("all")].copy()
    stats["stat_feature"] = stats.apply(safe_stat_key, axis=1)
    stats["home_value_num"] = stats["home_value"].map(to_number)
    stats["away_value_num"] = stats["away_value"].map(to_number)

    home = stats[["fotmob_match_id", "stat_feature", "home_value_num"]].rename(
        columns={"home_value_num": "value"}
    )
    away = stats[["fotmob_match_id", "stat_feature", "away_value_num"]].rename(
        columns={"away_value_num": "value"}
    )

    home_wide = home.pivot_table(
        index="fotmob_match_id", columns="stat_feature", values="value", aggfunc="first"
    ).add_prefix("stat_for_")
    away_wide = away.pivot_table(
        index="fotmob_match_id", columns="stat_feature", values="value", aggfunc="first"
    ).add_prefix("stat_for_")
    return home_wide.reset_index(), away_wide.reset_index()


def build_team_match_rows(matches: pd.DataFrame) -> pd.DataFrame:
    home_stats, away_stats = build_stats_wide()

    home = matches.copy()
    home["team"] = home["home_team"]
    home["opponent"] = home["away_team"]
    home["is_home"] = 1
    home["goals_for"] = home["home_score"]
    home["goals_against"] = home["away_score"]
    home = home.merge(home_stats, on="fotmob_match_id", how="left")

    away = matches.copy()
    away["team"] = away["away_team"]
    away["opponent"] = away["home_team"]
    away["is_home"] = 0
    away["goals_for"] = away["away_score"]
    away["goals_against"] = away["home_score"]
    away = away.merge(away_stats, on="fotmob_match_id", how="left")

    team_rows = pd.concat([home, away], ignore_index=True)
    team_rows["team"] = team_rows["team"].map(normalize_team_name)
    team_rows["opponent"] = team_rows["opponent"].map(normalize_team_name)
    team_rows["goal_diff"] = team_rows["goals_for"] - team_rows["goals_against"]
    team_rows["points"] = np.select(
        [team_rows["goal_diff"].gt(0), team_rows["goal_diff"].eq(0)], [3, 1], default=0
    )
    team_rows["won"] = team_rows["goal_diff"].gt(0).astype(int)
    team_rows["drawn"] = team_rows["goal_diff"].eq(0).astype(int)
    team_rows["lost"] = team_rows["goal_diff"].lt(0).astype(int)
    return team_rows.sort_values(["team", "date", "fotmob_match_id", "is_home"])


def add_rolling_features(team_rows: pd.DataFrame) -> pd.DataFrame:
    base_cols = ["goals_for", "goals_against", "goal_diff", "points", "won", "drawn", "lost"]
    stat_cols = [c for c in team_rows.columns if c.startswith("stat_for_")]
    rolling_cols = base_cols + stat_cols

    pieces = []
    for _, group in team_rows.groupby("team", sort=False):
        group = group.sort_values(["date", "fotmob_match_id"]).copy()
        shifted = group[rolling_cols].shift(1)
        for window in ROLLING_WINDOWS:
            rolled = shifted.rolling(window=window, min_periods=1).mean()
            rolled.columns = [f"roll{window}_{c}" for c in rolled.columns]
            group = pd.concat([group, rolled], axis=1)
        pieces.append(group)
    return pd.concat(pieces, ignore_index=True)


def load_transfermarkt_features() -> pd.DataFrame:
    tm = pd.read_csv(TRANSFERMARKT_PATH)
    tm["team"] = tm["country"].map(normalize_team_name)
    keep = [
        "team",
        "squad_size",
        "average_age",
        "fifa_world_ranking",
        "total_market_value_eur",
    ]
    tm = tm[keep].copy()
    for col in keep[1:]:
        tm[col] = pd.to_numeric(tm[col], errors="coerce")
    return tm


def build_match_dataset() -> pd.DataFrame:
    matches = load_base_matches()
    team_rows = add_rolling_features(build_team_match_rows(matches))
    tm = load_transfermarkt_features()

    feature_cols = [c for c in team_rows.columns if c.startswith("roll")]
    home_features = team_rows[team_rows["is_home"].eq(1)][
        ["fotmob_match_id", "team", *feature_cols]
    ].rename(columns={"team": "home_team"})
    away_features = team_rows[team_rows["is_home"].eq(0)][
        ["fotmob_match_id", "team", *feature_cols]
    ].rename(columns={"team": "away_team"})

    home_features = home_features.rename(columns={c: f"home_{c}" for c in feature_cols})
    away_features = away_features.rename(columns={c: f"away_{c}" for c in feature_cols})

    dataset = matches.merge(home_features, on=["fotmob_match_id", "home_team"], how="left")
    dataset = dataset.merge(away_features, on=["fotmob_match_id", "away_team"], how="left")

    home_tm = tm.rename(columns={c: f"home_tm_{c}" for c in tm.columns if c != "team"})
    away_tm = tm.rename(columns={c: f"away_tm_{c}" for c in tm.columns if c != "team"})
    dataset = dataset.merge(home_tm, left_on="home_team", right_on="team", how="left").drop(
        columns=["team"]
    )
    dataset = dataset.merge(away_tm, left_on="away_team", right_on="team", how="left").drop(
        columns=["team"]
    )

    for col in ["squad_size", "average_age", "fifa_world_ranking", "total_market_value_eur"]:
        h = f"home_tm_{col}"
        a = f"away_tm_{col}"
        dataset[f"diff_tm_{col}"] = dataset[h] - dataset[a]

    for col in feature_cols:
        dataset[f"diff_{col}"] = dataset[f"home_{col}"] - dataset[f"away_{col}"]

    dataset["target"] = np.select(
        [dataset["home_score"].gt(dataset["away_score"]), dataset["home_score"].eq(dataset["away_score"])],
        ["home_win", "draw"],
        default="away_win",
    )
    return dataset.sort_values(["date", "fotmob_match_id"]).reset_index(drop=True)


def main() -> None:
    dataset = build_match_dataset()
    dataset.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"saved: {OUTPUT_PATH}")
    print(f"shape: {dataset.shape}")
    print(dataset["target"].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
