# Building Inspection Intelligence

AI-powered inspection report intelligence for turning static building inspection PDFs into structured observations, searchable technical knowledge, and traceable source evidence.

## Problem

Building inspection reports contain valuable technical knowledge: defects, risks, recommendations, compliance observations, maintenance advice, and recurring patterns. In practice, this knowledge is often buried in long PDF reports and is difficult for inspectors or risk engineers to reuse when assessing a new issue.

For example, when an inspector sees water ingress near a roof or foundation, they may want to know:

- Have similar issues appeared in previous reports?
- What risks were identified?
- What recommendations were made?
- Which report and page supports the retrieved observation?

This project turns inspection reports into a small reusable engineering knowledge base.

## Target User

Primary user: building inspector or technical control engineer.

Secondary users:

- risk engineer
- asset manager
- insurance reviewer
- compliance auditor
- public authority reviewer

## Why This Is Relevant To SECO

SECO works with technical inspection, construction risk, compliance, and engineering knowledge. These activities generate large volumes of underused document data: inspection reports, observations, plans, photos, measurements, and recommendations.

This MVP demonstrates how historical inspection reports can become a searchable intelligence layer. It is designed to support faster retrieval of similar cases, more consistent recommendations, and better reuse of previous technical expertise.

## What The Product Does

The application lets a user search technical issues in natural language, such as:

```text
water leakage near roof
termite damage to timber structure
foundation drainage issue
electrical clearance compliance risk
```

The system retrieves similar observations from previous inspection reports and shows:

- observation type
- severity
- category
- location
- recommendation
- source report
- source page
- in-app preview of the cited PDF page

The source preview is intentionally shown inside the app instead of as a download-first workflow, because inspection reports may contain sensitive project information.

## Current Data

The current demo uses public/sample building inspection PDFs stored locally in:

```text
data/raw/
```

At the current stage, the project has been tested with 4 PDF reports. More reports can be added by dropping PDFs into `data/raw/` and rerunning the pipeline.

Generated outputs are stored locally:

```text
data/extracted/      # extracted page text, chunks, and observations
data/vector_store/   # local Qdrant vector store
```

These generated folders are ignored by Git.

## Pipeline

```text
PDF reports
-> page-level text extraction
-> text cleaning and chunking
-> LLM-based structured observation extraction
-> local JSON storage
-> local sentence-transformer embeddings
-> Qdrant vector index
-> semantic search
-> Streamlit user interface
```

## Architecture

```text
src/
├── app/
│   └── streamlit_app.py
├── embeddings/
│   ├── embedding_service.py
│   └── index_builder.py
├── evaluation/
│   └── summarize_observations.py
├── extraction/
│   ├── chunker.py
│   ├── llm_extractor.py
│   ├── pdf_loader.py
│   └── run_llm_extraction.py
├── models/
│   ├── observation.py
│   └── report.py
├── pipeline/
│   └── run_pipeline.py
├── retrieval/
│   └── search_service.py
└── utils/
    ├── config.py
    └── file_utils.py
```

## Technical Decisions

### Python and uv

The project uses Python with `uv` for dependency management because the challenge is data and AI heavy, and reproducibility matters.

### PyMuPDF

PyMuPDF is used for PDF text extraction and in-app page rendering. It provides reliable page-level extraction and allows the UI to preview cited source pages without requiring file downloads.

### Pydantic

Pydantic models define the expected report and observation schemas. This prevents unstructured LLM output from silently entering the pipeline.

### Groq LLM API

Groq is used for LLM-based extraction because it is fast, easy to test, and suitable for a demo. API credentials are loaded from `.env` and never committed.

### Local Embeddings

The project uses `BAAI/bge-small-en-v1.5` through SentenceTransformers for local embeddings. This keeps semantic search reproducible and avoids relying on paid embedding APIs.

### Qdrant

