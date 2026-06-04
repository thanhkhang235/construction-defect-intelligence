# Architecture

## System Flow

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

## Repository Structure

```text
src/
|-- app/
|   `-- streamlit_app.py
|-- embeddings/
|   |-- embedding_service.py
|   `-- index_builder.py
|-- evaluation/
|   `-- summarize_observations.py
|-- extraction/
|   |-- chunker.py
|   |-- llm_extractor.py
|   |-- pdf_loader.py
|   `-- run_llm_extraction.py
|-- models/
|   |-- observation.py
|   `-- report.py
|-- pipeline/
|   `-- run_pipeline.py
|-- retrieval/
|   `-- search_service.py
`-- utils/
    |-- config.py
    `-- file_utils.py
```

## Key Components

`extraction/`: extracts page text, chunks report text, and converts chunks into structured observations with an LLM.

`models/`: defines Pydantic schemas for reports, chunks, and observations.

`embeddings/`: creates local embeddings and builds the Qdrant vector index.

`retrieval/`: performs semantic search with optional metadata filters.

`evaluation/`: summarizes extraction quality and dataset consistency.

`app/`: Streamlit UI for searching observations and previewing source report pages.

## Storage

Raw PDFs:

```text
data/raw/
```

Generated JSON:

```text
data/extracted/
```

Local vector store:

```text
data/vector_store/
```

Generated data is intentionally ignored by Git.

