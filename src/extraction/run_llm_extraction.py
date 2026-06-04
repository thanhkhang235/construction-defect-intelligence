import time
from pathlib import Path
from typing import Any

from src.extraction.llm_extractor import extract_observations_from_chunk
from src.models.observation import Observation
from src.utils.config import EXTRACTED_DATA_DIR
from src.utils.file_utils import load_json, save_json


DEFAULT_INPUT_PATH = EXTRACTED_DATA_DIR / "sample_report_text.json"
DEFAULT_OUTPUT_PATH = EXTRACTED_DATA_DIR / "sample_report_observations.json"
DEFAULT_CHUNK_DELAY_SECONDS = 1.0


def get_observations_output_path(input_path: str | Path) -> Path:
    path = Path(input_path)
    report_id = path.name.removesuffix("_text.json")
    return EXTRACTED_DATA_DIR / f"{report_id}_observations.json"


def _save_observations(
    report: dict[str, Any],
    observations: list[Observation],
    output_path: str | Path,
) -> None:
    output = {
        "report_id": report["report_id"],
        "source_file": report["source_file"],
        "observations": [observation.model_dump() for observation in observations],
    }
    save_json(output, output_path)


def run_one_chunk_extraction(
    chunk_index: int,
    input_path: str | Path = DEFAULT_INPUT_PATH,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> list[Observation]:
    report = load_json(input_path)
    chunk = report["chunks"][chunk_index]

    observations = extract_observations_from_chunk(
        chunk=chunk,
        report_id=report["report_id"],
    )
    _save_observations(report, observations, output_path)

    print(f"Processed chunk: {chunk['chunk_id']}")
    print(f"Source page: {chunk['source_page']}")
    print(f"Extracted observations: {len(observations)}")
    print(f"Saved observations to: {output_path}")

    return observations


def run_selected_chunks_extraction(
    chunk_indexes: list[int],
    input_path: str | Path = DEFAULT_INPUT_PATH,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> list[Observation]:
    report = load_json(input_path)
    observations: list[Observation] = []

    for chunk_index in chunk_indexes:
        chunk = report["chunks"][chunk_index]
        observations.extend(
            extract_observations_from_chunk(
                chunk=chunk,
                report_id=report["report_id"],
            )
        )
        print(f"Processed chunk: {chunk['chunk_id']}")

    _save_observations(report, observations, output_path)

    print(f"Selected chunk indexes: {chunk_indexes}")
    print(f"Extracted observations: {len(observations)}")
    print(f"Saved observations to: {output_path}")

    return observations


def run_all_chunks_extraction(
    input_path: str | Path = DEFAULT_INPUT_PATH,
    output_path: str | Path | None = None,
    max_chunks: int | None = None,
    delay_seconds: float = DEFAULT_CHUNK_DELAY_SECONDS,
) -> list[Observation]:
    report = load_json(input_path)
    output_path = output_path or get_observations_output_path(input_path)
    observations: list[Observation] = []

    chunks = report["chunks"][:max_chunks]
    for chunk_index, chunk in enumerate(chunks, start=1):
        observations.extend(
            extract_observations_from_chunk(
                chunk=chunk,
                report_id=report["report_id"],
            )
        )
        print(f"Processed chunk {chunk_index}/{len(chunks)}: {chunk['chunk_id']}")

        if delay_seconds > 0 and chunk_index < len(chunks):
            time.sleep(delay_seconds)

    _save_observations(report, observations, output_path)

    print(f"Processed chunks: {len(chunks)}")
    print(f"Extracted observations: {len(observations)}")
    print(f"Saved observations to: {output_path}")

    return observations


if __name__ == "__main__":
    run_selected_chunks_extraction(chunk_indexes=[6, 7, 8])
    # run_all_chunks_extraction()
