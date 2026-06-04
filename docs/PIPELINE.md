# Data Pipeline

## Inputs

Place public/sample inspection report PDFs in:

```text
data/raw/
```

## Outputs

For each PDF, the pipeline creates:

```text
data/extracted/<report_id>_text.json
data/extracted/<report_id>_observations.json
```

The Qdrant vector index is stored in:

```text
data/vector_store/qdrant/
```

## Run Text Extraction Only

```bash
uv run python -m src.pipeline.run_pipeline
```

This extracts page-level text and chunks for every PDF in `data/raw/`.

## Run Full Pipeline

```bash
uv run python -m src.pipeline.run_pipeline --run-llm --rebuild-index
```

This runs:

```text
PDF extraction
-> chunking
-> LLM observation extraction
-> Qdrant index rebuild
```

## Cost-Controlled Test Run

```bash
uv run python -m src.pipeline.run_pipeline --run-llm --rebuild-index --max-chunks-per-report 3
```

This limits LLM extraction to the first 3 chunks per report.

## Rerun Safety

The pipeline skips existing observation files by default to avoid unnecessary LLM calls.

To force reprocessing:

```bash
uv run python -m src.pipeline.run_pipeline --run-llm --rebuild-index --overwrite-observations
```

## Docker Pipeline

```bash
docker compose --profile pipeline run --rm pipeline
```

The Docker pipeline uses the mounted local `data/` folder, so outputs persist between runs.

