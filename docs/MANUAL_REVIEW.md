# Manual Review

## Purpose

Automatic quality metrics can detect coverage, missing fields, duplicates, and label consistency. They cannot prove that an LLM-extracted observation is actually supported by the source report.

Manual review is used to estimate extraction quality on a small sample.

## Create A Review Sample

```bash
uv run python -m src.evaluation.create_manual_review_sample --sample-size 20
```

This creates:

```text
data/evaluation/manual_review_sample.csv
```

## Review Fields

Each sampled row contains the extracted observation plus blank review columns:

```text
is_supported_by_source
category_correct
severity_reasonable
recommendation_supported
review_notes
```

Suggested values:

```text
yes
partial
no
not_applicable
```

## How To Review

For each row:

1. Open the app.
2. Search for the observation or use the source report/page fields.
3. Expand the source report preview.
4. Check whether the extracted observation is supported by the cited page.
5. Fill in the review columns.

## Suggested Metrics

After reviewing 20 rows, estimate:

```text
support rate = supported observations / reviewed observations
category accuracy = category_correct yes / reviewed observations
severity reasonableness = severity_reasonable yes / reviewed observations
recommendation support = recommendation_supported yes / rows with recommendations
```

## Current Assisted Review Sample

A 20-row assisted review sample was created at:

```text
data/evaluation/manual_review_sample.csv
```

Current review summary:

```text
Source support:
- yes: 13
- partial: 5
- no: 2

Category correctness:
- yes: 14
- partial: 4
- no: 2

Severity reasonableness:
- yes: 14
- partial: 3
- no: 3

Recommendation support:
- yes: 4
- partial: 1
- not_applicable: 15
```

Interpretation:

```text
Fully supported observations: 65.0%
Fully or partially supported observations: 90.0%
Fully or partially correct categories: 90.0%
Fully or partially reasonable severities: 85.0%
```

This is an assisted review and should be treated as a lightweight MVP evaluation, not a statistically representative accuracy study.

## Why This Matters

This makes the evaluation more credible because it acknowledges that LLM quality cannot be fully assessed with automatic schema checks alone.
