from __future__ import annotations
from typing import List, Dict, Any
import numpy as np
import networkx as nx

def build_graph(vecs: np.ndarray, chunks: List[Dict[str, Any]], min_sim: float):
    G = nx.Graph()
    for i, ch in enumerate(chunks):
        G.add_node(i, doc=ch["doc"], page=ch["page"])
    sims = vecs @ vecs.T
    for i in range(len(chunks)):
        for j in range(i+1, len(chunks)):
            w = float((sims[i, j] + 1.0) / 2.0)
            if w >= min_sim:
                G.add_edge(i, j, weight=w)
    return G
