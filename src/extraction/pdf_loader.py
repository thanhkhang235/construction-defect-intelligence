from pathlib import Path
import fitz  # PyMuPDF


def extract_pdf_text(pdf_path: str | Path) -> list[dict]:
    """
    Extract text from a PDF page by page.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A list of dictionaries:
        [
            {
                "page": 1,
                "text": "..."
            }
        ]
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document = fitz.open(pdf_path)
    pages: list[dict] = []

    for page_index, page in enumerate(document):
        text = page.get_text("text").strip()

        pages.append(
            {
                "page": page_index + 1,
                "text": text,
            }
        )

    document.close()
    return pages