import argparse
from pathlib import Path

from src.embeddings.index_builder import build_qdrant_index_from_directory
from src.extraction.chunker import chunk_pages
from src.extraction.pdf_loader import extract_pdf_text
from src.extraction.run_llm_extraction import run_all_chunks_extraction
from src.models.report import ExtractedReport
from src.utils.config import EXTRACTED_DATA_DIR, RAW_DATA_DIR
from src.utils.file_utils import save_json


def get_report_text_output_path(pdf_path: Path) -> Path:
    return EXTRACTED_DATA_DIR / f"{pdf_path.stem}_text.json"


def extract_pdf_to_text_json(pdf_path: Path) -> Path:
    output_path = get_report_text_output_path(pdf_path)

    pages = extract_pdf_text(pdf_path)
    chunks = chunk_pages(pages)
    report = ExtractedReport.from_pdf_pages(pdf_path, pages, chunks)
    save_json(report.model_dump(), output_path)

    print(
        f"Extracted {pdf_path.name}: "
        f"{len(report.pages)} pages, {len(report.chunks)} chunks -> {output_path.name}"
    )
    return output_path


def extract_all_pdfs_to_text_json(raw_data_dir: Path = RAW_DATA_DIR) -> list[Path]:
    pdf_paths = sorted(raw_data_dir.glob("*.pdf"))
    if not pdf_paths:
        raise FileNotFoundError(f"No PDF files found in {raw_data_dir}")

    return [extract_pdf_to_text_json(pdf_path) for pdf_path in pdf_paths]


def run_data_pipeline(
    run_llm: bool = False,
    rebuild_index: bool = False,
    max_chunks_per_report: int | None = None,
) -> None:
    text_paths = extract_all_pdfs_to_text_json()

    if run_llm:
        for text_path in text_paths:
            run_all_chunks_extraction(
                input_path=text_path,
                max_chunks=max_chunks_per_report,
            )

    if rebuild_index:
        build_qdrant_index_from_directory()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the inspection report data pipeline.")
    parser.add_argument(
        "--run-llm",
        action="store_true",
        help="Extract structured observations from text chunks using Groq.",
    )
    parser.add_argument(
        "--rebuild-index",
        action="store_true",
        help="Rebuild the Qdrant vector index from observation JSON files.",
    )
    parser.add_argument(
        "--max-chunks-per-report",
        type=int,
        default=None,
        help="Limit LLM extraction cost while testing.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_data_pipeline(
        run_llm=args.run_llm,
        rebuild_index=args.rebuild_index,
        max_chunks_per_report=args.max_chunks_per_report,
    )
