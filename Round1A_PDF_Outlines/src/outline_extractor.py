from __future__ import annotations
from typing import Dict, Any
import yaml
from jsonschema import validate
from .pdf_utils import extract_spans
from .heuristics import select_candidates, dedup_and_merge, label_levels, infer_title
from .postprocess import build_outline
from .json_schema import SCHEMA
from .logging_utils import get_logger

log = get_logger("outline")

def extract_outline(pdf_path: str, cfg_path: str) -> Dict[str, Any]:
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    spans = extract_spans(pdf_path)
    if not spans:
        result = {"title": "", "outline": []}
        validate(result, SCHEMA)
        return result

    cand = select_candidates(spans, cfg)
    merged = dedup_and_merge(cand, cfg)
    labeled = label_levels(merged)
    title = infer_title(labeled, cfg)
    outline = build_outline(labeled, max_level=int(cfg["thresholds"]["max_h_level"]))

    result = {"title": title, "outline": outline}
    validate(result, SCHEMA)
    return result
