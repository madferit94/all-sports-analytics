"""Check generated tables and consequential findings against the frozen snapshot."""
from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd

# Resolve the project independently of the terminal's working directory.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project_config import OUTPUT_DIR

# Every public aggregate reference maps to a reproducible output, not a manual table.
manifest = json.loads((ROOT / 'results/manifest.json').read_text(encoding='utf-8'))
for item in manifest:
    reference = pd.read_csv(ROOT / item['reference'])
    actual = pd.read_csv(OUTPUT_DIR / item['output'])
    pd.testing.assert_frame_equal(actual, reference, check_dtype=False, atol=1e-10, rtol=1e-10)

matches = pd.read_csv(OUTPUT_DIR / 'v1/01_team_match_dataset.csv')
assert len(matches) == 360
assert not matches.duplicated(['game_id', 'team']).any()
assert matches.groupby(['team', 'period']).size().eq(15).all()
assert matches.groupby(['team', 'round']).size().eq(1).all()
assert matches.goals_for.sum() == matches.goals_against.sum()
late = matches.loc[matches.game_id == 129]
assert len(late) == 2 and late['round'].eq(22).all() and late.period.eq('After').all()
assert pd.to_datetime(late.game_date).eq(pd.Timestamp('2026-09-27')).all()

# Independently recompute score-based totals from the fixture file.
from project_config import DATA_DIR, TEAM_NAMES
raw = pd.read_csv(DATA_DIR / 'kleague1_2026_round01-30_results_weather.csv')
standings = pd.read_csv(OUTPUT_DIR / 'v2/06_standings_round30.csv').set_index('team')
for source_name, team in TEAM_NAMES.items():
    home = raw.loc[raw.home_team == source_name]
    away = raw.loc[raw.away_team == source_name]
    scored = home['home_득점'].sum() + away['away_득점'].sum()
    conceded = home['away_득점'].sum() + away['home_득점'].sum()
    points = (3 * (home['home_득점'] > home['away_득점']).sum()
              + (home['home_득점'] == home['away_득점']).sum()
              + 3 * (away['away_득점'] > away['home_득점']).sum()
              + (away['away_득점'] == away['home_득점']).sum())
    assert standings.loc[team, 'goals_for'] == scored
    assert standings.loc[team, 'goals_against'] == conceded
    assert standings.loc[team, 'points'] == points

# Check the three substantive claims from match-grain data.
summary = pd.read_csv(OUTPUT_DIR / 'v3/16_focus_period_summary.csv').set_index(['team', 'period'])
assert summary.loc[('Anyang', 'Before'), 'goals_against'] == 16
assert summary.loc[('Anyang', 'After'), 'goals_against'] == 31
assert summary.loc[('Daejeon', 'Before'), 'scoreless_matches'] == 7
assert summary.loc[('Daejeon', 'After'), 'scoreless_matches'] == 2
assert summary.loc[('Jeju', 'Before'), 'losses'] == 7
assert summary.loc[('Jeju', 'After'), 'losses'] == 1
jeju = matches.loc[matches.team == 'Jeju'].groupby('period').mean(numeric_only=True)
assert jeju.loc['After', 'shots_on_target'] < jeju.loc['Before', 'shots_on_target']
assert jeju.loc['After', 'opponent_shots_on_target'] > jeju.loc['Before', 'opponent_shots_on_target']
trials = pd.read_csv(OUTPUT_DIR / 'v4/12_focus_leave_one_match_out.csv')
assert len(trials) == 720 and trials.groupby(['team', 'metric']).size().eq(30).all()
assert np.isfinite(trials.delta_after_exclusion).all()
print(f'Passed {len(manifest)} aggregate-table regressions, score reconciliation and report-claim checks.')
