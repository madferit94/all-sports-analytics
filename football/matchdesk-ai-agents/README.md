# MatchDesk — Football Analytics Agent Team

[English](README.md) | [한국어](README.ko.md)

**Release 0.4.0 · 2026-10-06.** A provider-neutral five-agent project for football evidence, team analysis, interactive viewing, independent review and traceable decisions.

## Open a viewer

- [Open MatchDesk — adopted 8-bit design](index.html) · [versioned v15](visualization-design-2026-10-06-v15/index.html).
- [Soft app design preview — v13](visualization-design-2026-10-06-v13/index.html).
- [8-bit pixel clubhouse preview — v14](visualization-design-2026-10-06-v14/index.html).
- [Three design directions](design-candidates-2026-10-06-v01/index.html).

Download/open HTML locally; GitHub's source view does not run it. This release does not host a website. Choose Matches, Teams or League. Team names/logos open the team overview; metric names open a meaning/reading-tip bubble. Search accepts Korean labels or original codes. The source/collection panel and external match links are removed from v11/v12 onwards.

## What works, and what is pending

The viewers show PL/LaLiga history, selected-match summaries, recent xG, fixtures, season history, team search and filters. The pixel/soft designs retain the same data and behavior. The user adopted the 8-bit design in 0.4.0. All 56 club logos now render from their original images onto 24×24 grids with crisp enlargement and an initials fallback. Real-browser rendering quality remains unverified.

The baseline prediction experiment is now archived in [modeling](modeling/README.md). Its new-season accuracy underperforms the comparison baseline; adoption remains **false**, and probabilities are not shown in the viewer. Automatic refresh, administrator authentication, prediction API, hosting and a new five-agent runtime run are not implemented. Claude runtime execution is unverified.

## Data scope

The HTML embeds **2,399 completed matches, 641 scheduled matches and 56 clubs**, plus 4,798 team-match detail records and 160 team-season snapshots with 47 StatMuse metrics. Completed totals: 760 in each of 2023/24–2025/26 and 119 in elapsed 2026/27. Last recorded completed date: **2026-09-20**. No refresh was performed for these design changes.

Understat is the core match/date/xG source; StatMuse supplies additional whole-season statistics. Date/venue/result filters apply to match data; StatMuse season totals are explicitly not filtered. Football-Data, odds and Champions League are excluded. No shot-coordinate dataset is available; the pixel pitch is decorative.

The published CSV package remains a **20-completed/2-scheduled demonstration subset**. Full training CSV and provider caches remain local; the larger HTML display data does not make the demo CSV a complete modeling corpus. Squad/value/news evidence has different observation dates and documented gaps.

## Five execution owners

| Agent | Responsibility |
|---|---|
| Director | Plan, assign, track and decide after independent review |
| Research | Collect matches, auxiliary evidence and team news |
| Analyst | Team comparison and experimental modeling |
| Builder | Viewer, chart and service implementation |
| Reviewer | Independent calculation, data and model checks |

[Five-agent package](agent-team-integrated-2026-10-06-v01/README.md) · [Preserved ten-role package](agent-team-2026-10-06-v01/README.md) · [Actual archived run](team-run-2026-10-06-v01/README.md).
The actual representative Arsenal–Leeds/Malaga–Espanyol run used the previous ten-role arrangement; it is not relabelled as a five-agent run. Reviewer and final director stay separate from authors and each other. Model adoption and business decisions remain with the human user.

## Verification and limitations

```sh
python -m unittest discover -s agent-team-2026-10-06-v01/tests -v
python -m unittest discover -s agent-team-integrated-2026-10-06-v01/tests -v
python -m unittest discover -s modeling/tests -v
node visualization-design-2026-10-06-v15/check.cjs
```

Python 3.11+ with the pinned NumPy requirement is needed for model tests; agent tests use the standard library. Node runs 40 calculation/navigation/interaction checks with a DOM stub. **Real-browser rendering, mobile touch, remote logo/font loading and visual verification are pending; design adoption was explicitly confirmed.** A separate local source report is not an authenticated admin area. Historical snapshots still preserve earlier provenance. Team hex colours are UI choices, not verified official brand hex codes.

Archived run: 49 auxiliary entries (26 collected, 22 missing, 1 blocked), 117 squad players and 44 previous starters; an independent saved-input comparison recorded 271 checks. These verify scope and consistency, not every provider fact.

## Versions and specifications

[VERSION](VERSION) · [CHANGELOG](CHANGELOG.md) · [Release SPEC](docs/SPEC-0.4.0.md) · [0.3.0 SPEC](docs/SPEC-0.3.0.md) · [Version policy](docs/VERSIONING.md) · [Current viewer selection](viewer_selection.json) · [Content hashes](publication_manifest.json).
UI v01–v15 are preserved. Release 0.4.0 adopts v15 as the canonical index.html; archived v13/v14 remain design history. Older references and the original 0.2.1 manifest remain available. Some archived build/review commands describe the original local environment; use the checked-in HTML or current checks rather than assuming every old generator is portable.

| UI version | Change / 변경 |
|---|---|
| [v01](visualization-design-2026-10-06-v01/index.html) | Initial wireframes and coordinate audit |
| [v02](visualization-design-2026-10-06-v02/index.html) | Site design system |
| [v03](visualization-design-2026-10-06-v03/index.html) | Visitor UI and team colours |
| [v04](visualization-design-2026-10-06-v04/index-v02.html) | 56 logos and season history |
| [v05](visualization-design-2026-10-06-v05/index.html) | Team-name routes and overview |
| [v06](visualization-design-2026-10-06-v06/index.html) | 47 metrics and match filters |
| [v07](visualization-design-2026-10-06-v07/index.html) | Long-label and card containment |
| [v08](visualization-design-2026-10-06-v08/index.html) | Optional metric notes |
| [v09](visualization-design-2026-10-06-v09/index.html) | Korean names and meanings |
| [v10](visualization-design-2026-10-06-v10/index.html) | Click-to-open explanations |
| [v11](visualization-design-2026-10-06-v11/index.html) | Source metadata separation |
| [v12](visualization-design-2026-10-06-v12/index.html) | Remove external match links |
| [v13](visualization-design-2026-10-06-v13/index.html) | Soft app preview |
| [v14](visualization-design-2026-10-06-v14/index.html) | Pixel clubhouse preview |
| [v15](visualization-design-2026-10-06-v15/index.html) | Adopt pixel design; render all club logos on 24×24 grids |