Qdrant is used as the vector database because it gives a production-style retrieval layer while still supporting local development. It also maps well to a future Docker Compose setup.

### Streamlit

Streamlit was chosen for the MVP to prioritize a working end-to-end data and AI product within the time budget. In production, the frontend could be rebuilt in React or Next.js to align with SECO's stack and support richer client-facing workflows.

## Setup

Install dependencies:

```bash
uv sync
```

Create a local `.env` file:

```bash
cp .env.example .env
```

Then add your Groq API key:

```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

## Run The Pipeline

Extract page text and chunks for all PDFs in `data/raw/`:

```bash
uv run python -m src.pipeline.run_pipeline
```

Run LLM extraction and rebuild the vector index:

```bash
uv run python -m src.pipeline.run_pipeline --run-llm --rebuild-index
```

For a cheaper test run, limit the number of chunks sent to the LLM:

```bash
uv run python -m src.pipeline.run_pipeline --run-llm --rebuild-index --max-chunks-per-report 3
```

## Run Quality Checks

```bash
uv run python -m src.evaluation.summarize_observations
```

The quality report includes:

- report coverage
- observation completeness
- duplicate observation rate
- unknown severity rate
- unknown location rate
- missing recommendation rate
- invalid schema value rate
- category consistency signals

This helps evaluate the quality of the extracted AI data before relying on it in the search app.

## Run The App

```bash
uv run streamlit run src/app/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

The app supports:

- natural-language semantic search
- filters by observation type, severity, category, and source report
- source report and source page traceability
- in-app preview of cited PDF pages

## Run With Docker

Docker is provided so a non-technical reviewer can run the app without installing Python dependencies locally.

First, create `.env` from the example file:

```bash
cp .env.example .env
```

Add your Groq API key to `.env`, then put PDF reports in:

```text
data/raw/
```

Run the data pipeline inside Docker:

```bash
docker compose --profile pipeline run --rm pipeline
```

Start the app:

```bash
docker compose up --build app
```

Open:

```text
http://localhost:8501
```

The `data/` folder is mounted into the container, so extracted files and the local vector store persist between runs.

## Trade-Offs

What is production-like:

- modular pipeline structure
- typed schemas with Pydantic
- local vector database with Qdrant
- automated quality checks
- traceable source page previews

What is intentionally MVP:

- Streamlit instead of React
- local JSON instead of PostgreSQL
- local Qdrant storage instead of managed vector infrastructure
- limited document set
- no OCR for scanned PDFs
- no user authentication

## What I Would Keep In Production

- schema-first extraction design
- source traceability to report and page
- automated extraction quality checks
- vector search for similar historical observations
- Qdrant or another production vector store

## What I Would Replace In Production

- replace local JSON with PostgreSQL or a lakehouse table
- add OCR for scanned or image-heavy reports
- move LLM extraction to an asynchronous job queue
- add a React/Next.js frontend
- add authentication, access control, and audit logging
- add document-level permissions for sensitive reports

## Three-Month Roadmap

1. Add more public inspection reports and normalize the observation taxonomy.
2. Add human review sampling to estimate extraction precision.
3. Add OCR support for scanned reports.
4. Add trend dashboards for recurring defects, categories, and risk levels.
5. Add a React/Next.js frontend with role-based access.
6. Add Docker Compose and a production-style Qdrant service.
7. Add an insight layer that summarizes recurring risks and recommended actions from retrieved cases.

## Current Limitations

- The extraction quality depends on the quality of PDF text extraction.
- The LLM may produce inconsistent category labels, so taxonomy normalization is needed.
- The current dataset is small compared with a real SECO-scale repository.
- The system does not yet support images, plans, or scanned documents.

## Demo Narrative

An inspector can search for a new technical issue, retrieve similar historical observations, inspect recommendations made in previous reports, and verify the source evidence directly inside the app. This demonstrates how static inspection PDFs can become a reusable technical intelligence layer for construction risk and quality control.
