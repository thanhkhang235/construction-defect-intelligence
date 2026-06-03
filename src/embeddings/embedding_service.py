from functools import lru_cache

from sentence_transformers import SentenceTransformer

from src.utils.config import EMBEDDING_MODEL_NAME


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    model = get_embedding_model()
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()


def build_observation_text(observation: dict) -> str:
    fields = [
        observation.get("observation_type", ""),
        observation.get("category", ""),
        observation.get("severity", ""),
        observation.get("location", ""),
        observation.get("description", ""),
        observation.get("recommendation") or "",
    ]
    return " | ".join(field.strip() for field in fields if field and field.strip())
