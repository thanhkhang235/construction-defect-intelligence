from collections import Counter, defaultdict
from pathlib import Path

from src.utils.config import EXTRACTED_DATA_DIR
from src.utils.file_utils import load_json


REQUIRED_OBSERVATION_FIELDS = [
    "observation_id",
    "observation_type",
    "description",
    "source_page",
]
VALID_OBSERVATION_TYPES = {
    "finding",
    "risk",
    "recommendation",
    "compliance",
    "maintenance",
}
VALID_SEVERITIES = {"low", "medium", "high", "unknown"}


def normalize_text(value: str | None) -> str:
    return " ".join((value or "").lower().split())


def format_rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"

    return f"{(numerator / denominator) * 100:.1f}%"


def load_observation_files(extracted_dir: Path = EXTRACTED_DATA_DIR) -> list[dict]:
    paths = sorted(extracted_dir.glob("*_observations.json"))
    reports = []

    for path in paths:
        report = load_json(path)
        report["_path"] = str(path)
        reports.append(report)

    return reports


def summarize_observations(extracted_dir: Path = EXTRACTED_DATA_DIR) -> None:
    reports = load_observation_files(extracted_dir)
    if not reports:
        raise FileNotFoundError(f"No observation files found in {extracted_dir}")

    all_observations = []
    observations_by_report = {}
    empty_reports = []

    for report in reports:
        observations = report.get("observations", [])
        observations_by_report[report["report_id"]] = len(observations)

        if not observations:
            empty_reports.append(report["report_id"])

        for observation in observations:
            all_observations.append(
                {
                    "report_id": report["report_id"],
                    "source_file": report["source_file"],
                    **observation,
                }
            )

    type_counts = Counter(
        observation.get("observation_type", "unknown") for observation in all_observations
    )
    severity_counts = Counter(
        observation.get("severity", "unknown") for observation in all_observations
    )
    category_counts = Counter(
        observation.get("category", "Unknown") for observation in all_observations
    )

    descriptions_by_text = defaultdict(list)
    missing_description_count = 0
    missing_page_count = 0

    for observation in all_observations:
        description = normalize_text(observation.get("description"))
        if not description:
            missing_description_count += 1
        else:
            descriptions_by_text[description].append(observation["observation_id"])

        if observation.get("source_page") is None:
            missing_page_count += 1

    duplicate_groups = {
        description: observation_ids
        for description, observation_ids in descriptions_by_text.items()
        if len(observation_ids) > 1
    }
    duplicate_observation_count = sum(
        len(observation_ids) - 1 for observation_ids in duplicate_groups.values()
    )

    complete_observation_count = sum(
        all(observation.get(field) is not None for field in REQUIRED_OBSERVATION_FIELDS)
        for observation in all_observations
    )
    unknown_severity_count = sum(
        observation.get("severity") == "unknown" for observation in all_observations
    )
    unknown_location_count = sum(
        normalize_text(observation.get("location")) in {"", "unknown"}
        for observation in all_observations
    )
    missing_recommendation_count = sum(
        not observation.get("recommendation") for observation in all_observations
    )
    average_observations_per_report = len(all_observations) / len(reports)
    invalid_type_count = sum(
        observation.get("observation_type") not in VALID_OBSERVATION_TYPES
        for observation in all_observations
    )
    invalid_severity_count = sum(
        observation.get("severity") not in VALID_SEVERITIES
        for observation in all_observations
    )
    unique_categories = set(category_counts)
    normalized_category_groups = defaultdict(set)
    for category in unique_categories:
        normalized_category_groups[normalize_text(category)].add(category)
    category_casing_duplicates = {
        normalized_category: variants
        for normalized_category, variants in normalized_category_groups.items()
        if len(variants) > 1
    }

    print("\nObservation Quality Summary")
    print("===========================")
    print(f"Observation files: {len(reports)}")
    print(f"Reports with observations: {len(reports) - len(empty_reports)}")
    print(f"Total observations: {len(all_observations)}")
    print(f"Empty reports: {len(empty_reports)}")
    print(f"Missing descriptions: {missing_description_count}")
    print(f"Missing source pages: {missing_page_count}")
    print(f"Duplicate description groups: {len(duplicate_groups)}")

    print("\nAutomatic Quality Metrics")
    print("-------------------------")
    print(
        "Report coverage: "
        f"{format_rate(len(reports) - len(empty_reports), len(reports))}"
    )
    print(
        "Observation completeness: "
        f"{format_rate(complete_observation_count, len(all_observations))}"
    )
    print(
        "Duplicate observation rate: "
        f"{format_rate(duplicate_observation_count, len(all_observations))}"
    )
    print(
        "Unknown severity rate: "
        f"{format_rate(unknown_severity_count, len(all_observations))}"
    )
    print(
        "Unknown location rate: "
        f"{format_rate(unknown_location_count, len(all_observations))}"
    )
    print(
        "Missing recommendation rate: "
        f"{format_rate(missing_recommendation_count, len(all_observations))}"
    )
    print(
        "Invalid observation type rate: "
        f"{format_rate(invalid_type_count, len(all_observations))}"
    )
    print(
        "Invalid severity rate: "
        f"{format_rate(invalid_severity_count, len(all_observations))}"
    )
    print(f"Unique categories: {len(unique_categories)}")
    print(f"Category casing duplicate groups: {len(category_casing_duplicates)}")
    print(f"Average observations per report: {average_observations_per_report:.1f}")

    print("\nObservations by report")
    print("----------------------")
    for report_id, count in sorted(observations_by_report.items()):
        print(f"{report_id}: {count}")

    print("\nObservation types")
    print("-----------------")
    for observation_type, count in type_counts.most_common():
        print(f"{observation_type}: {count}")

    print("\nSeverity")
    print("--------")
    for severity, count in severity_counts.most_common():
        print(f"{severity}: {count}")

    print("\nTop categories")
    print("--------------")
    for category, count in category_counts.most_common(15):
        print(f"{category}: {count}")

    if empty_reports:
        print("\nEmpty report IDs")
        print("----------------")
        for report_id in empty_reports:
            print(report_id)

    if duplicate_groups:
        print("\nDuplicate description examples")
        print("------------------------------")
        for description, observation_ids in list(duplicate_groups.items())[:5]:
            print(f"{description[:120]} -> {observation_ids}")

    if category_casing_duplicates:
        print("\nCategory casing duplicate examples")
        print("----------------------------------")
        for _, variants in list(category_casing_duplicates.items())[:10]:
            print(", ".join(sorted(variants)))


if __name__ == "__main__":
    summarize_observations()
