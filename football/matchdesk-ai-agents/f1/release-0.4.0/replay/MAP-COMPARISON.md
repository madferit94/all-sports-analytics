# F1 map comparison / 서킷 지도 비교

New v05 module, preserving v03/v04 implementations:

```js
const view = MatchLabF1MapComparison.mount(container, race, prediction, {
  locale: 'ko',
  map: maps.races[String(race.session.session_key)],
  // mode: 'prediction' for upcoming races
  // selectedDriver: 63 (optional)
});
view.destroy(); // before changing races/pages
```

Dependencies: `replay.js` and `comparison.js`. Map input: raw Cartesian `points:[[x,y]...]`, `circuit_key`, and `drivers[number].samples:[[epoch_ms,x,y]...]`. The collector provides reference/cutoff/provenance metadata. Raw outline and driver points share one uniform transform. Circuit key mismatch, absent shape, too few valid points or degenerate shape produce an explicit unavailable-map placeholder; no oval or other circuit substitution occurs.

Completed races have 22 predicted and 22 recorded markers on the same observed circuit outline. The prediction car movement illustrates predicted final order over a normalized display phase (three illustrative loops); it does not train or infer lap times/overtakes, and does not consume target results/laps/pits. Recorded car coordinates use exact observed timestamps or linear interpolation only across a complete bracket of at most 2000ms. Outside sample coverage, invalid coordinates and gaps use a dashed lap-progress reconstruction, not claimed GPS. The current source mix is visible, e.g. 2 location records / 20 reconstructed. OpenF1 position samples provide rank at the cursor; missing/invalid rank carries an asterisk. Final rank/status uses stored official session results.

Driver selection highlights the selected pixel car last and shows a large 32px canvas label with number/acronym, a contrasting background and a clamped in-canvas label box. Selected cards explain coordinate source. The model/actual final table shows order, DNF/DNS/DSQ status, rank difference and win probability. Controls have minimum 44px targets; layout stacks on narrow screens. Both panes share phase/seek/speed. Playback starts paused, page hiding pauses, and destroy removes listeners and animation.

Upcoming races use prediction-only mode with 22 forecast drivers and one canvas. The default note explicitly says 2025 reference layout; the collapsed detail says this year's official layout equivalence has not been confirmed. Actual GPS/lap reconstruction legends are absent in prediction-only mode. Data collection selects historical same-circuit references; the display never treats a historic layout as confirmed current GPS.

Builder execution: `node test-map.cjs` → 5689 assertions PASS, 16 completed + 7 upcoming GP. Tests cover unique 22 markers, finite raw/pixel XY, exact 2000ms/2001ms/4000ms boundaries, exact-known-point acceptance, no extrapolation, circuit mismatch, missing-map placeholder, 22-row comparison, selection choices, endpoint/hidden/destroy, 2025 upcoming reference and unconfirmed-layout notices, and no actual-pane/actual-GPS legend in future mode. Evidence: `map-verification.json`. This is Node VM/synthetic DOM proof; real-browser screenshots and independent checks are separate. Monaco's preserved ~50-minute location gap is never bridged by the strict interpolation rule.
