import json
import os
import time
from typing import Any

from groq import Groq, RateLimitError
from pydantic import BaseModel, Field, ValidationError

from src.models.observation import Observation
from src.utils.category_normalizer import get_canonical_categories
from src.utils.config import load_environment


class ExtractedObservationFields(BaseModel):
    observation_type: str
    category: str = Field(default="Unknown")
    severity: str = Field(default="unknown")
    location: str = Field(default="Unknown")
    description: str
    recommendation: str | None = None


class ObservationExtractionResponse(BaseModel):
    observations: list[ExtractedObservationFields] = Field(default_factory=list)


CANONICAL_CATEGORY_LIST = "\n".join(
    f"- {category}" for category in get_canonical_categories()
)

SYSTEM_PROMPT = f"""
You extract structured technical observations from building inspection report text.

Choose category from this controlled taxonomy only:
{CANONICAL_CATEGORY_LIST}

Return only valid JSON with this exact shape:
{{
  "observations": [
    {{
      "observation_type": "finding | risk | recommendation | compliance | maintenance",
      "category": "one controlled taxonomy category from the list above",
      "severity": "low | medium | high | unknown",
      "location": "building location or Unknown",
      "description": "specific observation from the text",
      "recommendation": "recommended action or null"
    }}
  ]
}}

Only extract observations that are clearly supported by the provided text.
If the text contains no technical observations, return {{"observations": []}}.
Do not invent new category names. If no category fits, use "Other".
""".strip()

MAX_RETRIES = 5
INITIAL_RETRY_DELAY_SECONDS = 2.0


def _get_groq_client() -> Groq:
    load_environment()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")

    return Groq(api_key=api_key)


def _get_groq_model() -> str:
    load_environment()
    model = os.getenv("GROQ_MODEL")
    if not model:
        raise RuntimeError("GROQ_MODEL is missing. Add it to your .env file.")

    return model


def _parse_json_response(content: str) -> dict[str, Any]:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(f"LLM response was not valid JSON: {content}") from error

    if not isinstance(parsed, dict):
        raise ValueError("LLM response must be a JSON object.")

    return parsed


def extract_observations_from_chunk(
    chunk: dict[str, Any],
    report_id: str,
) -> list[Observation]:
    client = _get_groq_client()
    model = _get_groq_model()

    response = None
    retry_delay = INITIAL_RETRY_DELAY_SECONDS
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": chunk["text"]},
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )
            break
        except RateLimitError:
            if attempt == MAX_RETRIES:
                raise

            print(
                f"Rate limit reached for {chunk['chunk_id']}. "
                f"Retrying in {retry_delay:.0f}s..."
            )
            time.sleep(retry_delay)
            retry_delay *= 2

    if response is None:
        raise RuntimeError(f"No LLM response received for {chunk['chunk_id']}.")

    content = response.choices[0].message.content or "{}"
    parsed_response = _parse_json_response(content)
    extraction = ObservationExtractionResponse(**parsed_response)

    observations: list[Observation] = []
    for index, extracted in enumerate(extraction.observations, start=1):
        observation_id = f"{report_id}_{chunk['chunk_id']}_{index:03d}"
        try:
            observations.append(
                Observation(
                    observation_id=observation_id,
                    source_page=chunk["source_page"],
                    **extracted.model_dump(),
                )
            )
        except ValidationError as error:
            raise ValueError(
                f"Invalid observation extracted from {chunk['chunk_id']}: "
                f"{extracted.model_dump()}"
            ) from error

    return observations
