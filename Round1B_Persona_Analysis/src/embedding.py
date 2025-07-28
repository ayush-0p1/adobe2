from __future__ import annotations

from typing import List

import os
import numpy as np
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_dir: str):
        os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
        self.model = SentenceTransformer(model_dir, device="cpu")

    def encode(self, texts: List[str]) -> np.ndarray:
        emb = self.model.encode(texts, batch_size=64, convert_to_numpy=True, normalize_embeddings=True)
        return emb.astype("float32")
    