import numpy as np
from typing import List, Dict, Any, Optional
from utils.tokenizer import TokenizerUtils
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
import streamlit as st

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import nltk
    from nltk.tokenize import sent_tokenize
    NLTK_AVAILABLE = True
    
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
        
except ImportError:
    NLTK_AVAILABLE = False

class SemanticChunker:
    """Semantic chunking strategy using sentence embeddings."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.tokenizer = TokenizerUtils()
        self.model_name = model_name
        self.embedding_model = self._initialize_embedding_model()
        
    def _initialize_embedding_model(self):
        """Initialize the sentence embedding model."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            st.warning("Sentence Transformers not available. Semantic chunking will use fallback method.")
            return None
        
        try:
            model = SentenceTransformer(self.model_name)
            return model
        except Exception as e:
            st.warning(f"Failed to load embedding model: {str(e)}. Using fallback method.")
            return None
    
    def chunk_text(self, text: str, similarity_threshold: float = 0.7, max_chunk_size: int = 600) -> List[Dict[str, Any]]:
        """
        Chunk text using semantic similarity.
        
        Args:
            text: Input text to chunk
            similarity_threshold: Minimum similarity to group sentences
            max_chunk_size: Maximum tokens per chunk
            
        Returns:
            List of chunk dictionaries with metadata
        """
        if not text:
            return []
        
        if self.embedding_model is None:
            return self._fallback_chunking(text, max_chunk_size)
        
        # Split into sentences
        sentences = self._split_into_sentences(text)
        if not sentences:
            return []
        
        # Generate embeddings for all sentences
        embeddings = self._generate_embeddings(sentences)
        
        # Group semantically similar sentences
        sentence_groups = self._group_similar_sentences(
            sentences, embeddings, similarity_threshold
        )
        
        # Convert groups to chunks with size limits
        chunks = self._create_chunks_from_groups(
            sentence_groups, text, max_chunk_size
        )
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        if NLTK_AVAILABLE:
            try:
                sentences = sent_tokenize(text)
                return [s.strip() for s in sentences if s.strip()]
            except Exception:
                return self._simple_sentence_split(text)
        else:
            return self._simple_sentence_split(text)
    
    def _simple_sentence_split(self, text: str) -> List[str]:
        """Simple sentence splitting fallback."""
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _generate_embeddings(self, sentences: List[str]) -> np.ndarray:
        """Generate embeddings for sentences."""
        try:
            embeddings = self.embedding_model.encode(sentences)
            return embeddings
        except Exception as e:
            st.error(f"Error generating embeddings: {str(e)}")
            return np.random.rand(len(sentences), 384)  # Fallback random embeddings
    
    def _group_similar_sentences(self, sentences: List[str], embeddings: np.ndarray, 
                                 similarity_threshold: float) -> List[List[int]]:
        """Group sentences based on semantic similarity."""
        n_sentences = len(sentences)
        
        if n_sentences <= 1:
            return [[0]] if n_sentences == 1 else []
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Use hierarchical clustering
        # Convert similarity to distance
        distance_matrix = 1 - similarity_matrix
        
        # Set distance threshold based on similarity threshold
        distance_threshold = 1 - similarity_threshold
        
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=distance_threshold,
            linkage='average',
            metric='precomputed'
        )
        
        try:
            cluster_labels = clustering.fit_predict(distance_matrix)
        except Exception as e:
            # Fallback to simple sequential grouping
            st.warning(f"Clustering failed: {str(e)}. Using sequential grouping.")
            return self._sequential_grouping(sentences, embeddings, similarity_threshold)
        
        # Convert cluster labels to groups
        groups = {}
        for i, label in enumerate(cluster_labels):
            if label not in groups:
                groups[label] = []
            groups[label].append(i)
        
        return list(groups.values())
    
    def _sequential_grouping(self, sentences: List[str], embeddings: np.ndarray, 
                            similarity_threshold: float) -> List[List[int]]:
        """Sequential grouping fallback method."""
        groups = []
        current_group = [0]
        
        for i in range(1, len(sentences)):
            # Calculate similarity with the last sentence in current group
            similarity = cosine_similarity(
                embeddings[current_group[-1]].reshape(1, -1),
                embeddings[i].reshape(1, -1)
            )[0, 0]
            
            if similarity >= similarity_threshold:
                current_group.append(i)
            else:
                groups.append(current_group)
                current_group = [i]
        
        if current_group:
            groups.append(current_group)
        
        return groups
    
    def _create_chunks_from_groups(self, sentence_groups: List[List[int]], 
                                   text: str, max_chunk_size: int) -> List[Dict[str, Any]]:
        """Create chunks from sentence groups with size limits."""
        chunks = []
        sentences = self._split_into_sentences(text)
        
        for group_idx, sentence_indices in enumerate(sentence_groups):
            group_sentences = [sentences[i] for i in sentence_indices]
            
            # Check if group exceeds max size
            group_text = ' '.join(group_sentences)
            group_tokens = self.tokenizer.count_tokens(group_text)
            
            if group_tokens <= max_chunk_size:
                # Group fits in one chunk
                chunk_data = self._create_chunk_data(
                    group_text, text, len(chunks), group_idx
                )
                chunks.append(chunk_data)
            else:
                # Split large group into multiple chunks
                sub_chunks = self._split_large_group(
                    group_sentences, max_chunk_size, text, len(chunks), group_idx
                )
                chunks.extend(sub_chunks)
        
        return chunks
    
    def _split_large_group(self, sentences: List[str], max_chunk_size: int, 
                          text: str, chunk_id_start: int, group_id: int) -> List[Dict[str, Any]]:
        """Split a large semantic group into multiple chunks."""
        chunks = []
        current_chunk_sentences = []
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = self.tokenizer.count_tokens(sentence)
            
            if current_tokens + sentence_tokens <= max_chunk_size:
                current_chunk_sentences.append(sentence)
                current_tokens += sentence_tokens
            else:
                # Create chunk with current sentences
                if current_chunk_sentences:
                    chunk_text = ' '.join(current_chunk_sentences)
                    chunk_data = self._create_chunk_data(
                        chunk_text, text, chunk_id_start + len(chunks), group_id
                    )
                    chunks.append(chunk_data)
                
                # Start new chunk
                current_chunk_sentences = [sentence]
                current_tokens = sentence_tokens
        
        # Add remaining sentences
        if current_chunk_sentences:
            chunk_text = ' '.join(current_chunk_sentences)
            chunk_data = self._create_chunk_data(
                chunk_text, text, chunk_id_start + len(chunks), group_id
            )
            chunks.append(chunk_data)
        
        return chunks
    
    def _create_chunk_data(self, chunk_text: str, original_text: str, 
                          chunk_id: int, group_id: int) -> Dict[str, Any]:
        """Create chunk data dictionary."""
        # Find position in original text
        start_pos = original_text.find(chunk_text.split('.')[0])  # Approximate
        end_pos = start_pos + len(chunk_text)
        
        return {
            'content': chunk_text.strip(),
            'token_count': self.tokenizer.count_tokens(chunk_text),
            'start_pos': max(0, start_pos),
            'end_pos': end_pos,
            'overlap': 0,  # Semantic chunks don't have traditional overlap
            'chunk_id': chunk_id,
            'strategy': 'semantic_chunking',
            'semantic_group': group_id,
            'sentence_count': len(chunk_text.split('.'))
        }
    
    def _fallback_chunking(self, text: str, max_chunk_size: int) -> List[Dict[str, Any]]:
        """Fallback to sentence-based chunking when embeddings are unavailable."""
        sentences = self._split_into_sentences(text)
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = self.tokenizer.count_tokens(sentence)
            
            if current_tokens + sentence_tokens <= max_chunk_size:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
            else:
                # Create chunk
                if current_chunk:
                    chunk_text = ' '.join(current_chunk)
                    chunk_data = self._create_chunk_data(
                        chunk_text, text, len(chunks), len(chunks)
                    )
                    chunks.append(chunk_data)
                
                # Start new chunk
                current_chunk = [sentence]
                current_tokens = sentence_tokens
        
        # Add remaining sentences
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunk_data = self._create_chunk_data(
                chunk_text, text, len(chunks), len(chunks)
            )
            chunks.append(chunk_data)
        
        return chunks
    
    def analyze_semantic_coherence(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze semantic coherence of chunks."""
        if not chunks or self.embedding_model is None:
            return {'analysis': 'unavailable'}
        
        # Extract chunk texts
        chunk_texts = [chunk['content'] for chunk in chunks]
        
        # Generate embeddings
        embeddings = self._generate_embeddings(chunk_texts)
        
        # Calculate inter-chunk similarity
        similarity_matrix = cosine_similarity(embeddings)
        
        # Calculate metrics
        n_chunks = len(chunks)
        total_similarity = 0
        comparison_count = 0
        
        for i in range(n_chunks):
            for j in range(i + 1, n_chunks):
                total_similarity += similarity_matrix[i, j]
                comparison_count += 1
        
        avg_similarity = total_similarity / comparison_count if comparison_count > 0 else 0
        
        return {
            'average_inter_chunk_similarity': avg_similarity,
            'similarity_matrix': similarity_matrix.tolist(),
            'coherence_score': avg_similarity,
            'analysis': 'complete'
        }
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Return information about this chunking strategy."""
        return {
            'name': 'Semantic Chunking',
            'description': 'Groups semantically similar sentences using embedding similarity',
            'parameters': {
                'similarity_threshold': {
                    'type': 'float',
                    'description': 'Minimum similarity to group sentences',
                    'default': 0.7,
                    'range': [0.1, 0.9]
                },
                'max_chunk_size': {
                    'type': 'int',
                    'description': 'Maximum tokens per chunk',
                    'default': 600,
                    'range': [100, 1500]
                }
            },
            'pros': [
                'Maintains semantic coherence',
                'Adaptive to content',
                'Better retrieval quality',
                'Context-aware grouping'
            ],
            'cons': [
                'Computationally expensive',
                'Requires embedding models',
                'Complex implementation',
                'Variable processing time'
            ],
            'use_cases': [
                'High-quality RAG systems',
                'Complex documents',
                'When semantic coherence is priority',
                'Research and analysis tasks'
            ]
        } 