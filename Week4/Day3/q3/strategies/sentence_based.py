import re
from typing import List, Dict, Any
from utils.tokenizer import TokenizerUtils

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

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

class SentenceBasedChunker:
    """Sentence-based chunking strategy."""
    
    def __init__(self):
        self.tokenizer = TokenizerUtils()
        self.sentence_tokenizer = self._initialize_sentence_tokenizer()
    
    def _initialize_sentence_tokenizer(self):
        """Initialize the best available sentence tokenizer."""
        if NLTK_AVAILABLE:
            return 'nltk'
        elif SPACY_AVAILABLE:
            try:
                # Try to load a spaCy model
                import spacy
                nlp = spacy.load("en_core_web_sm")
                return nlp
            except (OSError, IOError):
                # Fallback to regex if no spaCy model available
                return 'regex'
        else:
            return 'regex'
    
    def chunk_text(self, text: str, sentences_per_chunk: int = 5) -> List[Dict[str, Any]]:
        """
        Chunk text by grouping sentences.
        
        Args:
            text: Input text to chunk
            sentences_per_chunk: Number of sentences per chunk
            
        Returns:
            List of chunk dictionaries with metadata
        """
        if not text:
            return []
        
        # Split into sentences
        sentences = self._split_into_sentences(text)
        if not sentences:
            return []
        
        chunks = []
        current_pos = 0
        
        # Group sentences into chunks
        for i in range(0, len(sentences), sentences_per_chunk):
            chunk_sentences = sentences[i:i + sentences_per_chunk]
            chunk_text = ' '.join(chunk_sentences)
            
            if not chunk_text.strip():
                continue
            
            # Calculate positions
            start_pos = text.find(chunk_sentences[0], current_pos)
            end_pos = start_pos + len(chunk_text)
            
            # Create chunk metadata
            chunk_data = {
                'content': chunk_text.strip(),
                'token_count': self.tokenizer.count_tokens(chunk_text),
                'start_pos': start_pos,
                'end_pos': end_pos,
                'overlap': 0,  # No overlap in sentence-based chunking by default
                'chunk_id': len(chunks),
                'strategy': 'sentence_based',
                'sentence_count': len(chunk_sentences)
            }
            
            chunks.append(chunk_data)
            current_pos = end_pos
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using the best available method."""
        if self.sentence_tokenizer == 'nltk':
            return self._split_with_nltk(text)
        elif hasattr(self.sentence_tokenizer, 'pipe'):  # spaCy model
            return self._split_with_spacy(text)
        else:
            return self._split_with_regex(text)
    
    def _split_with_nltk(self, text: str) -> List[str]:
        """Split text using NLTK sentence tokenizer."""
        try:
            sentences = sent_tokenize(text)
            return [s.strip() for s in sentences if s.strip()]
        except Exception:
            return self._split_with_regex(text)
    
    def _split_with_spacy(self, text: str) -> List[str]:
        """Split text using spaCy sentence tokenizer."""
        try:
            doc = self.sentence_tokenizer(text)
            sentences = [sent.text.strip() for sent in doc.sents]
            return [s for s in sentences if s]
        except Exception:
            return self._split_with_regex(text)
    
    def _split_with_regex(self, text: str) -> List[str]:
        """Split text using regex patterns (fallback method)."""
        # Simple sentence boundary detection
        # This is a basic implementation and may not be as accurate as NLTK or spaCy
        sentence_endings = r'[.!?]+'
        sentences = re.split(sentence_endings, text)
        
        # Clean up sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def chunk_text_with_overlap(self, text: str, sentences_per_chunk: int = 5, overlap_sentences: int = 1) -> List[Dict[str, Any]]:
        """
        Chunk text by sentences with overlap.
        
        Args:
            text: Input text to chunk
            sentences_per_chunk: Number of sentences per chunk
            overlap_sentences: Number of sentences to overlap between chunks
            
        Returns:
            List of chunk dictionaries with metadata
        """
        if not text:
            return []
        
        sentences = self._split_into_sentences(text)
        if not sentences:
            return []
        
        chunks = []
        current_pos = 0
        
        step_size = sentences_per_chunk - overlap_sentences
        
        for i in range(0, len(sentences), step_size):
            chunk_sentences = sentences[i:i + sentences_per_chunk]
            if not chunk_sentences:
                break
                
            chunk_text = ' '.join(chunk_sentences)
            
            # Calculate positions
            start_pos = text.find(chunk_sentences[0], current_pos)
            end_pos = start_pos + len(chunk_text)
            
            # Calculate actual overlap
            actual_overlap = 0
            if i > 0:
                actual_overlap = min(overlap_sentences, len(chunk_sentences))
            
            chunk_data = {
                'content': chunk_text.strip(),
                'token_count': self.tokenizer.count_tokens(chunk_text),
                'start_pos': start_pos,
                'end_pos': end_pos,
                'overlap': self.tokenizer.count_tokens(' '.join(chunk_sentences[:actual_overlap])),
                'chunk_id': len(chunks),
                'strategy': 'sentence_based',
                'sentence_count': len(chunk_sentences)
            }
            
            chunks.append(chunk_data)
            current_pos = end_pos - len(' '.join(chunk_sentences[:actual_overlap]))
            
            # Stop if we've processed all sentences
            if i + sentences_per_chunk >= len(sentences):
                break
        
        return chunks
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Return information about this chunking strategy."""
        return {
            'name': 'Sentence-Based Chunking',
            'description': 'Groups complete sentences together to maintain semantic coherence',
            'parameters': {
                'sentences_per_chunk': {
                    'type': 'int',
                    'description': 'Number of sentences per chunk',
                    'default': 5,
                    'range': [1, 20]
                }
            },
            'pros': [
                'Preserves sentence integrity',
                'Natural language boundaries',
                'Good readability',
                'Maintains local context'
            ],
            'cons': [
                'Variable chunk sizes',
                'Dependent on sentence detection accuracy',
                'May create very small/large chunks',
                'Language-specific challenges'
            ],
            'use_cases': [
                'Literature analysis',
                'Legal documents',
                'When sentence integrity matters',
                'Educational content processing'
            ]
        } 