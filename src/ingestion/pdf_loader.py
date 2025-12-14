from pathlib import Path
import pdfplumber

def extract_text_from_pdf(path: str, max_pages: int = 10) -> str:
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    parts = []
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages[:max_pages] if max_pages else pdf.pages
        for page in pages:
            txt = page.extract_text() or ""
            if txt.strip():
                parts.append(txt)

    return "\n".join(parts)