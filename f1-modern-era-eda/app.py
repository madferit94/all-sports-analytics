from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="F1 EDA Dashboard", layout="wide")

DATA_PATH = Path(__file__).resolve().parent / "data" / "processed" / "f1_race_results_clean.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, parse_dates=["race_date"])

df = load_data()

st.title("F1 EDA Dashboard")
st.caption(f"Loaded: {DATA_PATH.name} | Shape: {df.shape}")

# -------------------------
# Sidebar filters
# -------------------------
st.sidebar.header("Filters")

min_season = int(df["season"].min())
max_season = int(df["season"].max())
season_range = st.sidebar.slider("Season range", min_season, max_season, (2000, max_season))

df_f = df[(df["season"] >= season_range[0]) & (df["season"] <= season_range[1])].copy()

gps = sorted(df_f["grand_prix"].dropna().unique().tolist())
selected_gps = st.sidebar.multiselect("Grand Prix", gps, default=[])
if selected_gps:
    df_f = df_f[df_f["grand_prix"].isin(selected_gps)]

teams = sorted(df_f["team"].dropna().unique().tolist())
selected_teams = st.sidebar.multiselect("Team", teams, default=[])
if selected_teams:
    df_f = df_f[df_f["team"].isin(selected_teams)]

drivers = sorted(df_f["driver"].dropna().unique().tolist())
selected_drivers = st.sidebar.multiselect("Driver", drivers, default=[])
if selected_drivers:
    df_f = df_f[df_f["driver"].isin(selected_drivers)]

# -------------------------
# KPIs
# -------------------------
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Filtered rows", f"{len(df_f):,}")
with k2:
    st.metric("Races (unique GP)", f"{df_f['grand_prix'].nunique():,}")
with k3:
    st.metric("Drivers", f"{df_f['driver'].nunique():,}")
with k4:
    st.metric("Avg points", f"{df_f['points'].mean():.2f}")

# -------------------------
# Preview
# -------------------------
st.divider()
st.subheader("Preview (filtered)")
st.dataframe(df_f.head(50), width="stretch")

# -------------------------
# Chart 1: DNF rate by season
# -------------------------
st.divider()
st.subheader("DNF rate by season")

dnf_rate = (
    df_f.groupby("season", as_index=False)["is_dnf"]
    .mean()
    .sort_values("season")
)

st.line_chart(dnf_rate, x="season", y="is_dnf")

# -------------------------
# Chart 2: Positions gained (Grid - Finish)
# -------------------------
st.divider()
st.subheader("Positions gained (Grid - Finish)")

pos_gain = (df_f["grid"] - df_f["finish_position_num"]).dropna()
st.write("Positive = gained positions, Negative = lost positions")

# Histogram style with Streamlit built-in chart:
st.bar_chart(pos_gain.value_counts().sort_index())

# -------------------------
# Chart 3: Top Drivers / Teams by total points (filtered)
# -------------------------
st.divider()
st.subheader("Top Drivers / Teams by Total Points (filtered)")

colA, colB = st.columns(2)

with colA:
    top_drivers = (
        df_f.groupby("driver", as_index=False)["points"]
        .sum()
        .sort_values("points", ascending=False)
        .head(15)
    )
    st.dataframe(top_drivers, width="stretch")

with colB:
    top_teams = (
        df_f.groupby("team", as_index=False)["points"]
        .sum()
        .sort_values("points", ascending=False)
        .head(15)
    )
    st.dataframe(top_teams, width="stretch")