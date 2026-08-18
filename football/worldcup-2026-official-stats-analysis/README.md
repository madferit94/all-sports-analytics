# FIFA World Cup 2026 Official Stats Analysis

This project contains descriptive football analytics notebooks built from team-level FIFA Match Centre data for the 2026 FIFA World Cup.

## Notebooks

1. `01_field_tilt_proxy_analysis.ipynb` - Field Tilt Proxy and shot creation efficiency.
2. `02_champion_profile_analysis.ipynb` - Champion profile descriptive rankings.
3. `03_progression_quality_analysis.ipynb` - Territory and line-break progression quality.
4. `04_final_third_zone_dominance_mplsoccer.ipynb` - Final-third route and zone dominance with mplsoccer.
5. `05_off_ball_movement_analysis.ipynb` - Offers to Receive and reception access.
6. `06_Possession_vs_Directness_Analysis_fixed.ipynb` - Possession style vs direct final-third access.
7. `07_reception_to_shot_conversion_analysis.ipynb` - Reception-to-shot and box finishing conversion.
8. `08_defensive_shot_suppression_analysis.ipynb` - Defensive shot suppression proxy.

## Data

The notebooks expect the cleaned input CSV at:

`data/fifa_worldcup_2026/site_scrape/site_official_stats_team_wide_flagged.csv`

The raw/cleaned data file is not included in this upload. Add it locally if you want to rerun the notebooks.

## Metric Notes

- Field Tilt Proxy = team final-third entries / both teams' final-third entries x 100.
- Final-third Directness = final-third entries / completed passes x 100.
- Reception Access = receptions between midfield/defensive lines + receptions in behind.
- Entry-to-Shot Conceded Rate = shots conceded / opponent final-third entries conceded x 100.

These are descriptive analytical proxies unless the metric is directly provided by FIFA.

## Important Caveats

- Belgium vs Egypt is excluded from full-stat analyses because FIFA provided only Live Statistics for that match.
- Match counts differ from 3 to 8, so smaller samples may be more volatile.
- xG, shot location, game state, and opponent strength are not controlled.
- Rankings are descriptive, not causal.

## Source

FIFA Match Centre, full FIFA Official Stats only.
