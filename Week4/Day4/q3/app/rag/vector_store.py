from typing import List, Dict, Tuple
import numpy as np

class VectorStore:
    """
    A simple in-memory vector store for semantic search using cosine similarity.
    Stores tuples of (id, vector, metadata).
    """

    def __init__(self):
        self.vectors: List[Tuple[str, List[float], Dict]] = []

    def add(self, id: str, vector: List[float], metadata: Dict):
        """
        Add a vector with its metadata to the store.
        """
        self.vectors.append((id, vector, metadata))

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """
        Search for top_k most similar vectors using cosine similarity.
        Returns a list of metadata dictionaries with similarity score.
        """
        def cosine_similarity(a, b):
            a, b = np.array(a), np.array(b)
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        similarities = []
        for id, vec, metadata in self.vectors:
            sim = cosine_similarity(query_vector, vec)
            similarities.append((sim, metadata))

        # Sort by similarity (high to low)
        similarities.sort(reverse=True, key=lambda x: x[0])

        return [item[1] | {"similarity": round(item[0], 4)} for item in similarities[:top_k]]
