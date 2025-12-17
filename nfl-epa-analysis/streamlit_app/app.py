import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# -------------------------------------------------
# Debug (optional)
# -------------------------------------------------
st.write("RUNNING FILE:", str(Path(__file__).resolve()))

# -------------------------------------------------
# App Config
# -------------------------------------------------
st.set_page_config(page_title="NFL Analytics Dashboard", layout="wide")

st.title("🏈 NFL EPA & Win Probability Dashboard")
st.caption("2019–2024 Seasons | Rolling EPA, Matchups")

# -------------------------------------------------
# Paths
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EPA_PARQUET = PROCESSED_DIR / "team_game_features.parquet"
MATCHUPS_CSV = PROCESSED_DIR / "matchups_pre_game_2019_2024_with_clusters.csv"

# -------------------------------------------------
# Loaders
# -------------------------------------------------
@st.cache_data
def load_epa(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)

@st.cache_data
def load_matchups(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    for col in ["home_gameday", "away_gameday"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def compute_repel_label_positions(
    x: np.ndarray,
    y: np.ndarray,
    labels: list[str],
    *,
    x_pad_frac: float = 0.032,
    y_pad_frac: float = 0.045,
    min_above_frac: float = 0.040,
    iters: int = 260,
    step: float = 0.38,
    seed: int = 7,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)

    x = x.astype(float)
    y = y.astype(float)

    x_range = float(np.nanmax(x) - np.nanmin(x))
    y_range = float(np.nanmax(y) - np.nanmin(y))
    x_range = x_range if x_range > 0 else 1.0
    y_range = y_range if y_range > 0 else 1.0

    x_pad = x_pad_frac * x_range
    y_pad = y_pad_frac * y_range

    lx = x + rng.normal(0.0, 0.007 * x_range, size=len(x))
    ly = y + (min_above_frac * y_range) + rng.normal(0.0, 0.004 * y_range, size=len(y))

    floor = y + (min_above_frac * y_range)

    for _ in range(iters):
        moved = False
        for i in range(len(x)):
            for j in range(i + 1, len(x)):
                dx = lx[i] - lx[j]
                dy = ly[i] - ly[j]

                if abs(dx) < x_pad and abs(dy) < y_pad:
                    moved = True

                    push_x = (x_pad - abs(dx)) / x_pad
                    push_y = (y_pad - abs(dy)) / y_pad

                    sx = 1.0 if dx >= 0 else -1.0
                    sy = 1.0 if dy >= 0 else -1.0

                    lx[i] += sx * push_x * step * x_pad
                    lx[j] -= sx * push_x * step * x_pad

                    ly[i] += sy * push_y * step * y_pad
                    ly[j] -= sy * push_y * step * y_pad

        ly = np.maximum(ly, floor)

        if not moved:
            break

    return lx, ly

def pick_first_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None

def clamp01(s: pd.Series) -> pd.Series:
    return s.clip(lower=0.0, upper=1.0)

def prob_tier(p: float) -> str:
    if p >= 0.70:
        return "Very high (>=0.70)"
    if p >= 0.60:
        return "High (0.60–0.70)"
    if p >= 0.50:
        return "Slight (0.50–0.60)"
    if p >= 0.40:
        return "Low (0.40–0.50)"
    return "Very low (<0.40)"

# -------------------------------------------------
# Data
# -------------------------------------------------
df_epa = load_epa(EPA_PARQUET)
df_m = load_matchups(MATCHUPS_CSV)

if df_epa.empty:
    st.error(f"EPA data not found or empty: {EPA_PARQUET}")
    st.stop()

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("Filters")

seasons = sorted(df_epa["season"].unique())
season = st.sidebar.selectbox("Season", seasons, index=len(seasons) - 1)

weeks = sorted(df_epa[df_epa["season"] == season]["week"].unique())
week = st.sidebar.slider("Week (up to)", min(weeks), max(weeks), max(weeks))

always_show_labels = st.sidebar.checkbox("Always show team labels", value=True)
invert_def_axis = st.sidebar.checkbox("Invert defense axis (lower is better)", value=True)

df_epa_f = df_epa[(df_epa["season"] == season) & (df_epa["week"] <= week)].copy()

tab1, tab2, tab3 = st.tabs(["📊 EPA Landscape", "🔮 Win Probability", "📈 Team Momentum"])

# -------------------------------------------------
# Tab 1 — EPA Landscape
# -------------------------------------------------
with tab1:
    st.subheader(f"EPA Landscape — Season {season}, up to Week {week}")
    st.caption("Offense: higher is better | Defense: lower is better (when inverted)")

    latest_week_df = (
        df_epa_f.sort_values("week")
        .groupby("team", as_index=False)
        .tail(1)
        .copy()
    )

    latest_week_df["abs_net_epa_for_size"] = latest_week_df["rolling_net_epa_4"].abs() + 0.1

    # Net EPA tiers (discrete colors for readability)
    def net_tier(v: float) -> str:
        if v >= 0.15:
            return "Elite (>= +0.15)"
        if v >= 0.05:
            return "Strong (+0.05–0.15)"
        if v > -0.05:
            return "Average (-0.05–0.05)"
        if v > -0.15:
            return "Poor (-0.15–-0.05)"
        return "Weak (<= -0.15)"

    latest_week_df["net_epa_tier"] = latest_week_df["rolling_net_epa_4"].apply(net_tier)

    # Distinct tier colors (avoid Elite vs Strong similarity)
    tier_color_map = {
        "Elite (>= +0.15)": "#F2C14E",       # gold
        "Strong (+0.05–0.15)": "#2D9CDB",    # bright blue
        "Average (-0.05–0.05)": "#BDBDBD",   # grey
        "Poor (-0.15–-0.05)": "#F2994A",     # orange
        "Weak (<= -0.15)": "#EB5757",        # red
    }

    fig = px.scatter(
        latest_week_df,
        x="rolling_off_epa_4",
        y="rolling_def_epa_4",
        color="net_epa_tier",
        color_discrete_map=tier_color_map,
        size="abs_net_epa_for_size",
        hover_name="team",
        hover_data={
            "team": True,
            "rolling_off_epa_4": ":.3f",
            "rolling_def_epa_4": ":.3f",
            "rolling_net_epa_4": ":.3f",
            "net_epa_tier": True,
            "abs_net_epa_for_size": False,
        },
        title="Offensive vs Defensive EPA (Rolling 4-Game Avg)",
        labels={
            "rolling_off_epa_4": "Offensive EPA (higher is better)",
            "rolling_def_epa_4": "Defensive EPA (lower is better)",
            "net_epa_tier": "Net EPA Tier",
        },
        height=650,
    )

    if invert_def_axis:
        fig.update_yaxes(autorange="reversed")

    fig.add_hline(y=0, line_dash="dot", opacity=0.35)
    fig.add_vline(x=0, line_dash="dot", opacity=0.35)

    # Hide built-in text; we will add a separate repelled text layer
    fig.update_traces(mode="markers", selector=dict(type="scatter"))

    if always_show_labels:
        x_pts = latest_week_df["rolling_off_epa_4"].to_numpy(dtype=float)
        y_pts = latest_week_df["rolling_def_epa_4"].to_numpy(dtype=float)
        teams = latest_week_df["team"].astype(str).tolist()

        lx, ly = compute_repel_label_positions(
            x_pts,
            y_pts,
            teams,
            x_pad_frac=0.032,
            y_pad_frac=0.048,
            min_above_frac=0.045,
            iters=280,
            step=0.40,
            seed=7,
        )

        fig.add_trace(
            go.Scatter(
                x=lx,
                y=ly,
                mode="text",
                text=teams,
                textposition="middle center",
                textfont=dict(size=12),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    fig.update_layout(
        legend=dict(
            title="Net EPA Tier",
            itemsizing="constant",
        )
    )

    st.plotly_chart(fig, width="stretch")

# -------------------------------------------------
# Tab 2 — Win Probability
# -------------------------------------------------
with tab2:
    st.subheader("Win Probability (Pre-game)")
    st.caption("Home win probability predicted before the game (from Notebook 04 output).")

    if df_m.empty:
        st.warning(f"Matchups file not found or empty: {MATCHUPS_CSV}")
        st.stop()

    if ("season" not in df_m.columns) or ("week" not in df_m.columns):
        st.error("Matchups CSV must contain 'season' and 'week' columns.")
        st.stop()

    df_m_s = df_m[df_m["season"] == season].copy()
    if df_m_s.empty:
        st.info("No matchups found for the selected season.")
        st.stop()

    weeks_m = sorted(df_m_s["week"].unique())
    week_m = st.slider("Week (exact)", min(weeks_m), max(weeks_m), min(week, max(weeks_m)))
    games = df_m_s[df_m_s["week"] == week_m].copy()
    if games.empty:
        st.info("No games found for the selected week.")
        st.stop()

    prob_col = pick_first_col(games, ["pred_home_win_prob", "home_win_prob", "home_win_probability"])
    if prob_col is None:
        st.warning("No win-probability column found (expected: pred_home_win_prob).")
        st.write("Columns (prob/pred related):", [c for c in games.columns if ("pred" in c.lower()) or ("prob" in c.lower())])
        st.dataframe(games.head(50), width="stretch")
        st.stop()

    games[prob_col] = pd.to_numeric(games[prob_col], errors="coerce")
    games[prob_col] = clamp01(games[prob_col].fillna(0.5))

    date_col = pick_first_col(games, ["home_gameday", "away_gameday"])

    home_team_col = pick_first_col(games, ["home_team", "home_home_team"])
    away_team_col = pick_first_col(games, ["away_team", "home_away_team"])

    if home_team_col is None or away_team_col is None:
        st.error("Could not find home/away team columns in matchups CSV.")
        st.stop()

    # Standardize matchup label: HOME vs AWAY (fixed order)
    games["matchup"] = games[home_team_col].astype(str) + " vs " + games[away_team_col].astype(str)
    games["home_win_prob_pct"] = (games[prob_col] * 100).round(1)
    games["tier"] = games[prob_col].apply(prob_tier)

    show_cols = []
    if date_col is not None:
        show_cols.append(date_col)
    show_cols += [home_team_col, away_team_col, prob_col, "home_win_prob_pct", "tier"]

    for c in ["home_home_score", "home_away_score", "home_home_win", "home_win"]:
        if c in games.columns and c not in show_cols:
            show_cols.append(c)

    st.dataframe(games[show_cols].sort_values(prob_col, ascending=False), width="stretch")

    # Distinct tier colors for bar chart (strong separation)
    prob_tier_colors = {
        "Very high (>=0.70)": "#27AE60",     # green
        "High (0.60–0.70)": "#2D9CDB",       # blue
        "Slight (0.50–0.60)": "#F2C14E",     # gold
        "Low (0.40–0.50)": "#F2994A",        # orange
        "Very low (<0.40)": "#EB5757",       # red
    }

    fig_prob = px.bar(
        games.sort_values(prob_col, ascending=True),
        x=prob_col,
        y="matchup",
        color="tier",
        color_discrete_map=prob_tier_colors,
        orientation="h",
        title="Home Win Probability (sorted)",
        labels={prob_col: "Probability", "matchup": "Matchup", "tier": "Tier"},
        height=650,
    )
    fig_prob.update_layout(legend_title_text="Tier")
    st.plotly_chart(fig_prob, width="stretch")

# -------------------------------------------------
# Tab 3 — Team Momentum
# -------------------------------------------------
with tab3:
    st.subheader("Team Momentum Tracker")

    teams = sorted(df_epa_f["team"].unique())
    team_selected = st.selectbox("Team", teams)

    team_df = df_epa_f[df_epa_f["team"] == team_selected].sort_values("week")

    fig_m = px.line(
        team_df,
        x="week",
        y=["rolling_off_epa_4", "rolling_def_epa_4", "rolling_net_epa_4"],
        markers=True,
        title=f"{team_selected} — EPA Momentum ({season})",
        labels={"value": "EPA", "variable": "Metric", "week": "Week"},
        height=450,
    )
    st.plotly_chart(fig_m, width="stretch")

    with st.expander("View raw rows"):
        st.dataframe(team_df.tail(30), width="stretch")