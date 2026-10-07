# Shared playback speed / 예측·실제 공통 배속

v07 corrects the prediction pane's fixed three-loop circuit animation. Completed-race display now uses `raceLapCount(race)`: the maximum valid recorded lap number, falling back to stored session-result lap count only when no valid lap interval is available. Australia uses 57 valid recorded laps; its stored result has 58 laps, but the replay timeline lacks a valid duration for the final lap. Upcoming races and missing counts retain three illustrative loops rather than inventing target data.

`predictedMarkers(prediction, phase, map, lapCount)` uses the existing predicted normalized progress times this display-only lap scale. Predicted order, probabilities and rank-dependent illustrative finishing phases are unchanged. A predicted leader can still finish early in the illustration; this is not a learned lap-time/velocity model and does not claim identical physical trajectories or per-frame car speeds.

Both panes retain one existing animation tick, shared 0..1 phase, playback speed multiplier, play/pause/reset and seek. The selector is labeled Shared speed (prediction & recorded) / 공통 배속 (예측·실제), with 1×/2×/4×. No second clock or timer was introduced. Target lap count is used only to align retrospective display scale, not as a pre-race prediction feature.

Builder evidence:
- `node test-shared-speed.cjs`: 7159 checks PASS across 16 completed races. Covers valid/result/missing/future counts, 22-marker identity, preserved order/probabilities/finishing progress, exact circuit placement, old fixed-three-loop mismatch, immutable predictions and unchanged recorded duration.
- Existing `node test-driver-dashboard.cjs`: 11339 checks PASS, including default-all/selection/playback and time-cutoff dashboards.
- Independent reviewer/root browser evidence is separate; runtime 1×/2×/4× ratios and simultaneous drawing are verified there.
