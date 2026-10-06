# Football prediction cases and a MatchDesk experiment plan

Document v01 · Checked 2026-10-06 · [한국어](README.ko.md) · [Sources and execution record](sources.json)

**Test opponent strength, recency, and probability reliability before expanding the feature count.** This is a research report and a proposed experiment plan. No model was trained or adopted in this task.

## Primary-source cases

| Case | Verified approach or result | Proposed use in MatchDesk |
|---|---|---|
| Dixon–Coles (1997) | A goal-count model fitted to English league/cup results from 1992–95. A subsequent original paper explains low-score dependence and recency weighting. Publisher full-text access failed; the later paper corroborates those mechanisms. [Institutional original record](https://www.research.lancs.ac.uk/portal/en/publications/modelling-association-football-scores-and-inefficiencies-in-the-football-betting-market%28d16276a2-d6e0-483b-a708-1d29663f1992%29.html), [subsequent original paper](https://academic.oup.com/jrsssd/article/51/2/157/7120674) | Estimate a joint score distribution for outcome probabilities and pixel replay sampling. |
| Baio–Blangiardo (2010) | Hierarchical attack/defence estimation on Serie A 1991/92 and 2007/08; a mixture addressed excessive pooling. Authors acknowledge estimating from whole-season observed outcomes. [Paper, sections 4–5](https://discovery.ucl.ac.uk/16040/1/16040.pdf) | Explore partial pooling for limited histories; this paper does not establish an improvement for promoted teams. |
| Hubáček et al. (2019) | More than 200,000 historical challenge matches; pi-ratings/PageRank plus engineered features and boosted trees. Authors report the engineered-feature approach best among their validation/test comparisons. [Abstract](https://link.springer.com/article/10.1007/s10994-018-5704-6) | Test opponent-aware strength summaries using our existing records. |
| Yeung et al. (2023 preprint v1) | Five-year training windows and three temporal validation sets: mean RPS **0.2085** for CatBoost+pi-ratings, **0.2416** for selected-feature CatBoost, **0.2303** for W/D/L percentages. Lower is better. [Table 4](https://arxiv.org/html/2309.14807v1#S3.T4) | A larger feature set can underperform a compact rating model; use controlled ablations. |

These numbers are the fourth paper's validation results, not its final competition scores or expected MatchDesk accuracy. RPS measures probability error, not accuracy. The official 2023 competition evaluated 714 of 736 scheduled matches after schedule/venue exclusions. [Organizer results](https://sites.google.com/view/2023soccerpredictionchallenge/results)

## Our proposed experiments — inference, not demonstrated improvements

1. Freeze identical date cutoffs and evaluation matches for the current model, league-frequency baseline, and candidates. Report accuracy, log loss, three-class Brier, reliability bins, and sample sizes by league, season opening, missing prior-season history, and draw outcomes.
2. Compare last-five summaries with last-ten and time-weighted histories. Adjust goals/xG and conceded goals/xGA for opponents' pre-match strength and home/away context. Select decay only within development periods.
3. Fit independent Poisson goals, then compare a Dixon–Coles low-score correction. Check nonnegative normalized score probabilities and preserve tail mass. Derive W/D/L by summing the same score matrix; sample replay results from it instead of inventing a separate scoring rule.
4. Compare history weights such as `n/(n+k)` with k selected on development data. Preserve the distinction between missing prior-season observations and verified promotion. Do not invent lower-division records or equate lower-division ranks with top-flight ranks.
5. Compare a small tree model and calibrate on a held-out temporal development block. Calibration aims for reliable probabilities; temperature scaling can leave accuracy unchanged. [Official calibration documentation](https://scikit-learn.org/stable/modules/calibration.html)

Use date-based folds, keep same-date matches together, and prevent evaluation outcomes entering scaling, feature selection, ratings, or calibration. Football fixtures are irregularly spaced; do not blindly assume equally spaced samples when configuring a split helper. [TimeSeriesSplit assumptions](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)

## Existing evidence and adoption limits

The current 33-feature model recorded 50.92% accuracy and 1.011080 log loss on 760 matches in 2025/26. The rank-proxy addition recorded 49.87% and 1.011412. It did not improve performance. [Existing feature fact-check](../feature-factcheck-2026-10-06-v01/RESULTS.ko.md)

Those evaluation outcomes have already been inspected. Reusing them to select candidates is exploratory evaluation, not a new untouched final test. Before operational adoption, freeze predictions for subsequent real fixtures before their outcomes become known. Assess probability errors and league/subgroup behavior jointly; a small accuracy increase alone is insufficient evidence.

The existing completed-match data ends on 2026-09-20. No new fixtures, historical pass features, market values, second-division records, odds, or Football-Data were collected. Betting comparisons in the cited literature are not a proposed new input source. Pixel playback is a sampled fictional match, not a guaranteed score forecast. This report does not validate the current replay's score generator.

Producer: actual subagent `/root/prediction_cases`, research role using the project's `matchdesk-research` skill and integrated team protocol. Training, independent model verification, final adoption, and participant visual confirmation remain outside this research task.
