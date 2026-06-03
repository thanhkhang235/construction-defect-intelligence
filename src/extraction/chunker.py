import re


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_pages(
    pages: list[dict],
    max_chars: int = 1800,
    overlap_chars: int = 200,
) -> list[dict]:
    chunks: list[dict] = []

    for page in pages:
        page_number = page["page"]
        text = clean_text(page["text"])
        if not text:
            continue

        start = 0
        chunk_number = 1
        while start < len(text):
            end = min(start + max_chars, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": f"page_{page_number:03d}_chunk_{chunk_number:03d}",
                        "source_page": page_number,
                        "text": chunk_text,
                    }
                )

            if end == len(text):
                break

            start = max(0, end - overlap_chars)
            chunk_number += 1

    return chunks
