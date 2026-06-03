from pathlib import Path

from src.extraction.pdf_loader import extract_pdf_text


def main() -> None:
    pdf_path = Path("data/raw/sample_report.pdf")

    pages = extract_pdf_text(pdf_path)

    print(f"Total pages extracted: {len(pages)}")
    print("\n--- First page preview ---\n")
    print(pages[0]["text"][:1000])


if __name__ == "__main__":
    main()