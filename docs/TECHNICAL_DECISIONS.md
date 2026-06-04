# Technical Decisions

## Python And uv

Python is used because the project is data and AI heavy. `uv` is used for reproducible dependency management and fast environment setup.

## PyMuPDF

PyMuPDF handles PDF text extraction and source page rendering. It supports page-level extraction and lets the app preview cited report pages without forcing users to download source PDFs.

## Pydantic

Pydantic models define the schema for structured observations. This keeps LLM output constrained and validates important fields before data enters the retrieval layer.

## Category Normalization

The LLM can produce noisy category labels such as `Roof`, `Roofing`, `roofing`, or `Roof Covering`. The project keeps the original extracted category for transparency, but also maps it to a smaller canonical taxonomy for filtering and evaluation.

The taxonomy is also included in the LLM extraction prompt so new observations are encouraged to use canonical categories from the start. The rule-based normalizer remains as a safety net for legacy outputs and unexpected model responses.

## Groq

Groq is used for LLM extraction because it is fast and practical for a demo. The API key is stored in `.env` and excluded from Git.

The pipeline includes retry/backoff logic and skips existing observation files to avoid unnecessary API calls.

## SentenceTransformers

The project uses `BAAI/bge-small-en-v1.5` for local embeddings. This avoids paid embedding APIs and keeps semantic search reproducible.

## Qdrant

Qdrant is used as the vector database. It provides a production-style retrieval layer, metadata filtering, and a clear path to Docker Compose or managed deployment.

## Streamlit

Streamlit was chosen to prioritize a finished end-to-end MVP within the time budget. For production, a React or Next.js frontend would better match SECO's stack and support richer client-facing workflows.

## Docker

Docker support is included so non-technical users can run the app and pipeline without installing Python dependencies locally.

The app and pipeline are separate services because the pipeline may spend LLM API tokens, while opening the app should not silently trigger extraction.

## Trade-Offs

Production-like:

- modular pipeline
- typed schemas
- vector database
- quality checks
- source traceability
- Docker support

MVP limitations:

- local JSON instead of PostgreSQL
- local vector store instead of managed infrastructure
- Streamlit instead of React
- no OCR for scanned PDFs
- no authentication
- limited document set
