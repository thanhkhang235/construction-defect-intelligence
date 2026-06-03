from pathlib import Path

from pydantic import BaseModel, Field

from src.models.observation import Observation


class PageText(BaseModel):
    page: int
    text: str


class TextChunk(BaseModel):
    chunk_id: str
    source_page: int
    text: str


class ExtractedReport(BaseModel):
    report_id: str
    source_file: str
    pages: list[PageText]
    chunks: list[TextChunk] = Field(default_factory=list)
    observations: list[Observation] = Field(default_factory=list)

    @classmethod
    def from_pdf_pages(
        cls,
        pdf_path: str | Path,
        pages: list[dict],
        chunks: list[dict] | None = None,
    ) -> "ExtractedReport":
        path = Path(pdf_path)
        return cls(
            report_id=path.stem,
            source_file=path.name,
            pages=[PageText(**page) for page in pages],
            chunks=[TextChunk(**chunk) for chunk in chunks or []],
        )
