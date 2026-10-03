# Data dictionary

[한국어](data_dictionary.ko.md)

| Table/field | Grain and meaning | Important limit |
|---|---|---|
| `laps` / `analysis_lap_base` | One session–driver–lap row; seconds for `lap_duration` | Seven full-field durations are missing. |
| `drivers` | One session–driver record | Use session-specific car numbers. |
| `session_result` / `top10_drivers` | One classified driver; final position and published gaps | Final Top 10 selection excludes nonfinishers; not a reliability sample. |
| `stints` | One driver tyre stint with inclusive lap bounds | Use `tyre_age_at_start`; a new stint need not mean new tyres. |
| `tyre_age_start_lap_est` | Stint-start age + current lap − stint-start lap | Derived estimate; retain missing/ambiguous matches. |
| `pit` / `has_pit_lane_record` | Pit-lane activity / whether a lap has such a record | Passage through the lane does not prove a tyre change. |
| `race_control_events` | Every original notice, including before/after race | Notice lap number is not a driver's exact affected lap. |
| `race_control_during_race` | Notices between session start/finish | A message's absence is not general proof no incident occurred. |
| `safety_car_boundary_candidates` | Deployment + advance return notice + next leader-lap start | Candidate boundaries require restart review. |
| `intervals` | Time-stamped timing gaps; seconds when numeric | May include missing values or lap-deficit text; do not coerce that to zero. |
| `position` | Time-stamped classified position | Not starting-grid results. |
| `location` | Time-stamped arbitrary Cartesian x/y/z samples | Approximate track progress, not precise racing lines or time gaps. |
| `weather` | Session weather samples | Context; not a causal control automatically. |
| `lap_start_utc` / `lap_end_est_utc` | Parsed start / start plus lap duration | Compare with next lap start before applying interval overlap. |
| `pace_eligible` | Nullable final comparison flag | Intentionally blank while temporal review is pending. |
| `race_control_review` | Review state for the lap | `PENDING_TIME_INTERVAL_REVIEW` is not an eligible lap. |

Raw filenames retain request filters. CSVs use UTF-8 BOM. Manifests retain URLs, row counts, SHA-256 hashes, known retrieval timestamps, and snapshot-reuse status. Unknown original retrieval timestamps stay null.
