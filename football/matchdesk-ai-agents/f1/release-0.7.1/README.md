## MatchLab 0.19.1 / F1 0.7.1 — Conditional metric queries

Query 30 metrics in Korean/English. Single-driver values use cards; multiple metrics have separate tables/charts. Selected-GP queries support lap ranges, pit-lap exclusions, numeric thresholds, top N and sort order, with visible applied conditions. Deterministic analysis without API calls.

## MatchLab 0.19.0 / F1 0.7.0 — Natural-language charts

Enter driver names and a metric for the selected GP to generate lap-time lines or comparison bars. Korean and English supported. A deterministic local parser calculates saved records without AI API calls. Unsupported events, dates and custom filters return guidance.

## MatchLab 0.18.1 / F1 0.6.1

Matched 13 GP files from the DHL-derived f1pits archive; filled 276 missing stationary stop times. Existing OpenF1 values are preserved; 37 disagreements logged and one unmatched row excluded. Coverage counts distinguish partial averages. Completed-race records only; prediction models unchanged. Participant confirmation pending.

## MatchLab 0.18.0 / F1 0.6.0 — Driver metrics and contextual help

Select a driver and category to inspect race results, lap pace, pit records and pre-race model inputs. Click each metric label for its definition, aggregation and interpretation limits. Upcoming races show prediction metrics only. Long status and tyre labels wrap while numeric values remain readable.

245 separate headless Edge checks passed at 320, 375, 768 and 1280px in Korean and English. Participant confirmation pending. Earlier release notes are preserved below.
## 0.17.2 / F1 0.5.2 — Slower circuit playback

Completed races now use recorded real-time playback at 1×, replacing the previous entire-race-in-60-seconds compression. Shared speed offers 0.25×, 0.5×, 1×, 2×, 4×, 10×, 30×, 60×. Upcoming forecasts use a labeled 180-second illustration. Earlier speed descriptions below are release history. Previous versions preserved; user verification pending.

# MatchLab F1 0.5.2 · all drivers and selected-driver progress

Maps show all22 entries by default. Driver selection highlights an entrant and updates its progress panel. A paused selected-only view is retained; Play restores all-driver rendering without losing the selected records.

Progress records use only data available at the current cursor: position, laps, tyres, pit entries and completed lap durations. Charts exclude later events. Pit-lane duration is not stationary stop duration. Upcoming races expose prediction values only, not fabricated recorded statistics.

Existing completed16/upcoming7 maps, models, coordinate/reconstruction labels and retrospective forecast limitations are preserved. User verification pending; not pushed to GitHub.


Shared speed: prediction motion uses the completed race lap count. Both maps share one cursor and 1×/2×/4× speed. Prediction remains an illustration, not actual per-lap forecasting.



