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
| `sample_report_1.pdf` | 15 | Building Inspection Report | https://www.inspectmyhome.com.au/assets/pdf/SAMPLE-BUILDING-REPORT.pdf | Public sample residential building inspection report. |
| `sample_report_2.pdf` | 21 | Sample Building Report July 2023 | https://compassqld.com.au/wp-content/uploads/2023/02/Sample-Building-Report-July-2023.pdf | Public sample residential building inspection report. |
| `sample_report_3.pdf` | 79 | Example Commercial Building Survey Report | https://allcottcommercial.co.uk/wp-content/uploads/2020/11/Example-commercial-building-survey-report.pdf | Public sample commercial building survey report. |
| `sample_report_4.pdf` | 30 | Sample Home Inspection Report | https://www.inspectionsbykeystone.com/pdf/sample-home-inspection.pdf | Public sample home inspection report. |

## Why These Sources Were Used

The goal of the take-home challenge is to demonstrate a reproducible data and AI pipeline on public construction-sector documents. Public sample reports are sufficient for the MVP because they contain realistic inspection language, findings, risks, recommendations, and source-page references.

## Data Handling Assumptions

- The dataset is used only for demonstration and technical evaluation.
- The reports are treated as public/sample documents.
- Generated extraction outputs are stored locally and ignored by Git.
- The app previews cited report pages inside the interface instead of encouraging downloads.

## Submission Note

The source URLs above document the public provenance of the sample reports used in the MVP. If additional PDFs are added to `data/raw/`, their source URLs should also be added to this table.
