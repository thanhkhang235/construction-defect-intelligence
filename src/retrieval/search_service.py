from typing import Any

from src.embeddings.embedding_service import embed_texts
from src.embeddings.index_builder import get_qdrant_client
from src.utils.config import QDRANT_COLLECTION_NAME


def is_search_index_ready(collection_name: str = QDRANT_COLLECTION_NAME) -> bool:
    client = get_qdrant_client()
    is_ready = client.collection_exists(collection_name=collection_name)
    client.close()
    return is_ready


def search_similar_observations(
    query: str,
    limit: int = 5,
    collection_name: str = QDRANT_COLLECTION_NAME,
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
