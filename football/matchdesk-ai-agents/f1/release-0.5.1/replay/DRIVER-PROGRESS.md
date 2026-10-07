# Driver progress dashboard / 드라이버 진행 기록

v06 preserves the prior versions and updates the map module only.

- Driver selection (22 individual drivers) and car visibility (All / Selected driver) are independent.
- Default All draws all 22 cars at full opacity, with the selected driver emphasized. Selected driver view is available while paused. Starting playback restores All without changing the chosen driver or its cards.
- Below the map, the selected driver dashboard shows current rank, lap, status, tyre, pit entries so far and the last completed lap duration. It includes a recorded-position step chart, last 12 completed lap-duration bars and up to three recent pit events.
- `driverHistory(race, timeline, driverNumber, phase)` is a pure exported helper. Its cursor is `timeline.start + phase * timeline.duration`. Position events must fall between the provider session start and cursor, and ranks must be valid 1..22. Completed laps require `date_start + lap_duration <= cursor`. Pit counts require entry time between session start and cursor. An entry is known before its total lane duration; the duration is shown only after `pit.date + lane_duration <= cursor`. Before then it says In progress; missing duration remains a dash.
- Missing/failed pit collection returns null, not a fabricated zero. Zero is used only when a successfully available pit array has no eligible entries.
- Seeking, including backward movement inside the same displayed second, invalidates the dashboard cache. Changing the driver refreshes all records. The final table below remains a separate static result comparison.
- Upcoming races show selected-driver predicted order and win probability, with an explicit notice that actual progress is not yet available.
- Dates are parsed as timestamp instants and display Asia/Seoul time. The session start is the provider session timestamp, not an asserted green-light time. GPS vs reconstructed location coverage remains visible. Listener and animation cleanup include the new visibility selector.

Run `node test-driver-dashboard.cjs`: 11339 checks PASS across 16 completed and 7 upcoming GP, including unique markers, strict GPS gaps, 22 individual options, full-opacity default, selected-only mode, playback returning to all, driver switching, source-time cutoffs for all 22 drivers at four cursors per completed race, pit entry and completion boundaries, same-second backward seek, tyre changes, missing and failed pit data, and cleanup. Evidence is Node VM/synthetic DOM; root/browser and independent reviewer evidence are separate.
