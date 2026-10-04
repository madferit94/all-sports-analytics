# Saved-source, Python and presentation audit

[English](report.md) | [한국어](report.ko.md)

## Conclusion

All 77 independent pipeline checks pass. No metric-calculation or player-selection mismatch was found in the checked saved snapshot. The 16 native PPT charts and 2,381 values in their embedded workbooks agree with the numerical analysis. The decoded RGB images on all 13 PDF pages match the final PPT renders. This is internal source-to-output consistency, not external certification of match events or xG calibration.

## Scope and methodology

The saved 2025/26 snapshot contains 1,018 raw JSON files, 1,752 fixtures, 2,775 player-league summary rows, 18,128 canonical detailed appearances and 24,185 shot events. Detailed player responses cover 1,013 forward/substitute candidates, not all players in the summary table. The analysis cohort contains 181 recorded central-forward candidates, 5,204 appearances, 314,600 minutes and 8,847 non-penalty shots.

Raw JSON was reconstructed and reconciled with CSV fields, including null serialization. Raw-file hashes and retrieval metadata were checked. Event-level minutes, shots, goals and xG were independently aggregated; selection, median groups, Q75 thresholds, ranks, joins and zero-shot rates were reproduced. English/Korean numerical CSVs match byte-for-byte. Both analysis notebooks were rerun at the repository location with 16 code cells each; their Python logic matches the corresponding scripts. Both audit notebooks also execute from the relocated project.

## Corrected display issues

| Issue | Correction |
|---|---|
| Repeated shot-location tick labels after PDF rendering | Narrowed chart and displayed distinct 0.50–1.00 ticks; event coordinates unchanged |
| Possible duplicate penalty labels in PowerPoint | Disabled all native penalty labels and retained four explicit positive values; the zero remains hidden |
| Rounded metrics displayed as an exact multiplication | Displayed the metrics independently; formulas use unrounded values |

## Selection questions remain distinct

The five league representatives are selected by maximum NP xG/90 among cohort players with at least 50 NP shots: Haaland, Lewandowski, Kane, Krstovic and Aubameyang. The four cases (Ekitike, Budimir, Højlund and Pellegrino) are closest to their median-defined quadrant centers, after cohort-SD scaling, with at least 50 NP shots. Seven standouts pass both pooled-cohort Q75 thresholds. League scoring leaders come from total goals in all 2,775 summary rows. These are different descriptive questions, not overall ability rankings.

## Known source anomalies and limits

Twelve source appearances differ only in roster_id. Canonical records retain the smallest roster_id, preserve duplicate evidence, and exclude all 12 affected candidate rows from the final cohort. Eight OwnGoal events are retained in raw/processed data but excluded from attacking shot metrics. Assisted-player nulls occur in 5,688 original events and are not used by this analysis.

“Zero shots with 60+ minutes” means an appearance lasting at least 60 minutes with zero non-penalty shots; it is not a rolling window. The match scatter contains all appearances. The date range is 15 August 2025 to 24 May 2026. Live provider corrections, official-match/footage cross-checks, xG calibration, defensive analysis and league/team/opponent/game-state adjustment are outside scope. One-season conversion gaps do not establish persistent finishing skill. Microsoft PowerPoint itself was not executed; use the supplied verified PDF for posting.

## Individual checks

