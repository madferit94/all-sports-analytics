## 0.17.0 — 2026-10-07
- Preserve selected-driver view; Play shows all drivers and live cursor-based records.
- 전체22명재생/개별보기/선택선수순위·랩·타이어·피트차트,미래실제기록제외.

## 0.16.0 — 2026-10-07
- Port Baku xy/time replay principles into circuit-map comparison.
- 종료16지도·예정7역사참고지도,22차량/2명좌표와랩재구성구분.
- Fix invalid location query operators; preserve raw hashes, gaps and models.

## 0.15.0 — 2026-10-07
- Completed F1 prediction-vs-record comparison; per-race walk-forward refits.
- 종료GP예측판/실제판비교, 공식순위8100행추가,학습입력과실제기록분리.
- Korean/English descriptions, version backups and leakage checks.

## 0.14.0 — 2026-10-07
- Resume F1/sport integration; completed replay and scheduled historical-result forecasts.
- 기록 재생16/예정 예측7/취소2 구분, GPS 결측 및 모델 한계 표시.
- Version snapshots and bilingual documentation; independent checks and browser verification.

## 0.13.0 — 2026-10-07
- Add same-server Football/F1 navigation and preserve language.
- Separate Grand Prix branding from actual host venue; official Sepang override for Bahrain meeting1308.

## 0.12.2 — 2026-10-07
- Rename the KO/EN site to MatchLab; retain internal identifiers and historical snapshots.
- Retry one transient upstream 5xx response; cap each attempt at 25 seconds and preserve distinct auth/quota/timeout errors.

## 0.12.1 · 2026-10-07

- Publish accumulated0.9.2–0.12.0 changes, models, viewer snapshots and validation evidence.
- Add English packages for the current five-agent team, legacy ten-role team and three record/SQL/Python skills.
- Preserve Korean originals and shared contracts/tools; correct English package-relative paths.
- Refresh bilingual repository/project READMEs and publication inventory.

## 0.12.0 · 2026-10-07

- Team chart explorer with10match trends and47season metric options across6categories.
- Data-appropriate lines, grouped bars, stacked counts and0–100percentage bars.
- Missing data gaps, ongoing-season scope, exact value tables and metric explanation→chart links.
- Stored analyst, builder, independent reviewer and director role evidence; unchanged model/data.

## 0.11.4 · 2026-10-07

- Load6more fixtures per click on league and team schedules.
- Link team upcoming fixtures to exact internal previews using #preview=matchId.
- Preserve selected fixtures outside the initial three, reload and language switching.

## 0.11.3 · 2026-10-07

- Responsive metric card columns sized to nested match panels.
- Borderless readable labels, Korean word wrapping and unbroken numerical values.
- Preserve explanation popovers, pixel headings/numbers and bilingual pages.

## 0.11.2 · 2026-10-07

- Continuous ground-ball routes for passes, carries, shots and kickoff returns.
- Ball-reactive formation movement, defensive tracking and visible running; 11 players per side preserved.
- Remove the complete score-sampling footer in both locales.
- Preserve logistic probabilities, learned score grids and all previous viewer versions.

# Release history / 변경 이력

## 0.9.1 — 2026-10-06

- Include CSS in UTF-8/LF publication-hash normalization, preventing unchanged stylesheets from failing after Windows CRLF checkout. Preserve the exact 0.9.0 manifest as the baseline.
- CSS 줄바꿈 차이에 따른 파일 검사 오류만 수정합니다. v23 한영 화면·각 팀 11명 재생·모델·확률·수집 자료는 동일합니다.
- Validate LF/CRLF hash equivalence in memory and rerun the publication audit; no paid API call or new visual test is performed.

## 0.9.0 — 2026-10-06

- Preserve v20 improved AI errors, v21 readable loss/draw colours, v22 experimental prediction/replay and v23 eleven-player correction in both languages.
- Each simulated team contains one goalkeeper and ten outfield players. Replay is illustrative, not real footage, player-level forecasting or a confirmed result.
- Publish pre-match v2 code, stored-input features, metrics and independent review; keep model_adopted false. Attack/defence/pressing/recent-five features use strictly earlier records, with prior-season/league smoothing for sparse history. No actual passing accuracy, odds or market values are silently added.
- 2025/26 accuracy 50.92% versus 45.79% league-frequency baseline; current LaLiga accuracy remains below baseline. Prior rank proxy ablation did not improve 2025/26 results; official rank and time-correct market value remain candidates.
- 한국어·영어 README/SPEC와 파일 해시를 갱신합니다. 각 팀 11명 수정·실험 확률·가상 재생을 포함하며 정식 모델 채택은 보류합니다. 실제 브라우저 재생·참가자 확인은 아직입니다.
- Automated evidence is stored alongside the relevant engine/model/viewer/server checks. Mocked-provider tests are not live Google verification. No external hosting or GitHub CI success is claimed.

## 0.8.0 — 2026-10-06

