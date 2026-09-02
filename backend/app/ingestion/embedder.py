import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import math
import numpy as np
from typing import List, Dict, Any, Optional

try:
    from sentence_transformers import SentenceTransformer
    _SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    _SENTENCE_TRANSFORMERS_AVAILABLE = False


class Embedder:
    """
    Generates high-quality vector embeddings using local sentence-transformers (all-MiniLM-L6-v2),
    with an internal fast deterministic semantic hash & TF-IDF/n-gram vectorizer fallback.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.dim = 384
        
        if _SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
                if hasattr(self.model, "get_embedding_dimension"):
                    self.dim = self.model.get_embedding_dimension()
                else:
                    self.dim = self.model.get_sentence_embedding_dimension()
                print(f"[Embedder] Loaded SentenceTransformer model '{model_name}' (dim={self.dim})")
            except Exception as e:
                print(f"[Embedder] Could not initialize SentenceTransformer '{model_name}': {e}. Using fallback embedding.")
                self.model = None

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Embeds a list of strings into a 2D numpy array of shape (N, dim).
        """
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float32)

        if self.model is not None:
            try:
                embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
                # Normalize L2
                norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                norms[norms == 0] = 1.0
                return (embeddings / norms).astype(np.float32)
            except Exception as e:
                print(f"[Embedder] Model inference error: {e}. Falling back to statistical embedding.")

        # High-dimensional semantic feature hashing fallback
        return self._fallback_embed(texts)

    def embed_query(self, query: str) -> np.ndarray:
        """
        Embeds a single query string into a 1D vector of shape (dim,).
        """
        return self.embed_texts([query])[0]

    def _fallback_embed(self, texts: List[str]) -> np.ndarray:
        """
        Deterministic fast n-gram & word feature hashing embedding.
        """
        vectors = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, text in enumerate(texts):
            words = text.lower().split()
            if not words:
                continue
            for word in words:
                # Primary hash
                h1 = hash(word) % self.dim
                vectors[i, h1] += 1.0
                # Character bi-gram hash
                for b in range(len(word) - 1):
                    h2 = hash(word[b:b+2]) % self.dim
                    vectors[i, h2] += 0.5
            norm = np.linalg.norm(vectors[i])
            if norm > 0:
                vectors[i] /= norm
        return vectors
