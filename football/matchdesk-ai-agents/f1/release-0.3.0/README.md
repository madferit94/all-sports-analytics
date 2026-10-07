# MatchLab F1 0.3.0 · prediction versus recorded race

Each of 16 completed GPs is predicted by refitting only on earlier 2025/2026 races. Recorded position samples (8100) and target laps belong only to the actual comparison board. Seven upcoming forecasts and two cancelled events remain distinct.

Predicted car motion visualizes final predicted order; it is not a learned lap-time, overtaking or pit-timing forecast. Actual motion uses valid lap timing, with recorded intermediate positions and explicit gaps; it is not GPS footage. Participant lists were acquired after races and their pre-race publication time is not established. These are retrospective reconstructions, not forecasts published before those races.

Walk-forward top1:4/16 (25%); log loss2.7249 vsrecent-win2.8225; Brier0.9483 vsbaseline0.9337. Mixed metrics do not establish superiority. Continuous-rank MAE2.950; uniquely ordered-rank MAE3.713. This retrospective evaluation does not replace the separate frozen last-six-race holdout. See modeling/HISTORICAL-COMPARISON.md. Priorv03 preserved; participant verification pending; not pushed to GitHub.

Public release stores display payloads and evidence; training reproduction requires the local original historical session files.
