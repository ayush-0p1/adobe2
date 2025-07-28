from __future__ import annotations
from typing import List, Dict, Any
import numpy as np
from rapidfuzz import fuzz

def cosine(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return (a @ b.T).squeeze()

def make_keyword_set(keywords: List[str]) -> set[str]:
    s = set()
    for k in keywords:
        for token in k.lower().split():
            if len(token) >= 3:
                s.add(token)
    return s

def keyword_boost(text: str, kwset: set[str], weight: float) -> float:
    t = text.lower()
    score = 0.0
    for k in kwset:
        if k in t: score += weight
    return min(0.5, score)

def heading_boost_fn(page: int, headings: Dict[int, List[str]], text: str, weight: float) -> float:
    cand = headings.get(page, [])
    best = 0
    for h in cand:
        best = max(best, fuzz.partial_ratio(h.lower(), text.lower())/100.0)
    return weight * best

def page_prior(page: int, decay: float) -> float:
    return max(0.0, 1.0 - decay * (page - 1))

def rank_chunks(persona_vec: np.ndarray, chunk_vecs: np.ndarray, chunks: List[Dict[str, Any]], cfg: Dict[str, Any], headings: Dict[int, List[str]], keywords: List[str]):
    sims = cosine(chunk_vecs, persona_vec.reshape(1,-1))
    sims = (sims + 1.0) / 2.0
    kwset = make_keyword_set(keywords)
    scores = []
    for i, ch in enumerate(chunks):
        base = float(sims[i])
        s = base
        s += keyword_boost(ch["text"], kwset, cfg["rank"]["keyword_boost"])
        s += heading_boost_fn(ch["page"], headings, ch["text"], cfg["rank"]["heading_boost"])
        s *= page_prior(ch["page"], cfg["rank"]["page_decay"])
        scores.append(s)
    order = np.argsort(-np.array(scores))
    top_k = int(cfg["rank"]["subsection_top_k"])
    return [(int(i), float(scores[i])) for i in order[:top_k]]
