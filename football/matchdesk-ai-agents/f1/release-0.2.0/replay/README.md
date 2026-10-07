# F1 record replay / F1 기록 재생

`replay.js` exposes `window.MatchLabF1Replay.mount(container, race, {locale, shape})`.
Use the race record from `data/season-2026.json`. `locale` is `ko` or `en`.
Optional `shape` is `track-shapes.json[String(race.session.session_key)]`.
The returned object has `destroy()` and `timeline`; destroy it before navigation.
`timeline(race).state(seconds)` is also exposed for deterministic tests.

- All 22 driver entries remain visible; race-order is reconstructed from recorded lap start/end times.
- Cars move only within valid recorded intervals. Missing intervals pause; DNS does not move; DNF stops after the last recorded lap. At the final cursor, the official stored session result supplies rank and final status.
- Tyre stint and pit indicators use the stored lap/time records.
- Playback, pause, reset, 10/30/60/120×, seek, page-hidden pause and listener/RAF cleanup are implemented.
- Reduced-motion does not autoplay. Playback always starts paused.
- Motion is lap-time interpolation, **not actual GPS movement or recorded overtakes**. The trace shape, if available, is a normalized single recorded lap, not an independently surveyed circuit.
- All 16 completed 2026 location requests returned HTTP 404 in this run. Therefore the UI uses an explicitly labeled schematic track, not a false actual circuit map. Circuit keys stay separate: Bahrain-titled session 11731 carries circuit key 12 (Sepang); cancelled 11261/key63 is not replayed or reused.

## 실행 근거

`node test-timeline.cjs`: 16 races / 22 drivers each / 6977 assertions PASS. The builder test covers finite progression, DNS immobility, active intervals, stopped final states, DNF states, official final rank, forward/backward seek and a missing-lap gap. DOM/browser checks remain the independent reviewer/root integration responsibility. `track-shapes.json` contains per-request endpoint/error records. Collection retries were performed after the initial local network sandbox socket denial; actual outbound requests returned HTTP404.
