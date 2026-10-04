# Beyond Goals: bilingual striker analysis

[English](README.md) | [한국어](README.ko.md) · [Collection and source definitions](../README.md)

## Question and outcome

How do recorded central-forward candidates differ in non-penalty shot frequency, average chance quality and scoring conversion? This is a descriptive comparison of 181 candidates in five leagues for 2025/26, using the Understat snapshot saved on 3 October 2026. The 13-slide [English landscape PDF](../presentation/Beyond_Goals_EN_Landscape_verified.pdf) and [editable PPTX](../presentation/Beyond_Goals_EN_Landscape_verified.pptx) explain the results visually.

## Code and learning flow

| Material | English | Korean |
|---|---|---|
| Commented Python script | [Script](scripts/en/01_striker_shot_profiles.py) | [Script](scripts/ko/01_striker_shot_profiles.py) |
| Executed Jupyter companion | [Notebook](notebooks/en/01_striker_shot_profiles.ipynb) | [Notebook](notebooks/ko/01_striker_shot_profiles.ipynb) |

The script and notebook have identical Python logic within each language, excluding notebook display magic. English and Korean versions produce identical numerical CSVs. There are 16 stages: setup; load; validate; calculate; volume/quality; conversion; league distributions; quadrant cases; shot locations/composition; match consistency; minutes sensitivity; metric rankings/Q75 standouts; league representatives; labeled shot scatter; labeled conversion scatter; save evidence. Read the question before each cell, predict the denominator, then run and interpret the result. `# %%` separates script stages.

## Run

Use Python 3.11 (verified runtime: 3.11.4). From this `analysis` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/en/01_striker_shot_profiles.py
python scripts/ko/01_striker_shot_profiles.py
python -m ipykernel install --user --name striker-analysis --display-name "Striker Analysis"
python -m jupyterlab
```

Select that kernel and run notebook cells from top to bottom. Korean chart labels require AppleGothic, Malgun Gothic, Noto Sans CJK KR or NanumGothic. Each execution writes a new timestamped directory under `results/en` or `results/ko`. The [latest published results index](latest_results.json) identifies the verified run; rerunning code does not automatically republish the index or rebuild the PPT. Scripts and notebooks are independently editable, so compare their logic after learning edits.

## Data and metric definitions

The four inputs under `data/input` are copied from `../data/processed`, with matching SHA-256 hashes in `data/input_manifest.json`. The default cohort requires recorded central-forward eligibility, at least 900 minutes, at least one NP shot and passed QC. It includes all positions played in the selected league-season. Full details are in the collection README.

NP excludes penalty attempts and OwnGoal events; other set pieces remain included.

- NP shots/90 = NP shots ÷ minutes × 90.
- NP xG/shot = event-summed NP xG ÷ NP shots.
- NP xG/90 = event-summed NP xG ÷ minutes × 90.
- Observed conversion = NP goals ÷ NP shots × 100; expected conversion = NP xG/shot × 100.
- Goals above xG = NP goals − event-summed NP xG.

Pooled league rates use sums, not unweighted player-rate means. League percentiles cover selected candidates only. Lowering `MIN_MINUTES` alone cannot restore players absent from the prefiltered input. Use `forward_candidate_audit.csv` to rebuild a wider cohort and repeat joins and checks.

## Three different selection questions

| Selection | Rule | Purpose |
|---|---|---|
| Four contrasting cases | Split all 181 candidates by pooled median volume and quality; require 50+ NP shots; choose closest to quadrant median using cohort-standard-deviation-scaled squared distance | Explain contrasting profiles |
| Seven dual-metric standouts | 50+ NP shots and both metrics ≥ pooled cohort Q75, using linear quantiles | Identify frequent, higher-quality shooting profiles |
| One representative per league | 50+ NP shots; highest NP xG/90; ties by minutes descending, then numeric player ID ascending | Compare expected shooting production within each league |

The four cases are Hugo Ekitike (high/high), Ante Budimir (high/low), Rasmus Højlund (low/high) and Mateo Pellegrino (low/low). They are examples near their quadrant centers, not four best strikers. League representatives are Erling Haaland, Robert Lewandowski, Harry Kane, Nikola Krstovic and Pierre-Emerick Aubameyang. The complete player-summary table separately selects league scoring leaders by total goals, including penalties: Haaland, Mbappé, Kane, Lautaro Martínez and Esteban Lepaul. Neither selection implies league-adjusted overall ability.

## Results and verification

Each run exports eight PNG/SVG figures, numerical CSVs, `validation.json`, `findings.json`, `standout_findings.json` and league-selection evidence. `player_match_analysis.csv` retains every appearance through a left join, including zero-NP-shot matches. The 60+ rate means zero NP shots in an appearance lasting at least 60 minutes; it is not a rolling 60-minute interval. The match scatter includes all appearances.

The [verification folder](../verification/README.md) records 77 source/analysis/PPT checks, 16 native chart comparisons, 2,381 workbook values and PDF image agreement across 13 pages. Source duplicates affect 12 candidate rows, all excluded from the cohort. The full original raw cache remains local.

## Limits and next steps

This is one season of a saved provider snapshot. No team, opponent, game-state or league-strength adjustment, defensive analysis, independent match-event certification or xG calibration was performed. A conversion gap does not prove persistent finishing skill. Shot coordinates are normalized provider fractions, not metres or off-ball movements. The presentation has editable native charts, but it was not opened in the Microsoft PowerPoint app; use the verified PDF for posting. Next steps are external match-record checks and multi-season/context comparisons.
