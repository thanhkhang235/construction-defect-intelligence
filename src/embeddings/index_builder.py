from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from src.embeddings.embedding_service import build_observation_text, embed_texts
from src.utils.config import (
    EXTRACTED_DATA_DIR,
    QDRANT_COLLECTION_NAME,
    QDRANT_LOCAL_PATH,
)
from src.utils.file_utils import load_json


DEFAULT_OBSERVATIONS_PATH = EXTRACTED_DATA_DIR / "sample_report_observations.json"
VECTOR_SIZE = 384


def get_qdrant_client(path: str | Path = QDRANT_LOCAL_PATH) -> QdrantClient:
    Path(path).mkdir(parents=True, exist_ok=True)
    return QdrantClient(path=str(path))


def build_qdrant_index_from_files(
    observations_paths: list[str | Path],
    collection_name: str = QDRANT_COLLECTION_NAME,
) -> None:
    client = get_qdrant_client()
    if client.collection_exists(collection_name=collection_name):
        client.delete_collection(collection_name=collection_name)

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )

    indexed_observations = []
    for observations_path in observations_paths:
        report = load_json(observations_path)
        for observation in report["observations"]:
            indexed_observations.append(
                {
                    "report_id": report["report_id"],
                    "source_file": report["source_file"],
                    **observation,
                }
            )

    observation_texts = [
        build_observation_text(observation) for observation in indexed_observations
    ]
    vectors = embed_texts(observation_texts)

    points = []
    for index, (observation, text, vector) in enumerate(
        zip(indexed_observations, observation_texts, vectors),
        start=1,
    ):
        payload = {
            "observation_text": text,
            **observation,
        }
        points.append(
            PointStruct(
                id=index,
                vector=vector,
                payload=payload,
            )
        )

    if points:
        client.upsert(collection_name=collection_name, points=points)

    print(f"Indexed observations: {len(points)}")
    print(f"Observation files: {len(observations_paths)}")
    print(f"Qdrant collection: {collection_name}")
    print(f"Qdrant local path: {QDRANT_LOCAL_PATH}")
    client.close()


def build_qdrant_index(
    observations_path: str | Path = DEFAULT_OBSERVATIONS_PATH,
    collection_name: str = QDRANT_COLLECTION_NAME,
) -> None:
    build_qdrant_index_from_files(
        observations_paths=[observations_path],
        collection_name=collection_name,
    )


def build_qdrant_index_from_directory(
    observations_dir: str | Path = EXTRACTED_DATA_DIR,
    collection_name: str = QDRANT_COLLECTION_NAME,
) -> None:
    paths = sorted(Path(observations_dir).glob("*_observations.json"))
    if not paths:
        raise FileNotFoundError(
            f"No observation files found in {observations_dir}. "
            "Run LLM extraction before building the vector index."
        )

    build_qdrant_index_from_files(
        observations_paths=paths,
        collection_name=collection_name,
    )


if __name__ == "__main__":
    build_qdrant_index()
