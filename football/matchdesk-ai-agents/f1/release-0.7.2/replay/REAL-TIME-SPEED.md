# True recorded-time playback / 실제 기록 시간 배속

v08 fixes the misleading prior 1× speed, which compressed the complete race into 60 wall-clock seconds. Completed GP now advance by:

`phase += wall_elapsed_seconds / recorded_timeline.duration * selected_speed`

Therefore one wall-clock second at 1× advances one recorded second; 0.25× and 0.5× allow slower inspection, and 2×/4×/10×/30×/60× accelerate the same shared cursor. Both map panes remain on one phase/tick, with their existing driver movement and prediction illustration rules unchanged. Full playback at 1× takes the duration of the available recorded timeline. Prediction motion remains a rank illustration, not a fitted lap-time model.

Upcoming GP have no actual duration to follow. Their prediction-only animation uses an explicitly stated 180-second illustrative base at 1×. Tooltip wording distinguishes this from true recorded elapsed time. `playbackDuration(timeline, predictionOnly)` exposes the choice for testing; invalid/missing recorded duration safely uses the illustrative base.

`node test-real-time-speed.cjs`: 899 runtime checks PASS. All 16 completed races are tested at 0.25/0.5/1/2/4/10/30/60×, asserting one wall-clock second advances precisely the corresponding number of recorded seconds. Checks also verify default 1×, tooltip wording, paused speed changes staying still, reset, listener/animation cleanup, and the future 180-second case. Source data, prediction files, GPS interpolation, history cutoffs and actual timeline are unchanged. Old assertions about a 60-second normalization must not be reused as the new speed contract.
