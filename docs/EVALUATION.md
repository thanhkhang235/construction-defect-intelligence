# Evaluation

## Why Evaluation Matters

LLM extraction can produce structured data that looks plausible but still contains errors, duplicates, missing values, or inconsistent labels. This project includes automatic quality checks to evaluate the extracted dataset before relying on it in the search app.

## Run Quality Checks

```bash
uv run python -m src.evaluation.summarize_observations
```

## Automatic Metrics

The quality script reports:

- report coverage
- total observations
- observations by report
- observations by type
- severity distribution
- top categories
- empty reports
- missing descriptions
- missing source pages
- duplicate observation rate
- unknown severity rate
- unknown location rate
- missing recommendation rate
- invalid observation type rate
- invalid severity rate
- unique category count
- normalized category count
- category casing duplicate groups

## Interpretation

Useful signals:

- High report coverage means the extraction pipeline produced observations for most reports.
- High completeness means required fields are present.
- Duplicate rate detects stale files or repeated observations.
- Unknown severity and location rates reveal extraction uncertainty.
- Category inconsistency reveals where taxonomy normalization is needed.
- Normalized category count shows how noisy LLM labels are mapped into a smaller inspection taxonomy.

## Current Limitation

These are automatic quality metrics, not ground-truth accuracy metrics. True precision/recall would require a manually reviewed sample of source pages and extracted observations.

## Next Evaluation Step

A production-grade workflow should add human review sampling:

```text
observation_id
source_report
source_page
is_supported_by_source
severity_correct
category_correct
notes
```

This would allow an estimated extraction precision score.

This repository includes a lightweight manual review workflow in [Manual review](MANUAL_REVIEW.md).
