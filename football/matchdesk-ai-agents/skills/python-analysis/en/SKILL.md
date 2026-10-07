---
name: python-analysis
description: Record actual execution and verification evidence for tables, charts and model outputs when connecting Python calculation tools to MatchDesk. Current HTML analysis uses JavaScript.
---

Use this skill when an actual Python execution tool is provided. Do not execute arbitrary user-entered code directly in a browser or server.

- Check the schema, units and missing values of SQL results or stored validated data. Generate outputs without modifying the data source.
- Execute calculations permitted by the tool through functions and return the numerical table used for the chart. Record library/code versions and execution success or failure.
- Independently compare sample-match source values, row counts, totals and the denominators of averages. Distinguish model outputs from aggregate values.
- Prediction is a separate tool. Do not mark a result as adopted without chronological training/validation separation, prevention of data leakage beyond the cutoff, baseline performance and a model version.
- Include a title, axes/legend, units and conditions in charts, and return the results table alongside them. Do not generate numerical natural-language explanations without evidence.
- Record the actual executed code and verification results in the SPEC. Before connection, do not claim execution occurred.

