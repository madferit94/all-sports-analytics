# V3 learning walkthrough

[한국어](v3_walkthrough.ko.md)

**Goal:** Did a close finish imply comparable pace throughout the race? Follow this question without starting with modeling.

1. Read the published timing-gap curve. Locate SC and pit records on the same clock. Pit passage is not automatically a tyre change.
2. Read `driver_lap_exclusions.csv`: one driver–lap row, start/end timing, context, and explicit exclusion reasons.
3. Read `paired_lap_audit.csv`: one lap number with RUS/VER duration and eligibility. If either driver is excluded, discard the pair. SC boundaries remain provisional, so eligibility is named `candidate_pair_eligible`.
4. Read `candidate_pace_summary.csv`: paired VER−RUS median, count and IQR (middle 50% spread). Positive means RUS was faster. Compute each pair's difference before the median.
5. Read `sensitivity_summary.csv`: include/exclude yellow-overlap laps and expand/shrink intervals by one second. Phase thresholds move with those candidate boundaries. Minimum five pairs is a display rule, not a confidence guarantee.
6. Add tyre-stint context. Starting tyre age is not necessarily zero for a new stint. Do not isolate a tyre effect from this descriptive comparison.

## Function map

| Function | Purpose |
|---|---|
| `load_and_validate` | Preserve raw inputs and confirm joins, IDs, duration/start timing and leader identity. |
| `build_candidate_periods` | Pair SC deployment/return notices; build conservative yellow notice intervals and record conflicts. |
| `select_candidate_pairs` | Apply time overlap, pit, restart, timing and stint-context rules to both drivers. |
| `summarize_pace` | Calculate the median and IQR of same-lap differences. |
| `sensitivity_check` | Show how predefined exclusion rules affect counts and summaries. |
| `plot_results` | Export timing, candidate pace and tyre figures. |
| `save_results` | Save input hashes, event-gap joins, exclusions, summaries and figures. |

## Important boundaries

This is a tutorial/companion notebook with the actual commented code. Run every cell from top to bottom. CSV field names and API event strings remain English in both versions so calculations are directly comparable. Explanations, comments and figures are localized.

The case study intentionally stops if VSC/RED messages appear, because those intervals have not been implemented for another race. It is not a generic all-races eligibility engine. Sector yellow notices are treated conservatively; a sector is not necessarily one of the three timing sectors. Missing clear notices remain review items, and a timing overlap does not prove the car was directly affected.

Outputs are provisional until restart/flag review is complete. Raw files and V1/V2 are unchanged. V3 can run directly on the saved raw data.
