from __future__ import annotations
import networkx as nx
def export_graph(G: nx.Graph):
    data = []
    for u, v, d in G.edges(data=True):
        data.append({"u": int(u), "v": int(v), "w": float(d.get("weight", 1.0))})
    return data
