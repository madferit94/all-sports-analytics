# Verification and reproducibility

[English](README.md) | [한국어](README.ko.md)

[Full English report](report.md) · [한국어 보고서](report.ko.md). The published receipts show 77 passing source/analysis/PPT checks, 16 chart comparisons, 2,381 workbook values and image agreement across 13 PDF pages. Analysis inputs and final presentation are included; the approximately 107MB original full raw cache remains local.

## Run without raw cache

From the project directory, `python3 verify_saved_data.py` checks the published source CSVs with the standard library. Analysis scripts/notebooks require `analysis/requirements.txt` and use included CSVs. They do not need a fresh download.

## Full original-source and PPT audit

Activate the analysis environment and set the original cached snapshot directory:

```bash
export UNDERSTAT_RAW_CACHE="/path/to/original/understat_strikers_2025_26"
python verification/scripts/en/verify_pipeline.py
python verification/scripts/ko/verify_pipeline.py
```

The directory must contain `data/raw/leagues`, `data/raw/players` and their original `.meta.json` files. A new download may differ from the saved hashes. The environment variable replaces machine-specific hardcoded paths. Without that cache, the full audit stops with an explicit missing-cache message; it does not claim a successful raw check.

Executed notebook companions: [English](notebooks/en/verification.ipynb) · [Korean](notebooks/ko/verification.ipynb). Set the variable before starting Jupyter and run top-to-bottom. `verify_pipeline.py` at this directory is an English convenience entry point. Both language scripts share calculations and are independently editable.

## Evidence files

- `pipeline_validation.json`: individual source, calculation, selection, chart and workbook checks.
- `pdf_validation.json`: original final-export image comparison and PDF hash; the PDF is copied unchanged for this publication.
- `visual_corrections.json`: original display-correction receipt.
- `publication_validation.json`: relocated notebook execution, script parity, links and file hashes for this update.
- `league_representatives_crosscheck.sql`: independent SQLite representative selection.

Read the reports for definitions, source anomalies and limits. This checks saved-data consistency, not independently certified source events or the xG model. The deck was not tested in the Microsoft PowerPoint app.
