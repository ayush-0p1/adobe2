from __future__ import annotations
from typing import List, Dict

def chunk_pages(pages: List[str], max_chars: int, stride_chars: int, min_chars: int):
    chunks = []
    for idx, page in enumerate(pages, start=1):
        text = page.strip()
        if not text: continue
        i, n = 0, len(text)
        while i < n:
            j = min(n, i + max_chars)
            seg = text[i:j]
            if len(seg) >= min_chars:
                chunks.append({"page": idx, "text": seg})
            i += max(1, max_chars - stride_chars)
    return chunks
