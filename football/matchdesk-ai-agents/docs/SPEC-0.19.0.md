# F1 natural-language charts / 자연어 시각화

Version: MatchLab 0.19.0 / F1 0.7.0.

- A natural-language analysis tab appears in completed and scheduled GP details.
- Scope is the selected GP; supports recognized Korean/English driver aliases and lap times, mean lap time, stationary/pit-lane time, top recorded speed, points, final position and stored win probability.
- This is deterministic parsing of supported expressions, not a connected general-purpose LLM. No API call, credential or arbitrary SQL/Python execution.
- Unsupported conditions, dates, race names, unknown drivers and multi-metric ambiguity return guidance instead of dropping conditions.
- Lap trends require 1–4 drivers, retain lap gaps and include all recorded valid laps. Pit/safety-car effects explicitly explained; no clean-pace claims.
- Metric bars include recorded values and missing values; stationary stops retain coverage counts and partial-average labels.
- Scheduled GPs cannot produce actual-record charts. Probability uses existing saved model, not a generated prediction.
- Labels and prompt are escaped; 500-character input limit. 44px buttons, visible labels, keyboard submission and live status.
- 34 parser/computation checks on actual race data PASS; 40 real isolated-component headless Edge checks in KO/EN at 320/375/768/1280px PASS. Participant confirmation pending.
- Prior v10/UI 0.18.1 preserved. Data and prediction files unchanged; no GitHub upload this turn.

Full localhost integration PASS: analysis tab → pit-stop chart (Norris 2.75s) → existing metrics tab. Local server restarted after connection refusal. Participant confirmation remains pending.