- Gemini local server, ignored local .env and empty public example; validated tool calls execute saved-record calculations.
- Bilingual async mode, key/configuration/error state, no browser secrets or invented probabilities. Preserve v19.
- 98 checks passed including 12 mocked-provider HTTP tests. Live Gemini verification awaits a user key; local server is not external hosting.


## 0.7.0 — 2026-10-06

- Bilingual recorded-data workbench: phrase interpretation, comparison/ranking/venue/trend, follow-ups, chart/table/calculation disclosure. Runs in browser JavaScript.
- Explicit unavailable prediction and unsupported-metric states; no LLM/SQL/Python execution or fabricated future probabilities.
- Service registration interface, three project skills, ownership and SPEC; broader pixel typography. Preserve v18 and prior releases.
- 15 engine + 48 Korean + 23 English checks passed (86 total). Actual browser confirmation pending.


## 0.6.0 — 2026-10-06

- Separate club and explicit Understat match links in completed-match lists.
- Remove provider/count badge; six bilingual detailed metric popovers; statistics unchanged.
- Preserve v17; 44 Korean and 19 English Node VM checks passed. Actual browser confirmation pending.


## 0.5.0 — 2026-10-06

- Add canonical English index.en.html alongside Korean index.html, preserving v16 in both languages.
- Translate all UI, filters, 47 StatMuse metric labels/definitions, reading tips and accessibility labels. Language links preserve selected-team hashes; other filters reset.
- Confirm 27 Premier League and 29 LaLiga historical/current clubs retain pixel logos and club colours. Statistical data and prediction adoption unchanged.
- 한·영 화면과 지표 설명 제공, 선택 팀을 유지하는 언어 전환. 한국어 40개·영어 15개 코드 검사 통과. 실제 화면·참가자 확인 전.


## 0.4.0 — 2026-10-06

- Adopt the 8-bit design as the canonical index.html and preserve v15.
- Render original logos for all 56 teams onto 24×24 grids, reuse loads, retain aspect ratios and fall back to initials on image/canvas failures. No logo raster files are rewritten.
- Update bilingual READMEs, selection, SPEC and hashes; preserve earlier design previews.
- 8비트 디자인을 기본 화면으로 채택. 56개 원본 팀 로고의 픽셀 표시·비율 유지·로딩 재사용·실패 대체 처리. 자료/모델 변경과 웹 호스팅 없음.
- Node VM: 40 checks passed; actual browser rendering and visual quality confirmation remain pending.

## 0.3.0 — 2026-10-06

- Preserve UI v01–v14: team colours/logos/history, match filters, 47 Korean metrics, click explanations, layout fixes and source/external-link removal.
- Add functioning soft-app and 8-bit previews, release SPEC, viewer selection and refreshed hashes.
- Publish archived baseline code/review while keeping service adoption false; no model improvement or deployment in this release.
- 화면 v01~v14 보존, 팀 정보·필터·한글 지표·말풍선·넘침 수정·외부 링크 제거. 부드러운/8비트 미리보기와 SPEC·버전 명세 추가. 모델 실험은 보존하되 서비스 채택은 보류.
- Actual browser rendering, administrator authentication, automatic refresh and user design acceptance remain pending.

## 0.2.1 — 2026-10-06

- Normalize manifest hashes to the published UTF-8/LF representation. No agent/data behavior changed.
- 공개 텍스트 줄바꿈 기준으로 파일 해시 보완. 에이전트/자료 동작 변경 없음.

## 0.2.0 — 2026-10-06

- Consolidated ten roles into five execution owners; retained independent review and final decision.
- Added ownership-aware approval adapter, six protocol tests, future-target policy and provider-neutral skills.
- Published bilingual entry documents, representative viewer and sanitized run evidence.
- 10역할→5담당 통합, 독립 검증/결재 유지, 담당 검사·6시험·미래경기 정책·영한 문서 추가.
- Five-agent actual execution, prediction models and automatic refresh remain unimplemented/unverified as documented.

## 0.1.0 — preserved 2026-10-06 snapshot

- Original ten-role package, contracts, validators and seven tests.
- Actual representative run is archived separately; it predates consolidation.
- 이전10역할 구성·공통계약·7시험 보존. 실제 대표2경기 실행은 통합이전 배정입니다.

Publication commits are made now; they do not reconstruct or backdate historical Git commits.

## 0.9.2 · 2026-10-07 · local
Internal completed-match routes in Korean and English; removed analyst calculation disclosure. All-team training scope clarified. No model deployment.

## 0.10.0 · 2026-10-07 · local
Selected logistic-111 model connected to641stored future fixtures and bilingual simulation. Updated model evidence. Score sampling remains illustrative fixed1:0/1:1/0:1; low scoring traced to this fallback. Previous0.9.2 preserved.

## 0.11.0 · 2026-10-07 · local
Trained Poisson count model on1518historical matches, conditioned score distributions on frozen logistic outcome probabilities. Bilingual score summaries and varied pixel replay scores. Preserved0.10.0.

## 0.11.1 · 2026-10-07 · local
Added broad player movement and player-linked ball paths, goal banners and kickoff. Internal model ID removed from user footer. Score distributions unchanged.
