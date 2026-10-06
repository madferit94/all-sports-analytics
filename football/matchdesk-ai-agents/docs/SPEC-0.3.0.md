# MatchDesk 0.3.0 — requirements and evidence / 요구사항·검증

Release date: 2026-10-06 (Asia/Seoul). Scope: team analytics, viewer improvements, archived baseline experiment and two design previews. Publication/merge is authorized by the user; hosting a live service is not part of this release.

| Requirement / 요구사항 | Implementation / 구현 | Evidence / 근거 | Limit / 한계 |
|---|---|---|---|
| PL + LaLiga historical/current results | HTML embeds 2,399 completed and 641 scheduled records; 56 historical/current clubs | Latest preview checks and preserved data manifest | Last completed match 2026-09-20; no data refresh in this release |
| Team logo/name opens overview | Exact internal team route with league selection | Navigation tests | Logo image rendering not visually reverified |
| Team/season/venue/result/date filters | Shared selection for match summaries and detail totals | Independent sum/date-range checks | StatMuse 160 season snapshots remain whole-season values |
| Readable metric labels | 47 Korean labels, explanations, name/code/description search | Language and search tests | SH-BLK attack/defence direction remains ambiguous |
| Meaning on click | One labelled bubble; reading tips; close button/outside/Escape; focus return | Open/switch/close/filter/scroll tests | Real-browser keyboard/touch checks remain pending |
| Prevent layout overflow | Zero-minimum grid tracks, wrapped names, responsive columns, local table scrolling | CSS plus preserved functional checks | No real-browser small-screen/zoom verification |
| Hide source collection section | v11+ removes panel and snapshot provenance fields | Absence checks | Separate local admin file has no authentication; earlier snapshots/raw evidence retained |
| Remove external match navigation | Numeric/history results are plain text; internal team links remain | Rendered table output checks | Remote logos/fonts still make asset requests |
| Soft design candidate | v13 warm surfaces, rounded cards, selected-club accent | 35 Node VM checks | Preview; human design acceptance pending |
| Pixel/game-inspired preview | v14 original SVG stadium, pixel frames/buttons, Galmuri headings | 36 Node VM checks | Decorative pitch, no actual coordinates; font/images/rendering not visually verified |
| Preserve versions | v01–v14 folders, VERSION, changelog, selection JSON, hashes | Release manifest and Git commits | Snapshot numbers are viewer revisions, not semantic release numbers |
| Prediction honesty | Baseline code/tests/review archived; service adoption remains false | Existing modeling review; five temporal unit tests | New-season accuracy worse than baseline; no probabilities in viewer |

## Data scope / 자료 범위

- Completed: 2023/24 760, 2024/25 760, 2025/26 760, elapsed 2026/27 119. Both leagues combined.
- Embedded team-match details: 4,798 rows. StatMuse: 160 team-season snapshots × 47 fields.
- Public CSV demonstration stays 20 completed/2 scheduled; full training CSV and provider caches remain local. The newer HTML contains the larger read-only display dataset. Do not mistake the CSV demo for the modeling corpus.
- Future fixtures are comparison/prediction targets, never completed labels. Comparison history precedes the target date.
- No Football-Data, odds or Champions League. No collected shot coordinates, fabricated x/y positions, fake rating/level, or unadopted service probabilities.
- Team accent hex values are UI choices. Official colour-family checks cover six clubs; other colours are candidates. Logos use observed StatMuse CDN URLs and an initials fallback.

## Verification status / 검증 상태

Release checks are executed locally with Python/Node. Node VM uses simplified DOM objects: it validates calculations and interaction logic, not rendered pixels, browser event integration, image/font loading, or mobile touch behavior. The root workshop journal stays local and records participant confirmation separately. No screenshot of the new designs has been verified.

Archived model review distinguishes author checks, independent recomputation, and reproduction. A passing implementation check does not approve model performance or production deployment.

## Design references / 디자인 참고

- [NES.css official demo](https://nostalgic-css.github.io/NES.css/) — pixel component direction.
- [RPGUI official demo](https://ronenness.github.io/RPGUI/) — game menu/window direction.
- [Galmuri official project](https://github.com/quiple/galmuri) — Korean bitmap-style font, requested from the CDN at 2.40.3 with system fallback.

Custom CSS/SVG are authored for this preview. NES.css/RPGUI code and art are not copied. Deployment, administrator authentication, automatic refresh and model improvement remain future work.
