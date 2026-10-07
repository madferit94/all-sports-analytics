# Barcelona circuit image repair / 바르셀로나 서킷 이미지

MatchLab 0.19.2 / F1 0.7.2

- Observed: old meeting.circuit_image returned HTTP404; image error handler hid it and displayed Catalunya text only.
- Replacement discovered on https://www.formula1.com/en/racing/2026/barcelona-catalunya ; HEAD200 image/webp.
- Display override only for session11307/circuit15, leaving source meeting metadata intact.
- Both catalog and detail image calls pass race context. On image failure use existing map11307 coordinates only when circuit keys match. Preserve aspect ratio; no invented path or artificial closure. Fallback labeled recorded-coordinate outline in KO/EN.
- Real image load at 320/1280px, forced network failure fallback, geometry count and mismatch guard: 8 checks PASS.
- Prior v12/0.19.1 preserved. Data/models unchanged. Participant confirmation pending. No GitHub upload requested.

Current localhost full-page integration PASS: Barcelona detail and catalog images visible with naturalWidth greater than zero.

