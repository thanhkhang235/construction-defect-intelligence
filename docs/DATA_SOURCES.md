# Data Sources

## Current Dataset

The MVP uses public/sample building inspection report PDFs collected from the web for demonstration purposes. No confidential SECO data or private client data is used.

The reports are stored locally in:

```text
data/raw/
```

## Source Inventory

| File | Pages | Document title | Source URL | Notes |
| --- | ---: | --- | --- | --- |
| `sample_report_1.pdf` | 15 | Building Inspection Report | To document | Public/sample inspection report used for pipeline testing. |
| `sample_report_2.pdf` | 21 | Building inspection document | To document | Public/sample inspection report used for multi-report testing. |
| `sample_report_3.pdf` | 79 | Building Inspection Report | To document | Public/sample inspection report used for larger-report testing. |
| `sample_report_4.pdf` | 30 | Building Inspection Report | To document | Public/sample inspection report used for retrieval and UI testing. |

## Why These Sources Were Used

The goal of the take-home challenge is to demonstrate a reproducible data and AI pipeline on public construction-sector documents. Public sample reports are sufficient for the MVP because they contain realistic inspection language, findings, risks, recommendations, and source-page references.

## Data Handling Assumptions

- The dataset is used only for demonstration and technical evaluation.
- The reports are treated as public/sample documents.
- Generated extraction outputs are stored locally and ignored by Git.
- The app previews cited report pages inside the interface instead of encouraging downloads.

## Submission Note

Before final submission, each PDF should have its original source URL documented in the table above. Any report whose public provenance cannot be confirmed should be removed or replaced with a clearly documented public sample.

