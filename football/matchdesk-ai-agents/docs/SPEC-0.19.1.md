# Conditional F1 queries / 조건별 지표 조회

MatchLab 0.19.1 / F1 0.7.1

- User clarified: natural-language queries must support conditions, not only metric names.
- 30 existing computed metric labels/aliases supported in KO/EN, plus lap-time series. Up to four drivers and four metrics; unsupported residual text returns guidance.
- Single-driver numeric/status output uses a card. Multiple metric units are never pooled on one axis. Multiple drivers use labeled bars and an accessible values table. Signed values retain direction around zero.
- Selected-GP inclusive lap range 1–200, start <= end. Applied only to lap-derived metrics (duration, sectors, speed-trap and valid lap count).
- Pit-lap exclusion removes recorded pit-entry laps and is_pit_out_lap. Explicit Korean pit-out exclusion removes only pit-out laps. Safety Car effects are not inferred/removed.
- One numeric metric may have a threshold (<, <=, >, >=), matching unit, top 1–22 and ascending/descending order. Missing records fail numeric predicates; top N excludes missing values. Time/rank defaults lower first; speed/points/probability higher first. Probability thresholds use percentage points.
- Display applied range/exclusion/threshold/order; unknown dates, races, weather and arbitrary filters are not ignored.
- Saved data/model artifacts unchanged. Pure local parser, no LLM, API keys or uploaded-file analysis.
- Tests: 96 manual-arithmetic/parser cases and 80 isolated real-browser cases on KO/EN 320/375/768/1280px PASS. Participant confirmation pending.
- Prior v11/0.19.0 preserved. No GitHub upload requested this turn.

Full localhost integration PASS: selected GP lap-range mean card and top-five speed chart, then existing metrics navigation. Participant confirmation pending.

