from typing import List, Dict

def split_into_chunks(text: str, max_chars: int = 1200, overlap: int = 200) -> List[Dict]:
    if max_chars <= 0:
        raise ValueError("max_chars must be > 0")

    # Prevent overlap >= max_chars which can cause non-progress loops
    overlap = max(0, min(overlap, max_chars - 1))

    chunks: List[Dict] = []
    start = 0
    cid = 0
    n = len(text)

    while start < n:
        end = min(start + max_chars, n)
        chunks.append({"id": cid, "text": text[start:end]})
        cid += 1

        if end >= n:
            break

        next_start = end - overlap
        if next_start <= start:
            next_start = end  # force progress

        start = next_start

    return chunks