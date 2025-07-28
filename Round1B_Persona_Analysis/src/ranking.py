from __future__ import annotations

from typing import Any, Dict, List


def top_sections(
    chunks: List[Dict[str, Any]],
    ranked: List[tuple[int, float]],
    section_top_k: int,
) -> List[Dict[str, Any]]:
    page_best: Dict[tuple[str, int], tuple[float, Dict[str, Any]]] = {}
    for idx, score in ranked:
        ch = chunks[idx]
        key = (ch["doc"], ch["page"])
        if key not in page_best or score > page_best[key][0]:
            page_best[key] = (score, ch)
    items = sorted(page_best.items(), key=lambda x: -x[1][0])[:section_top_k]
    out = []
    rank = 1
    for (_, _), (score, ch) in items:
        out.append({
            "document": ch["doc"],
            "page": ch["page"],
            "section_title": ch.get("heading", ""),
            "importance_rank": rank,
            "score": float(score),
        })
        rank += 1
    return out
