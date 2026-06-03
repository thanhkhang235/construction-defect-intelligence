from typing import Any

from qdrant_client.models import FieldCondition, Filter, MatchValue

from src.embeddings.embedding_service import embed_texts
from src.embeddings.index_builder import get_qdrant_client
from src.utils.config import QDRANT_COLLECTION_NAME


def is_search_index_ready(collection_name: str = QDRANT_COLLECTION_NAME) -> bool:
    client = get_qdrant_client()
    is_ready = client.collection_exists(collection_name=collection_name)
    client.close()
    return is_ready


def build_metadata_filter(
    observation_types: list[str] | None = None,
    severities: list[str] | None = None,
    categories: list[str] | None = None,
    source_files: list[str] | None = None,
) -> Filter | None:
    conditions = []

    filter_fields = {
        "observation_type": observation_types,
        "severity": severities,
        "category": categories,
        "source_file": source_files,
    }

    for field_name, selected_values in filter_fields.items():
        values = [value for value in selected_values or [] if value]
        if not values:
            continue

        conditions.append(
            Filter(
                should=[
                    FieldCondition(
                        key=field_name,
                        match=MatchValue(value=value),
                    )
                    for value in values
                ]
            )
        )

    if not conditions:
        return None

    return Filter(must=conditions)


def get_filter_options(
    collection_name: str = QDRANT_COLLECTION_NAME,
) -> dict[str, list[str]]:
    client = get_qdrant_client()
    if not client.collection_exists(collection_name=collection_name):
        client.close()
        return {
            "observation_types": [],
            "severities": [],
            "categories": [],
            "source_files": [],
        }

    records, _ = client.scroll(
        collection_name=collection_name,
        limit=10_000,
        with_payload=True,
        with_vectors=False,
    )
    client.close()

    payloads = [record.payload or {} for record in records]
    return {
        "observation_types": sorted(
            {payload.get("observation_type") for payload in payloads if payload.get("observation_type")}
        ),
        "severities": sorted(
            {payload.get("severity") for payload in payloads if payload.get("severity")}
        ),
        "categories": sorted(
            {payload.get("category") for payload in payloads if payload.get("category")}
        ),
        "source_files": sorted(
            {payload.get("source_file") for payload in payloads if payload.get("source_file")}
        ),
    }


def search_similar_observations(
    query: str,
    limit: int = 5,
    collection_name: str = QDRANT_COLLECTION_NAME,
    observation_types: list[str] | None = None,
    severities: list[str] | None = None,
    categories: list[str] | None = None,
    source_files: list[str] | None = None,
) -> list[dict[str, Any]]:
    client = get_qdrant_client()
    if not client.collection_exists(collection_name=collection_name):
        client.close()
        raise RuntimeError(
            "Search index is missing. Run `uv run python -m src.embeddings.index_builder` first."
        )

    query_vector = embed_texts([query])[0]

    response = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=build_metadata_filter(
            observation_types=observation_types,
            severities=severities,
            categories=categories,
            source_files=source_files,
        ),
        limit=limit,
        with_payload=True,
    )
    client.close()

    return [
        {
            "score": result.score,
            **(result.payload or {}),
        }
        for result in response.points
    ]


if __name__ == "__main__":
    matches = search_similar_observations("water leakage near roof", limit=3)

    for index, match in enumerate(matches, start=1):
        print(f"\nResult {index}")
        print(f"Score: {match['score']:.4f}")
        print(f"Type: {match['observation_type']}")
        print(f"Category: {match['category']}")
        print(f"Severity: {match['severity']}")
        print(f"Source page: {match['source_page']}")
        print(f"Description: {match['description']}")
        print(f"Recommendation: {match.get('recommendation')}")
