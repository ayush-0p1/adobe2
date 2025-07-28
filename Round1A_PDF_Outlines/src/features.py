from __future__ import annotations
import numpy as np, re
from typing import List, Dict, Any
from .pdf_utils import Span

NUM_PAT = re.compile(r"^(\d+([\.\)])\s+|[A-Z]([\.\)])\s+|[ivxlcdm]+[\.\)]\s+)", re.I)
ROMAN_PAT = re.compile(r"^(?=[MDCLXVI])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})([\.)])\s*", re.I)
ALPHA_PAT = re.compile(r"^[A-Z][\.)]\s+")

def page_stats(spans: List[Span]):
    by_page: Dict[int, List[float]] = {}
    for s in spans:
        by_page.setdefault(s.page, []).append(s.size)
    stats = {}
    for p, arr in by_page.items():
        a = np.array(arr, dtype=np.float32)
        stats[p] = {
            "mean": float(a.mean()),
            "std": float(a.std() + 1e-6),
            "median": float(np.median(a)),
            "p90": float(np.percentile(a, 90)),
        }
    return stats

def detect_number_depth(text: str) -> int:
    txt = text.strip()
    if not txt: return 0
    if re.match(r"^(\d+\.){2,}\s*", txt): return 2
    if re.match(r"^\d+\.", txt): return 1
    if ROMAN_PAT.search(txt): return 1
    if ALPHA_PAT.search(txt): return 1
    if NUM_PAT.search(txt): return 1
    return 0

def heading_score(span: Span, stats: Dict[int, Dict[str, float]], cfg: Dict[str, Any]) -> float:
    st = stats[span.page]
    z = (span.size - st["median"]) / st["std"]
    size_feat = max(0.0, min(1.0, z / 2.5))
    bold_feat = 1.0 if span.bold else 0.0
    short_feat = 1.0 if span.line_len <= int(cfg["thresholds"]["shortline_max_chars"]) else 0.0
    indent_feat = 1.0 if span.x0 < 90 else (0.5 if span.x0 < 140 else 0.0)
    number_depth = detect_number_depth(span.text)
    number_feat = min(1.0, 0.5 * number_depth + (1.0 if NUM_PAT.search(span.text) else 0.0))
    caps_pen = 1.0 if span.text.isupper() and len(span.text) > 3 else 0.0
    punct_pen = 1.0 if span.text.endswith((':', ';', ',')) else 0.0

    w = cfg["score"]
    score = (
        w["size_weight"] * size_feat +
        w["bold_weight"] * bold_feat +
        w["shortline_weight"] * short_feat +
        w["number_weight"] * number_feat +
        w["indent_weight"] * indent_feat -
        w["caps_penalty"] * caps_pen -
        w["punct_penalty"] * punct_pen
    )
    return float(max(0.0, min(1.0, score)))

def assign_level(span: Span, size_cutoffs) -> str:
    size = span.size
    if size >= size_cutoffs[0]: return "H1"
    if size >= size_cutoffs[1]: return "H2"
    return "H3"
