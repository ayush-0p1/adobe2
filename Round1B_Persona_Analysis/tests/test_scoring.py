import numpy as np
from src.scoring import rank_chunks
def test_rank_simple():
    p = np.ones((384,), dtype="float32") / np.sqrt(384)
    chunk_vecs = np.tile(p, (5,1))
    chunks = [{"text":"a", "page":1, "doc":"d"} for _ in range(5)]
    cfg = {"rank":{"subsection_top_k":3,"keyword_boost":0.1,"heading_boost":0.05,"page_decay":0.0}}
    ranked = rank_chunks(p, chunk_vecs, chunks, cfg, {}, ["a"])
    assert len(ranked) == 3
