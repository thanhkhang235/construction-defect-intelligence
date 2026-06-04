import argparse
import csv
from pathlib import Path

from src.utils.config import EXTRACTED_DATA_DIR, PROJECT_ROOT
from src.utils.file_utils import load_json


DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "data/evaluation/manual_review_sample.csv"


def load_observations(extracted_dir: Path = EXTRACTED_DATA_DIR) -> list[dict]:
    observations = []
    for path in sorted(extracted_dir.glob("*_observations.json")):
        report = load_json(path)
        for observation in report["observations"]:
            observations.append(
                {
                    "report_id": report["report_id"],
                    "source_file": report["source_file"],
                    **observation,
                }
            )

    return observations


def create_manual_review_sample(
    sample_size: int = 20,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> None:
    observations = load_observations()
    if not observations:
        raise FileNotFoundError(
            "No observations found. Run the pipeline before creating a review sample."
        )

    step = max(1, len(observations) // sample_size)
    sampled_observations = observations[::step][:sample_size]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "observation_id",
                "source_file",
                "source_page",
                "observation_type",
                "category",
                "severity",
                "location",
                "description",
                "recommendation",
                "is_supported_by_source",
                "category_correct",
                "severity_reasonable",
                "recommendation_supported",
                "review_notes",
            ],
        )
        writer.writeheader()
        for observation in sampled_observations:
            writer.writerow(
                {
                    "observation_id": observation.get("observation_id"),
                    "source_file": observation.get("source_file"),
                    "source_page": observation.get("source_page"),
                    "observation_type": observation.get("observation_type"),
                    "category": observation.get("category"),
                    "severity": observation.get("severity"),
                    "location": observation.get("location"),
                    "description": observation.get("description"),
                    "recommendation": observation.get("recommendation"),
                    "is_supported_by_source": "",
                    "category_correct": "",
                    "severity_reasonable": "",
                    "recommendation_supported": "",
                    "review_notes": "",
                }
            )

    print(f"Manual review rows: {len(sampled_observations)}")
    print(f"Saved manual review sample to: {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a manual review CSV sample from extracted observations."
    )
    parser.add_argument("--sample-size", type=int, default=20)
    parser.add_argument(
        "--output-path",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    create_manual_review_sample(
        sample_size=args.sample_size,
        output_path=args.output_path,
    )
