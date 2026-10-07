# Pre-race prediction vs recorded race / 경기 전 예측과 실제 기록 비교

`comparison.js` is a new v04 module; the preserved v03 `replay.js` supplies its lap timeline API unchanged.

```js
const view = MatchLabF1Comparison.mount(container, race, historicalPrediction, {locale:'ko'});
// Before navigation:
view.destroy();
```

Pass one race from `data/season-2026.json` and its matching `modeling/historical-predictions.json.races[String(session_key)]`.

- Two horizontal lane boards retain all 22 driver identities, not a generic oval.
- Prediction-board car positions are a deterministic illustration of `predicted_order`, not trained lap times or overtakes. The normalized 0..1 phase calculation takes only the prediction object. It never reads target laps, results or pit data.
- Record-board vehicle distance uses the valid lap intervals in `MatchLabF1Replay.timeline`. Missing lap intervals, DNS and DNF remain stopped.
- Record-board displayed rank selects the latest OpenF1 `records.position` sample at or before the actual record cursor: `timeline.start + phase * timeline.duration`. Future samples are excluded even when input rows are unsorted. Out-of-range ranks (for example position 23 among 22 entries) remain in raw data but fall back to inferred order with invalid_position_sample=true. Missing samples are labeled with `*` and `rank_source: lap_inference`; final rank comes from `session_result`.
- The comparison table has predicted order, actual order, final finish/DNF/DNS/DSQ status, actual-minus-predicted rank difference and unmodified model win probability.
- The shared controls animate the normalized phase over 60 wall-clock seconds at 1/2/4×; prediction-board timing is display-only. Playback begins paused, including reduced-motion contexts. Hidden pages pause. `destroy()` cancels animation and unregisters page/control listeners.
- Font size is 14px or larger in lanes; controls are at least 44px tall; narrow layouts stack prediction and record boards.

`node test-comparison.cjs` executes 340 checks across 16 completed GP in a Node virtual document plus pure functions. It verifies 22+22 lanes, 22 comparison rows, immutable predictions, bounds, endpoint/reset/hidden cleanup, official final results, source-time safety and an unsorted past/future position regression. This is builder evidence, not real-browser proof; browser and independent reviewer evidence are separate.


Time-origin clarification: zero phase is the first valid lap interval start, not an asserted green-light start. The clock shows elapsed time since that valid record plus the absolute Asia/Seoul HH:MM:SS KST timestamp.

Readability: the default view shows a single concise prediction-vs-record explanation. Detailed interpolation, inference, time-origin and prediction-input limitations remain accessible under a collapsed How this comparison works disclosure. Builder verification now includes this default state: 356 assertions PASS.
