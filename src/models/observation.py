from typing import Literal

from pydantic import BaseModel, Field


ObservationType = Literal[
    "finding",
    "risk",
    "recommendation",
    "compliance",
    "maintenance",
]

Severity = Literal["low", "medium", "high", "unknown"]


class Observation(BaseModel):
    observation_id: str
    observation_type: ObservationType
    category: str = Field(default="Unknown")
    severity: Severity = Field(default="unknown")
    location: str = Field(default="Unknown")
    description: str
    recommendation: str | None = None
    source_page: int

