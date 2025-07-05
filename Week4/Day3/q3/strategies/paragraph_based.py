import re
from typing import List, Dict, Any
from utils.tokenizer import TokenizerUtils

class ParagraphBasedChunker:
    """Paragraph-based chunking strategy."""
    
    def __init__(self):
        self.tokenizer = TokenizerUtils()
    
    def chunk_text(self, text: str, paragraphs_per_chunk: int = 1) -> List[Dict[str, Any]]:
        """
        Chunk text by grouping paragraphs.
        
        Args:
            text: Input text to chunk
            paragraphs_per_chunk: Number of paragraphs per chunk
            
        Returns:
            List of chunk dictionaries with metadata
        """
        if not text:
            return []
        
        # Split into paragraphs
        paragraphs = self._split_into_paragraphs(text)
        if not paragraphs:
            return []
        
        chunks = []
        current_pos = 0
        
        # Group paragraphs into chunks
        for i in range(0, len(paragraphs), paragraphs_per_chunk):
            chunk_paragraphs = paragraphs[i:i + paragraphs_per_chunk]
            chunk_text = '\n\n'.join(chunk_paragraphs)
            
            if not chunk_text.strip():
                continue
            
            # Calculate positions
            start_pos = text.find(chunk_paragraphs[0], current_pos)
            end_pos = start_pos + len(chunk_text)
            
            # Create chunk metadata
            chunk_data = {
                'content': chunk_text.strip(),
                'token_count': self.tokenizer.count_tokens(chunk_text),
                'start_pos': start_pos,
                'end_pos': end_pos,
                'overlap': 0,  # No overlap in paragraph-based chunking by default
                'chunk_id': len(chunks),
                'strategy': 'paragraph_based',
                'paragraph_count': len(chunk_paragraphs)
            }
            
            chunks.append(chunk_data)
            current_pos = end_pos
        
        return chunks
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs using various paragraph boundary indicators."""
        # Multiple strategies for paragraph detection
        
        # Strategy 1: Double newlines (most common)
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Filter out empty paragraphs
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        # If no paragraphs found using double newlines, try single newlines
        if len(paragraphs) <= 1:
            paragraphs = text.split('\n')
            paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        # If still no paragraphs, use sentence-based splitting as fallback
        if len(paragraphs) <= 1:
            paragraphs = self._split_by_sentence_groups(text)
        
        return paragraphs
    
    def _split_by_sentence_groups(self, text: str, sentences_per_group: int = 3) -> List[str]:
        """Split text into sentence groups as paragraph fallback."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Group sentences into pseudo-paragraphs
        paragraphs = []
        for i in range(0, len(sentences), sentences_per_group):
            group = sentences[i:i + sentences_per_group]
            if group:
                paragraphs.append('. '.join(group) + '.')
        
        return paragraphs
    
    def chunk_text_with_overlap(self, text: str, paragraphs_per_chunk: int = 1, overlap_paragraphs: int = 0) -> List[Dict[str, Any]]:
        """
        Chunk text by paragraphs with overlap.
        
        Args:
            text: Input text to chunk
            paragraphs_per_chunk: Number of paragraphs per chunk
            overlap_paragraphs: Number of paragraphs to overlap between chunks
            
        Returns:
            List of chunk dictionaries with metadata
        """
        if not text:
            return []
        
        if overlap_paragraphs >= paragraphs_per_chunk:
            overlap_paragraphs = max(0, paragraphs_per_chunk - 1)
        
        paragraphs = self._split_into_paragraphs(text)
        if not paragraphs:
            return []
        
        chunks = []
        current_pos = 0
        
        step_size = paragraphs_per_chunk - overlap_paragraphs
        
        for i in range(0, len(paragraphs), step_size):
            chunk_paragraphs = paragraphs[i:i + paragraphs_per_chunk]
            if not chunk_paragraphs:
                break
                
            chunk_text = '\n\n'.join(chunk_paragraphs)
            
            # Calculate positions
            start_pos = text.find(chunk_paragraphs[0], current_pos)
            end_pos = start_pos + len(chunk_text)
            
            # Calculate actual overlap
            actual_overlap = 0
            if i > 0:
                actual_overlap = min(overlap_paragraphs, len(chunk_paragraphs))
            
            chunk_data = {
                'content': chunk_text.strip(),
                'token_count': self.tokenizer.count_tokens(chunk_text),
                'start_pos': start_pos,
                'end_pos': end_pos,
                'overlap': self.tokenizer.count_tokens('\n\n'.join(chunk_paragraphs[:actual_overlap])),
                'chunk_id': len(chunks),
                'strategy': 'paragraph_based',
                'paragraph_count': len(chunk_paragraphs)
            }
            
            chunks.append(chunk_data)
            current_pos = end_pos - len('\n\n'.join(chunk_paragraphs[:actual_overlap]))
            
            # Stop if we've processed all paragraphs
            if i + paragraphs_per_chunk >= len(paragraphs):
                break
        
        return chunks
    
    def analyze_paragraph_structure(self, text: str) -> Dict[str, Any]:
        """Analyze the paragraph structure of the text."""
        paragraphs = self._split_into_paragraphs(text)
        
        if not paragraphs:
            return {
                'total_paragraphs': 0,
                'avg_paragraph_length': 0,
                'avg_tokens_per_paragraph': 0,
                'structure_quality': 'poor'
            }
        
        # Calculate statistics
        paragraph_lengths = [len(p) for p in paragraphs]
        paragraph_token_counts = [self.tokenizer.count_tokens(p) for p in paragraphs]
        
        avg_length = sum(paragraph_lengths) / len(paragraph_lengths)
        avg_tokens = sum(paragraph_token_counts) / len(paragraph_token_counts)
        
        # Determine structure quality
        length_variance = sum((l - avg_length) ** 2 for l in paragraph_lengths) / len(paragraph_lengths)
        
        if length_variance < avg_length * 0.5:
            quality = 'excellent'
        elif length_variance < avg_length:
            quality = 'good'
        elif length_variance < avg_length * 2:
            quality = 'fair'
        else:
            quality = 'poor'
        
        return {
            'total_paragraphs': len(paragraphs),
            'avg_paragraph_length': avg_length,
            'avg_tokens_per_paragraph': avg_tokens,
            'min_paragraph_length': min(paragraph_lengths),
            'max_paragraph_length': max(paragraph_lengths),
            'length_variance': length_variance,
            'structure_quality': quality
        }
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Return information about this chunking strategy."""
        return {
            'name': 'Paragraph-Based Chunking',
            'description': 'Splits text at paragraph boundaries to maintain topical coherence',
            'parameters': {
                'paragraphs_per_chunk': {
                    'type': 'int',
                    'description': 'Number of paragraphs per chunk',
                    'default': 1,
                    'range': [1, 10]
                }
            },
            'pros': [
                'Maintains topical coherence',
                'Natural document structure',
                'Good for structured documents',
                'Preserves author intent'
            ],
            'cons': [
                'Highly variable chunk sizes',
                'Depends on document formatting',
                'May create very large chunks',
                'Inconsistent paragraph detection'
            ],
            'use_cases': [
                'Academic papers',
                'Books and articles',
                'Well-structured documents',
                'Content with clear topical breaks'
            ]
        } 