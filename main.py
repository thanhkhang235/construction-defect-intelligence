from pathlib import Path

from src.extraction.chunker import chunk_pages
from src.extraction.pdf_loader import extract_pdf_text
from src.models.report import ExtractedReport
from src.utils.file_utils import save_json


def main() -> None:
    pdf_path = Path("data/raw/sample_report.pdf")
    output_path = Path("data/extracted/sample_report_text.json")

    pages = extract_pdf_text(pdf_path)
    chunks = chunk_pages(pages)
    report = ExtractedReport.from_pdf_pages(pdf_path, pages, chunks)

    save_json(report.model_dump(), output_path)

    print(f"Extracted {len(report.pages)} pages")
    print(f"Created {len(report.chunks)} text chunks")
    print(f"Saved report text to {output_path}")


if __name__ == "__main__":
    main()
