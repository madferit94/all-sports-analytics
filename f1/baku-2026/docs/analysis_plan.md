# Analysis design and publication gate

[한국어](analysis_plan.ko.md) · [Project](../README.md)

## Question → source → metric

**Question:** How did Russell–Verstappen's gap and paired pace evolve around race neutralisation, with the final Top 10 providing context?

Use `laps`, `drivers`, `stints`, `pit`, `race_control`, `session_result`, `position`, `intervals`, and `weather`; use `location` only for the replay. Preserve all 22 drivers before selecting the final Top 10. Weather describes context, not a causal adjustment by itself.

The primary pace metric is `median(lap_duration_VER − lap_duration_RUS)` over eligible same-numbered laps. Positive values mean Russell was quicker. Report n, median, and IQR (middle 50% spread). Compute paired differences before summarising; do not subtract two unpaired medians.

## Validate → qualify → compare

1. Validate IDs, timestamps, unique driver-lap keys, nulls, positive durations, and join cardinality. Match stints by inclusive lap ranges; retain missing or ambiguous matches. Compare estimated lap ends with the next lap start before using temporal overlap.
2. Define SC/VSC/RED periods from in-race messages. Review SC restart candidates manually; “in this lap” is an advance notice, not an exact withdrawal timestamp. Reset flag state at session start. Record conflicting simultaneous YELLOW/CLEAR messages and unmatched clear events for review; do not silently choose a convenient order.
3. Exclude lap 1, missing/invalid laps, pit in/out laps, neutralised laps, and restart laps. Apply exclusions when **either driver's** lap overlaps a relevant period, using UTC intervals. Conservative yellow-flag filtering may exclude any sector overlap but does not prove that the particular driver was affected; a flag sector is not necessarily one of the three timing sectors.
4. Primary windows: eligible laps after L1 before the first SC; eligible laps after the second restart, excluding its restart lap, through the finish. The short interval between the two SCs is context only. The old L21–30/L41–50 windows remain an exploratory secondary comparison; they are not the primary analysis.
5. Check boundary sensitivity at ±1 second; compare conservative yellow exclusions with inclusion. Five pairs is a display threshold, not a statistical confidence guarantee. Leave `pace_eligible` null until the rules have been applied and reviewed.
6. For timing joins, use the latest **past** sample with a candidate eight-second tolerance, then inspect actual coverage. Never use future data to fill a prior state. If exploring traffic, gap-to-car-ahead ≤1 second is a proximity proxy; compare 0.5/1/2-second thresholds and do not call it proof of blocking.

## Story → interpretation → limitation

The final publication should contain three panels: final Top 10 context, the main pair's published gap with reviewed SC/pit events, and eligible paired pace with sample counts/spread. A replay is a supporting visual, not proof of tyre strategy superiority.

Do not infer independent tyre effects, fuel-corrected pace, or a counterfactual winner. A fresh stint or pit-lane passage alone is not evidence of fresh tyres. No model or significance test is needed before the descriptive comparison is valid.

**Current gate:** collection, raw preservation, base-table validation, and exploratory rendering are complete. Temporal eligibility, verified restart boundaries, sensitivity results, and a final public pace conclusion are outstanding. The existing charts explicitly remain exploratory.
