# Building Inspection Intelligence

AI-powered mini-product that turns building inspection PDF reports into structured observations, searchable technical knowledge, and traceable source evidence.

## Objective

Inspection reports contain valuable engineering knowledge, but the information is often buried in long static PDFs. This project helps inspectors and risk engineers retrieve similar historical observations, recommendations, and risks using semantic search.

The goal is to make previous inspection knowledge reusable instead of leaving it locked inside documents.

## Target User

Primary user:

- building inspector or technical control engineer

Secondary users:

- risk engineer
- asset manager
- insurance reviewer
- compliance auditor
- public authority reviewer

## Why This Matters To SECO

SECO works with technical inspection, construction risk, compliance, and engineering knowledge. These activities generate large volumes of underused document data. This MVP demonstrates how historical inspection reports can become a searchable intelligence layer for construction quality and risk control.

## Main Features

- Converts inspection PDFs into structured observations
- Enables semantic search across historical findings, risks, and recommendations
- Provides filters by severity, category, observation type, and source report
- Shows the cited report page directly in the app for traceability
- Includes automated quality checks for extracted observations
- Runs locally with Docker

## Quick Start With Docker

Docker is the recommended way to run the project if you do not want to install Python dependencies manually.

Create your environment file:

```bash
cp .env.example .env
```

Add your Groq API key to `.env`:

```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

The repository already includes sample public inspection PDFs in:

```text
data/raw/
```

The original report source URLs are documented in [Data sources](docs/DATA_SOURCES.md). To test with additional reports, add more PDF files to `data/raw/`. 

Run the data pipeline:

```bash
docker compose --profile pipeline run --rm pipeline
```

Start the app:

```bash
docker compose up app
```

Open:

```text
http://localhost:8501
```

## Local Development

Install dependencies:

```bash
uv sync
```

Run the pipeline:

```bash
uv run python -m src.pipeline.run_pipeline --run-llm --rebuild-index
```

Run a cheaper test pipeline:

```bash
uv run python -m src.pipeline.run_pipeline --run-llm --rebuild-index --max-chunks-per-report 3
```

Run quality checks:

```bash
uv run python -m src.evaluation.summarize_observations
```

Run the app:

```bash
uv run streamlit run src/app/streamlit_app.py
```

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

## Project Structure

```text
src/
|-- app/
|-- embeddings/
|-- evaluation/
|-- extraction/
|-- models/
|-- pipeline/
|-- retrieval/
`-- utils/
```

## Documentation

- [Product framing](docs/PRODUCT.md)
- [Data sources](docs/DATA_SOURCES.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Data pipeline](docs/PIPELINE.md)
- [Evaluation](docs/EVALUATION.md)
- [Manual review](docs/MANUAL_REVIEW.md)
- [Technical decisions](docs/TECHNICAL_DECISIONS.md)
- [Roadmap](docs/ROADMAP.md)

## Current Limitations

- The current dataset is small compared with a real SECO-scale repository.
- The extraction quality depends on PDF text quality.
- Category labels still need taxonomy normalization.
- OCR for scanned PDFs is not included in the MVP.
- Streamlit is used for speed; a production version would likely use React or Next.js.
