from pathlib import Path
from typing import Any

from src.extraction.llm_extractor import extract_observations_from_chunk
from src.models.observation import Observation
from src.utils.config import EXTRACTED_DATA_DIR
from src.utils.file_utils import load_json, save_json


DEFAULT_INPUT_PATH = EXTRACTED_DATA_DIR / "sample_report_text.json"
DEFAULT_OUTPUT_PATH = EXTRACTED_DATA_DIR / "sample_report_observations.json"


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


def run_all_chunks_extraction(
    input_path: str | Path = DEFAULT_INPUT_PATH,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> list[Observation]:
    report = load_json(input_path)
    observations: list[Observation] = []

    for chunk in report["chunks"]:
        observations.extend(
            extract_observations_from_chunk(
                chunk=chunk,
                report_id=report["report_id"],
            )
        )

    _save_observations(report, observations, output_path)

    print(f"Processed chunks: {len(report['chunks'])}")
    print(f"Extracted observations: {len(observations)}")
    print(f"Saved observations to: {output_path}")

    return observations


if __name__ == "__main__":
    run_one_chunk_extraction(chunk_index=6)
    # run_all_chunks_extraction()
