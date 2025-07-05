from typing import List, Dict, Any
from utils.tokenizer import TokenizerUtils

class SlidingWindowChunker:
    """Sliding window chunking strategy with overlap."""
    
    def __init__(self):
        self.tokenizer = TokenizerUtils()
    
    def chunk_text(self, text: str, chunk_size: int = 512, overlap: int = 50) -> List[Dict[str, Any]]:
        """
        Chunk text using sliding window with overlap.
        
        Args:
            text: Input text to chunk
            chunk_size: Number of tokens per chunk
            overlap: Number of tokens to overlap between chunks
            
        Returns:
            List of chunk dictionaries with metadata
        """
        if not text:
            return []
        
        if overlap >= chunk_size:
            overlap = chunk_size // 2  # Ensure overlap is less than chunk size
        
        chunks = []
        current_pos = 0
        
        # Tokenize the entire text first
        if self.tokenizer.tokenizer is not None:
            tokens = self.tokenizer.tokenizer.encode(text)
            step_size = chunk_size - overlap
            
            for i in range(0, len(tokens), step_size):
                chunk_tokens = tokens[i:i + chunk_size]
                if len(chunk_tokens) == 0:
                    break
                
                # Decode tokens back to text
                chunk_text = self.tokenizer.tokenizer.decode(chunk_tokens)
                
                # Calculate positions (approximate)
                start_pos = current_pos
                end_pos = current_pos + len(chunk_text)
                
                # Calculate actual overlap for this chunk
                actual_overlap = 0
                if i > 0:
                    actual_overlap = min(overlap, len(chunk_tokens))
                
                chunk_data = {
                    'content': chunk_text.strip(),
                    'token_count': len(chunk_tokens),
                    'start_pos': start_pos,
                    'end_pos': end_pos,
                    'overlap': actual_overlap,
                    'chunk_id': len(chunks),
                    'strategy': 'sliding_window'
                }
                
                chunks.append(chunk_data)
                current_pos += len(chunk_text) - (actual_overlap * 2)  # Approximate position adjustment
                
                # Stop if we've reached the end
                if i + chunk_size >= len(tokens):
                    break
        
        else:
            # Fallback to word-based sliding window
            chunks = self._sliding_window_fallback(text, chunk_size, overlap)
        
        return chunks
    
    def _sliding_window_fallback(self, text: str, chunk_size: int, overlap: int) -> List[Dict[str, Any]]:
        """Fallback sliding window implementation using word-based estimation."""
        words = text.split()
        words_per_chunk = int(chunk_size / 0.75)  # Estimate: 0.75 tokens per word
        overlap_words = int(overlap / 0.75)
        
        chunks = []
        current_pos = 0
        step_size = words_per_chunk - overlap_words
        
        for i in range(0, len(words), step_size):
            chunk_words = words[i:i + words_per_chunk]
            if not chunk_words:
                break
                
            chunk_text = ' '.join(chunk_words)
            
            # Calculate positions
            start_pos = current_pos
            end_pos = current_pos + len(chunk_text)
            
            # Calculate actual overlap
            actual_overlap = 0
            if i > 0:
                actual_overlap = min(overlap_words, len(chunk_words))
            
            chunk_data = {
                'content': chunk_text,
                'token_count': self.tokenizer.count_tokens(chunk_text),
                'start_pos': start_pos,
                'end_pos': end_pos,
                'overlap': int(actual_overlap * 0.75),  # Convert back to estimated tokens
                'chunk_id': len(chunks),
                'strategy': 'sliding_window'
            }
            
            chunks.append(chunk_data)
            current_pos += len(chunk_text) - len(' '.join(chunk_words[:actual_overlap]))
            
            # Stop if we've processed all words
            if i + words_per_chunk >= len(words):
                break
        
        return chunks
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Return information about this chunking strategy."""
        return {
            'name': 'Sliding Window Chunking',
            'description': 'Creates overlapping chunks with specified overlap to maintain context',
            'parameters': {
                'chunk_size': {
                    'type': 'int',
                    'description': 'Number of tokens per chunk',
                    'default': 512,
                    'range': [50, 2048]
                },
                'overlap': {
                    'type': 'int',
                    'description': 'Number of tokens to overlap between chunks',
                    'default': 50,
                    'range': [0, 500]
                }
            },
            'pros': [
                'Maintains context across chunks',
                'Reduces information loss',
                'Better for question answering',
                'Handles boundary issues well'
            ],
            'cons': [
                'Increased storage requirements',
                'Processing overhead',
                'Potential redundancy',
                'Higher computational cost'
            ],
            'use_cases': [
                'Question answering systems',
                'When context preservation is crucial',
                'Complex document analysis',
                'Multi-step reasoning tasks'
            ]
        } 