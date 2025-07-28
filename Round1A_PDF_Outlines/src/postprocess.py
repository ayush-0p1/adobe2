from __future__ import annotations
from typing import List, Dict, Any
from .pdf_utils import Span

def build_outline(labeled: List[tuple[Span, float, str]], max_level: int = 3):
    outline = []
    for s, sc, lvl in labeled:
        if lvl not in ("H1", "H2", "H3"):
            continue
        outline.append({"level": lvl, "text": s.text.strip(), "page": s.page})
    return outline
