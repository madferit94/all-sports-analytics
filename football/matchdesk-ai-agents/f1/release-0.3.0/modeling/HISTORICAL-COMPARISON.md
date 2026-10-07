# Pre-race model versus actual race · 0.3.0

`historical-predictions.json` contains all 16 completed 2026 Grand Prix. For each target, a new logistic winner model and ridge finishing-percentile model are fitted only on completed races ending before that target starts. The first five 2025 races are warm-up history; they are not training examples. Consequently the first 2026 GP uses 19 training races and the sixteenth uses 34. Earlier 2026 results enter only after their race has ended. The current target's labels cannot enter its own fit. `historical-feature-audit.json` records every training key and latest source end.

Ten indicators and fixed settings are reused from the previous experimental model: last-five finishing score, points, win rate, podium rate and DNF/DNS/DSQ rate; season-to-date finishing score; team recent finishing score and win rate; previous same-circuit finishing score and win rate. Circuit identity is the recorded actual circuit key rather than Grand Prix title. Numbers changing between driver seasons are not identity keys. Cold starts use fixed neutral priors.

The `drivers` array contains prediction information only. `predicted_order` assigns a unique final-order illustration by sorting the continuous expected rank, breaking ties by win probability then driver number. This assigned order is distinct from the model's continuous expected-rank estimate. The separate `actual.drivers` array supplies official recorded position and DNF/DNS/DSQ flags for comparison, without affecting this target's forecasts. An animation of `predicted_order` is a symbolic visualisation of a final-order forecast, not a lap-by-lap speed, overtaking, pit or retirement simulation. Target timing/laps must never shape the prediction lane.

| Retrospective metric, 16 GP | Model | Recent-win baseline | Uniform |
|---|---:|---:|---:|
| Winner top-1, ties shared | 25.0% (4/16) | 26.25% | 4.55% |
| Log loss, lower better | 2.7249 | 2.8225 | 3.0910 |
| Brier sum across entrants, lower better | 0.9483 | 0.9337 | 0.9545 |

Continuous expected-rank MAE is 2.950 places. Assigned unique-order MAE is 3.713 places. The model improves log loss but loses to the recent-win baseline on Brier and top-1. This is not a claim of superior forecasting. Tied top-1 probabilities share credit rather than selecting an arbitrary first driver.

These forecasts are reconstructed now; no claim is made that they were published before the races. The participant list comes from target-session drivers metadata collected after the race. Its pre-race publication timestamp is unverified, so this evaluation assumes the retrospective roster. There is no qualifying grid, future weather or race-final championship information in input features. This 16-race reconstruction is not a new untouched prospective test, does not replace the previous six-race frozen evaluation, and has uncalibrated probabilities and 2026 regulation-change limitations. The existing seven future-GP predictions remain separate and unchanged.

Reproduce `train-historical.py` and `check-historical.py` using the earlier Python/scikit-learn environment. The historical runner extracts only declarations from `train.py` through Python's syntax tree; it does not import or execute that script's global fitting or publishing statements. Original v03 artifacts are preserved. Self-check: 834 checks; independent reviewer/director approval is separate.