| Check | Status | Evidence |
|---|---|---|
| input_hash:striker_scatter_ready.csv | pass | "4f60944eae691622626517c244bf05c18fda01fdff77870ac2ea120d54b9a31b" |
| input_hash:shot_events.csv | pass | "04533747c93d7b94858b460f0ef5bb9d68bcc89fe09c1f8b7b9242ce219987ab" |
| input_hash:player_match_records.csv | pass | "e5d3dd3b84edb3f4f14f309a1e2df800fcbd6277f86bcc6fc24b3b9170eca0f2" |
| input_hash:forward_candidate_audit.csv | pass | "cf27c7821fbd6584f99a858290582b4119d20dbc66c18f3876986921b6f8813c" |
| raw_hashes_and_retrieval_metadata | pass | {"files": 1018, "mismatches": []} |
| league_summary_raw_reconciliation | pass | {"rows": 2775, "mismatch_keys": []} |
| fixture_raw_reconciliation | pass | {"fixtures": 1752, "mismatches": []} |
| duplicate_payload:11401:29482 | pass | "784933" |
| duplicate_payload:12160:29482 | pass | "784971" |
| duplicate_payload:12322:29482 | pass | "784957" |
| duplicate_payload:13700:29482 | pass | "784927" |
| duplicate_payload:13701:29482 | pass | "784925" |
| duplicate_payload:13705:29482 | pass | "784931" |
| duplicate_payload:13996:29482 | pass | "784967" |
| duplicate_payload:14173:29482 | pass | "784941" |
| duplicate_payload:14393:29482 | pass | "784929" |
| duplicate_payload:5656:29482 | pass | "784968" |
| duplicate_payload:770:29482 | pass | "784972" |
| duplicate_payload:8187:29482 | pass | "784969" |
| appearance_raw_reconstruction | pass | {"canonical_rows": 18128, "duplicates_retained_in_evidence": 12, "mismatches": []} |
| shot_raw_reconstruction | pass | {"events": 24185, "mismatch_ids": []} |
| profile_keys_and_completeness | pass | {"players": 181} |
| event_and_appearance_unique_keys | pass | {"events": 24185, "appearances": 18128} |
| all_event_appearance_links | pass | {"orphan_events": 0} |
| event_ranges | pass | "X,Y,xG in [0,1]" |
| penalty_own_goal_flags | pass | {"own_goal_events": 8} |
| all_cohort_metrics_from_events | pass | {"cohort_rows": 181, "cohort_minutes": 314600, "cohort_np_shots": 8847} |
| duplicate_affected_candidate_exclusion | pass | {"affected_candidate_rows": 12} |
| recorded_position_minutes | pass | {"candidate_rows": 1042, "mismatches": []} |
| position_classification_rule | pass | "Known position minutes ≥50% of total; FW minutes ≥50% of known position minutes" |
| cohort_filter_reproduction | pass | {"selected_rows": 181, "excluded_failed_qc": 12} |
| four_quadrant_classification | pass | {"volume_median": 2.464840858623242, "quality_median": 0.1579359607263044} |
| global_upper_quartile_standouts | pass | {"players": ["Serhou Guirassy", "Patrik Schick", "Erling Haaland", "Benjamin Sesko", "Ferrán Torres", "Alexander Sørloth", "Robert Lewandowski"], "volume_q75": 2.87109375, "quality_q75": 0.1976654265075922} |
| output_metric_formula | pass | "NP goals - event xG; conversion NP goals/shots" |
| bilingual_parity:player_profiles.csv | pass | "Exact CSV byte comparison" |
| bilingual_parity:league_summary.csv | pass | "Exact CSV byte comparison" |
| bilingual_parity:representative_players.csv | pass | "Exact CSV byte comparison" |
| bilingual_parity:match_consistency.csv | pass | "Exact CSV byte comparison" |
| bilingual_parity:player_match_analysis.csv | pass | "Exact CSV byte comparison" |
| bilingual_parity:shot_volume_ranking.csv | pass | "Exact CSV byte comparison" |
| bilingual_parity:chance_quality_ranking.csv | pass | "Exact CSV byte comparison" |
| bilingual_parity:goals_above_xg_ranking.csv | pass | "Exact CSV byte comparison" |
| bilingual_parity:league_metric_representatives.csv | pass | "Exact CSV byte comparison" |
| bilingual_parity:both_measures_standouts.csv | pass | "Exact CSV byte comparison" |
| four_case_selection | pass | [["EPL", "Hugo Ekitike"], ["La_liga", "Ante Budimir"], ["Serie_A", "Rasmus Højlund"], ["Serie_A", "Mateo Pellegrino"]] |
| league_representative_selection | pass | [{"league": "EPL", "player_name": "Erling Haaland", "npxg_per90": 0.7779655817986165}, {"league": "La_liga", "player_name": "Robert Lewandowski", "npxg_per90": 0.764004570140612}, {"league": "Bundesliga", "player_name": "Harry Kane", "npxg_per90": 0.8016770556920542}, {"league": "Serie_A", "player_name": "Nikola Krstovic", "npxg_per90": 0.7921103954446962}, {"league": "Ligue_1", "player_name": "Pierre-Emerick Aubameyang", "npxg_per90": 0.6737361387183518}] |
| metric_rank:shot_volume_ranking | pass | {"rows": 181} |
| metric_rank:chance_quality_ranking | pass | {"rows": 85} |
| metric_rank:goals_above_xg_ranking | pass | {"rows": 85} |
| zero_shot_appearance_reconstruction | pass | "All appearances retained; absent NP event totals become 0" |
| 60plus_zero_shot_rates | pass | "Condition is ≥60 minutes played per appearance, not a rolling 60-minute window" |
| ppt_chart_1 | pass | [{"series": 0, "points": 33, "match": true}, {"series": 1, "points": 38, "match": true}, {"series": 2, "points": 30, "match": true}, {"series": 3, "points": 50, "match": true}, {"series": 4, "points": 30, "match": true}] |
| ppt_chart_3 | pass | [{"series": 0, "points": 33, "match": true}, {"series": 1, "points": 38, "match": true}, {"series": 2, "points": 30, "match": true}, {"series": 3, "points": 50, "match": true}, {"series": 4, "points": 30, "match": true}] |
| ppt_chart_2 | pass | [{"series": 0, "points": 5, "match": true}] |
| ppt_chart_4 | pass | [{"series": 0, "points": 181, "match": true}, {"series": 1, "points": 1, "match": true}, {"series": 2, "points": 1, "match": true}, {"series": 3, "points": 1, "match": true}, {"series": 4, "points": 1, "match": true}, {"series": 5, "points": 1, "match": true}] |
| ppt_chart_5 | pass | [{"series": 0, "points": 1, "match": true}, {"series": 1, "points": 1, "match": true}, {"series": 2, "points": 1, "match": true}, {"series": 3, "points": 1, "match": true}, {"series": 4, "points": 2, "match": true}, {"series": 5, "points": 2, "match": true}] |
| ppt_chart_6 | pass | [{"series": 0, "points": 33, "match": true}, {"series": 1, "points": 38, "match": true}, {"series": 2, "points": 30, "match": true}, {"series": 3, "points": 50, "match": true}, {"series": 4, "points": 30, "match": true}, {"series": 5, "points": 2, "match": true}] |
| ppt_chart_7 | pass | [{"series": 0, "points": 5, "match": true}] |
| ppt_chart_8 | pass | [{"series": 0, "points": 5, "match": true}] |
| five_scoring_leaders | pass | [{"player_name": "Erling Haaland", "league": "EPL", "goals": 27}, {"player_name": "Kylian Mbappe-Lottin", "league": "La_liga", "goals": 25}, {"player_name": "Harry Kane", "league": "Bundesliga", "goals": 36}, {"player_name": "Lautaro Martínez", "league": "Serie_A", "goals": 17}, {"player_name": "Esteban Lepaul", "league": "Ligue_1", "goals": 21}] |
| ppt_chart_9 | pass | [{"series": 0, "points": 5, "match": true}, {"series": 1, "points": 5, "match": true}] |
| ppt_chart_10 | pass | [{"series": 0, "points": 1, "match": true}, {"series": 1, "points": 1, "match": true}, {"series": 2, "points": 1, "match": true}, {"series": 3, "points": 1, "match": true}, {"series": 4, "points": 1, "match": true}] |
| ppt_chart_11 | pass | [{"series": 0, "points": 54, "match": true}, {"series": 1, "points": 11, "match": true}] |
| ppt_chart_12 | pass | [{"series": 0, "points": 84, "match": true}, {"series": 1, "points": 11, "match": true}] |
| ppt_chart_13 | pass | [{"series": 0, "points": 47, "match": true}, {"series": 1, "points": 12, "match": true}] |
| ppt_chart_14 | pass | [{"series": 0, "points": 64, "match": true}, {"series": 1, "points": 8, "match": true}] |
| ppt_chart_15 | pass | [{"series": 0, "points": 4, "match": true}, {"series": 1, "points": 4, "match": true}, {"series": 2, "points": 4, "match": true}, {"series": 3, "points": 4, "match": true}] |
| ppt_chart_16 | pass | [{"series": 0, "points": 28, "match": true}, {"series": 1, "points": 37, "match": true}, {"series": 2, "points": 33, "match": true}, {"series": 3, "points": 37, "match": true}] |
| removed_footer_and_author | pass | "13 slides visible text" |
| case_selection_explanation | pass | "Why these four case studies? One central example from each shot-profile quadrant, with at least 50 non-penalty shots. Hugo Ekitike High volume · High xG/shot Ante Budimir High volume · Low xG/shot Rasmus Højlund Low volume · High xG/shot Mateo Pellegrino Low volume · Low xG/shot Why these four? To compare shot locations, body-part mix and match variation across contrasting profiles. Split the cohort at both medians, then choose the player nearest each quadrant’s median after scaling the metrics. These are illustrative cases. High and low are relative to the cohort, not overall ability grades." |
| embedded_workbook_numeric_values | pass | {"numeric_cache_values": 2381, "workbooks": 16, "errors": []} |
| visible_league_representative_values | pass | "Five names and fifteen rounded metrics checked" |
| leader_superlative_claims | pass | "Highest volume Mbappe; highest quality Haaland, among five leaders" |
| league_median_claim | pass | "Premier League cohort highest median xG/shot" |
| penalty_native_labels_disabled | pass | "Five native labels hidden; four explicit positive labels retained; zero omitted" |
| ppt_native_chart_and_slide_counts | pass | {"charts": 16, "slides": 13} |
| visible_key_findings | pass | "Mbappe 4.70; Haaland .213; Lepaul +5.31; Pellegrino headers 41.7%" |

## Next steps

Use the verified presentation now, and repeat the audit after changes. Independent official-record checks and multi-season/context comparisons would address remaining evidence gaps.
