# Historical F1 EDA Dashboard

[English](README.md) · [한국어](README.ko.md)

An existing Streamlit dashboard showing season-level DNF labels, grid-to-finish differences, and total points by driver/team. The committed CSV covers **1950–2025**; the current app defaults to 2000 onward and does not enforce a 2016 lower bound.

**Status: preserved dashboard prototype; metric corrections needed.** The deployment link is retained, but live availability was not verified in this review.

- [Dashboard](https://f1-modern-era-eda.streamlit.app/)
- [Application source](app.py)
- [Review: keep and revise](../f1/baku-2026/docs/existing_f1_review.md)
- [New Baku race-context project](../f1/baku-2026)

## Corrections before portfolio use

The input's DNF definition classifies `+N Lap(s)` statuses as DNF. Reliability rates therefore need to be rebuilt. The KPI named Races currently counts distinct GP names; use season + round to count race instances. Positions gained exclude missing finishes and should state their sample coverage. Total points reflect unequal participation and should not be presented as a controlled driver-skill comparison.

The application, CSV, and historical prediction notebooks were preserved. The Baku project adds a separate in-race workflow and does not replace this dashboard.
