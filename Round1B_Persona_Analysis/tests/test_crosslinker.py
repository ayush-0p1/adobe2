import numpy as np
from src.crosslinker import build_graph
def test_graph():
    vecs = np.eye(3, dtype="float32")
    chunks = [{"doc":"d","page":1},{"doc":"d","page":2},{"doc":"d","page":3}]
    G = build_graph(vecs, chunks, 0.0)
    assert G.number_of_nodes() == 3
