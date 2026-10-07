# MatchLab 0.18.1 / F1 0.6.1

- Source: https://github.com/Jordan-Soria/PitStops/tree/main/2026 (DHL-derived third-party transcription).
- Explicit session-to-file mapping for 13 completed GPs; never infer an event from country or round alone.
- Match unique normalized surname and exact lap within session; require positive stop time no greater than pit-lane duration.
- Fill null/absent stationary stop times only. Preserve OpenF1 non-null values. Log conflicts without overwrite.
- 276 filled rows, 37 source disagreements retained, one unmatched row excluded. Later completed GPs without source files remain unchanged.
- Cards display recorded/total count; partial averages explicitly marked in both languages. No stops vs unrecorded time distinguished.
- Provenance stored on supplemented rows; raw archived CSV and SHA in v10 verification. Provider reasons for discrepancies unverified.
- Prediction artifacts unchanged. Supplements are post-race records, not training inputs.
- Previous v09 and 0.18.0 UI preserved. Participant confirmation pending; no GitHub upload in this task.

Verification: source preservation PASS; pure metrics 15,877 checks PASS. Full-page and focused headless render verification not completed due machine memory pressure/timeouts. Previous v09 UI render checks do not certify this increment. Participant confirmation pending.

