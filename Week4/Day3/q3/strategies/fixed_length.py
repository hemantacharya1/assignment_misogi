from typing import List, Dict, Any
from utils.tokenizer import TokenizerUtils

class FixedLengthChunker:
    """Fixed-length token chunking strategy."""
    
    def __init__(self):
        self.tokenizer = TokenizerUtils()
    
    def chunk_text(self, text: str, chunk_size: int = 512) -> List[Dict[str, Any]]:
        """
        Chunk text into fixed-length token chunks.
        
        Args:
            text: Input text to chunk
            chunk_size: Number of tokens per chunk
            
        Returns:
            List of chunk dictionaries with metadata
        """
        if not text:
            return []
        
        chunks = []
        current_pos = 0
        
        # Split text by tokens
        token_chunks = self.tokenizer.split_by_tokens(text, chunk_size)
        
        for i, chunk_text in enumerate(token_chunks):
            if not chunk_text.strip():
                continue
            
            # Calculate positions
            start_pos = current_pos
            end_pos = current_pos + len(chunk_text)
            
            # Create chunk metadata
            chunk_data = {
                'content': chunk_text.strip(),
                'token_count': self.tokenizer.count_tokens(chunk_text),
                'start_pos': start_pos,
                'end_pos': end_pos,
                'overlap': 0,  # No overlap in fixed-length chunking
                'chunk_id': i,
                'strategy': 'fixed_length'
            }
            
            chunks.append(chunk_data)
            current_pos = end_pos
        
        return chunks
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Return information about this chunking strategy."""
        return {
            'name': 'Fixed-Length Token Chunking',
            'description': 'Splits text into chunks of exactly the specified number of tokens',
            'parameters': {
                'chunk_size': {
                    'type': 'int',
                    'description': 'Number of tokens per chunk',
                    'default': 512,
                    'range': [50, 2048]
                }
            },
            'pros': [
                'Predictable chunk sizes',
                'Simple to implement',
                'Good for consistent processing',
                'Memory efficient'
            ],
            'cons': [
                'May break sentences/paragraphs',
                'Context loss at boundaries',
                'Inflexible to content structure',
                'No semantic awareness'
            ],
            'use_cases': [
                'When you need consistent chunk sizes',
                'Simple RAG implementations',
                'Token-constrained models',
                'Batch processing requirements'
            ]
        } 