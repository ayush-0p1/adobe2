from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
from rapidfuzz import fuzz

from .pdf_utils import Span
from .features import assign_level, heading_score, page_stats


def compute_size_cutoffs(spans: List[Span]) -> list[float]:
    sizes = np.array([s.size for s in spans], dtype=np.float32)
    if len(sizes) == 0:
        return [12.0, 10.0]
    p95 = float(np.percentile(sizes, 95))
    p80 = float(np.percentile(sizes, 80))
    if p95 <= p80:
        p95 = p80 + 0.5
    return [p95, p80]


def select_candidates(
    spans: List[Span], cfg: Dict[str, Any]
) -> List[Tuple[Span, float]]:
    stats = page_stats(spans)
    min_score = float(cfg["thresholds"]["min_score"])
    cand = []
    for s in spans:
        sc = heading_score(s, stats, cfg)
        if sc >= min_score:
            cand.append((s, sc))
    return cand


def dedup_and_merge(cand: List[tuple[Span, float]], cfg: Dict[str, Any]):
    cand = sorted(cand, key=lambda x: (x[0].page, x[0].y0))
    merged: List[tuple[Span, float]] = []
    fuzz_thr = int(cfg["postprocess"]["dedup_fuzz_ratio"])
    last = None
    for s, sc in cand:
        t = s.text.strip()
        if (
            last
            and s.page == last[0].page
            and fuzz.token_set_ratio(last[0].text, t) >= fuzz_thr
        ):
            continue
        merged.append((s, sc))
        last = (s, sc)
    return merged


def label_levels(merged: List[tuple[Span, float]]):
    if not merged:
        return []
    sizes = np.array([s.size for s, _ in merged], dtype=np.float32)
    p95 = float(np.percentile(sizes, 95))
    p80 = float(np.percentile(sizes, 80))
    cutoffs = [p95, p80]
    labeled = []
    for s, sc in merged:
        lvl = assign_level(s, cutoffs)
        labeled.append((s, sc, lvl))
    return labeled


def infer_title(
    labeled: List[tuple[Span, float, str]], cfg: Dict[str, Any]
) -> str:
    if not labeled:
        return ""
    top = max(labeled, key=lambda x: (x[2] == "H1", x[1], x[0].size))
    if top[1] >= float(cfg["postprocess"]["title_min_score"]):
        return top[0].text.strip()
    p12 = [x for x in labeled if x[0].page <= 2]
    if p12:
        return max(p12, key=lambda x: x[0].size)[0].text.strip()
    return top[0].text.strip()
