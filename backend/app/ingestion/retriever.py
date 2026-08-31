import numpy as np
from typing import List, Dict, Any, Optional

try:
    import faiss
    _FAISS_AVAILABLE = True
except ImportError:
    _FAISS_AVAILABLE = False

from .embedder import Embedder


class FAISSRetriever:
    """
    FAISS-powered vector store and retriever for ingested document chunks.
    Falls back gracefully to vectorized numpy cosine similarity if faiss is unavailable.
    """

    def __init__(self, embedder: Optional[Embedder] = None):
        self.embedder = embedder or Embedder()
        self.dim = self.embedder.dim
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None
        self.index = None
        
        if _FAISS_AVAILABLE:
            try:
                # Flat inner product (cosine similarity since embeddings are normalized)
                self.index = faiss.IndexFlatIP(self.dim)
            except Exception as e:
                print(f"[FAISSRetriever] Could not initialize FAISS index: {e}")
                self.index = None

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> None:
        """
        Embeds chunks and adds them to the vector index.
        """
        if not chunks:
            return

        texts = [c["text"] for c in chunks]
        new_embeddings = self.embedder.embed_texts(texts)

        start_idx = len(self.chunks)
        for i, chunk in enumerate(chunks):
            chunk_copy = dict(chunk)
            chunk_copy["index_id"] = start_idx + i
            self.chunks.append(chunk_copy)

        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])

        if self.index is not None:
            try:
                self.index.add(new_embeddings)
            except Exception as e:
                print(f"[FAISSRetriever] FAISS add error: {e}")

    def query(self, query_text: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """
        Searches for top_k most relevant chunks given a query string.
        """
        if not self.chunks or self.embeddings is None or len(self.chunks) == 0:
            return []

        top_k = min(top_k, len(self.chunks))
        query_vec = self.embedder.embed_query(query_text).reshape(1, -1)

        # 1. Try FAISS
        if self.index is not None and self.index.ntotal > 0:
            try:
                distances, indices = self.index.search(query_vec, top_k)
                results = []
                for score, idx in zip(distances[0], indices[0]):
                    if 0 <= idx < len(self.chunks):
                        res = dict(self.chunks[idx])
                        res["similarity_score"] = float(score)
                        results.append(res)
                return results
            except Exception as e:
                print(f"[FAISSRetriever] FAISS query error: {e}. Using NumPy fallback.")

        # 2. NumPy Cosine Similarity Fallback
        scores = np.dot(self.embeddings, query_vec.T).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            res = dict(self.chunks[idx])
            res["similarity_score"] = float(scores[idx])
            results.append(res)
        return results

    def get_combined_context(self, query_text: str, top_k: int = 4, max_words: int = 1500) -> str:
        """
        Retrieves top_k chunks and merges them into a clean LLM context block.
        """
        results = self.query(query_text, top_k=top_k)
        if not results:
            return ""

        context_blocks = []
        current_words = 0
        for r in results:
            text = r["text"]
            words = text.split()
            if current_words + len(words) > max_words and context_blocks:
                break
            context_blocks.append(f"--- [Page {r.get('page', 1)}] ---\n{text}")
            current_words += len(words)

        return "\n\n".join(context_blocks)
