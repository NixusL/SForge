from flask import Blueprint, render_template, request, redirect, url_for, current_app
from pathlib import Path

from src.ingestion.pdf_loader import extract_text_from_pdf
from src.ingestion.text_cleaner import normalize_whitespace
from src.nlp.chunking import split_into_chunks
from src.nlp.summarizer import Summarizer

main_bp = Blueprint("main", __name__)
summarizer = Summarizer()

@main_bp.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

@main_bp.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return redirect(url_for("main.index"))

    filename = uploaded_file.filename
    if not filename:
        return redirect(url_for("main.index"))

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    file_path = upload_folder / filename
    uploaded_file.save(file_path)

    # --- SAFETY LIMITS (prevents RAM blow-ups) ---
    MAX_PAGES = 10          # start small for simple PDFs
    MAX_TEXT_CHARS = 200_000
    MAX_CHUNKS = 300

    # 1) Extract (limit pages)
    raw_text = extract_text_from_pdf(str(file_path), max_pages=MAX_PAGES)
    print(f"[SForge] Raw extracted chars: {len(raw_text)}")

    # 2) Clean
    clean_text = normalize_whitespace(raw_text)
    print(f"[SForge] Clean chars: {len(clean_text)}")

    # Cap text size so chunking can’t explode
    if len(clean_text) > MAX_TEXT_CHARS:
        clean_text = clean_text[:MAX_TEXT_CHARS]
        print(f"[SForge] Clean text capped to {MAX_TEXT_CHARS} chars")

    # 3) Chunk (safe chunker should guarantee progress)
    chunks = split_into_chunks(clean_text, max_chars=1200, overlap=200)

    # Absolute cap on chunk count
    if len(chunks) > MAX_CHUNKS:
        chunks = chunks[:MAX_CHUNKS]
        print(f"[SForge] Chunks capped to {MAX_CHUNKS}")

    print(f"[SForge] Chunks: {len(chunks)}")

    # 4) Summarize (placeholder)
    summaries = summarizer.summarize_chunks(chunks)

    return render_template(
        "summaries.html",
        filename=filename,
        summaries=summaries,
        chunk_count=len(chunks),
        text_length=len(clean_text),
    )