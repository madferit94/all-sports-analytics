# MatchLab F1 0.2.0

Completed races open a recorded-lap pixel replay; upcoming races open historical-result forecasts. 16 completed, 7 upcoming and 2 cancelled races remain separate. Replay uses a schematic circuit because all 16 location requests returned HTTP 404; it is not GPS footage or a record of actual overtakes.

The model uses 2025 and completed 2026 results, with ten pre-race indicators and a last-six-race chronological holdout. Win prediction hit 2/6; log loss 3.1195 was worse than uniform 3.0910 and recent-win baseline 2.9699. Predictions are experimental and use projected, unconfirmed entries. See modeling/README.md and verification/. Original versions remain preserved. User verification pending.
