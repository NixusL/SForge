from typing import List, Dict

class Summarizer:
    def summarize_chunks(self, chunks: List[Dict]) -> List[Dict]:
        summaries = []
        for c in chunks:
            cleaned = " ".join(c["text"].split())
            summary = cleaned[:240] + ("..." if len(cleaned) > 240 else "")
            summaries.append({"chunk_id": c["id"], "summary": summary})
        return summaries