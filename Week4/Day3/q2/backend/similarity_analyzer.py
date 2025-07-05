from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple

class PlagiarismDetector:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the plagiarism detector with specified model."""
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = 0.8  # 80% threshold
        
    def analyze_texts(self, texts: List[str]) -> Dict:
        """
        Analyze multiple texts for plagiarism detection.
        
        Args:
            texts: List of text strings to analyze
            
        Returns:
            Dict containing similarity matrix and flagged pairs
        """
        # Generate embeddings for all texts
        embeddings = self.model.encode(texts)
        
        # Calculate cosine similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Convert to percentages and round
        similarity_percentages = np.round(similarity_matrix * 100, 2)
        
        # Find potential plagiarism pairs
        flagged_pairs = self._find_flagged_pairs(similarity_percentages)
        
        # Format results
        results = {
            "similarity_matrix": similarity_percentages.tolist(),
            "flagged_pairs": flagged_pairs,
            "text_count": len(texts),
            "threshold_percentage": self.similarity_threshold * 100,
            "highest_similarity": float(np.max(similarity_matrix[~np.eye(len(texts), dtype=bool)]))
        }
        
        return results
    
    def _find_flagged_pairs(self, similarity_matrix: np.ndarray) -> List[Dict]:
        """Find pairs of texts that exceed similarity threshold."""
        flagged_pairs = []
        n = len(similarity_matrix)
        
        for i in range(n):
            for j in range(i + 1, n):
                similarity = similarity_matrix[i][j]
                if similarity >= self.similarity_threshold * 100:  # Convert to percentage
                    flagged_pairs.append({
                        "text1_index": i,
                        "text2_index": j,
                        "similarity_percentage": float(similarity),
                        "status": "High Similarity - Potential Plagiarism"
                    })
        
        return flagged_pairs
    
    def preprocess_text(self, text: str) -> str:
        """Basic text preprocessing."""
        # Remove extra whitespace and normalize
        text = ' '.join(text.split())
        return text.strip() 