import re
from typing import List, Optional
import streamlit as st

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

class TokenizerUtils:
    """Utilities for tokenization and token counting."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        self.tokenizer = None
        self._initialize_tokenizer()
    
    def _initialize_tokenizer(self):
        """Initialize the tokenizer based on available libraries."""
        if TIKTOKEN_AVAILABLE:
            try:
                self.tokenizer = tiktoken.encoding_for_model(self.model_name)
            except KeyError:
                # Fallback to a default encoding if model not found
                self.tokenizer = tiktoken.get_encoding("cl100k_base")
        else:
            # Fallback to simple word-based tokenization
            self.tokenizer = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in the given text."""
        if not text:
            return 0
        
        if self.tokenizer is not None:
            try:
                return len(self.tokenizer.encode(text))
            except Exception as e:
                st.warning(f"Error with tiktoken: {str(e)}. Using word-based fallback.")
                return self._count_tokens_fallback(text)
        else:
            return self._count_tokens_fallback(text)
    
    def _count_tokens_fallback(self, text: str) -> int:
        """Fallback token counting using word-based estimation."""
        # Simple estimation: ~0.75 tokens per word for English text
        words = len(text.split())
        return int(words * 0.75)
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into tokens."""
        if not text:
            return []
        
        if self.tokenizer is not None:
            try:
                tokens = self.tokenizer.encode(text)
                return [self.tokenizer.decode([token]) for token in tokens]
            except Exception as e:
                st.warning(f"Error with tiktoken: {str(e)}. Using word-based fallback.")
                return self._tokenize_fallback(text)
        else:
            return self._tokenize_fallback(text)
    
    def _tokenize_fallback(self, text: str) -> List[str]:
        """Fallback tokenization using simple word splitting."""
        return text.split()
    
    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to specified number of tokens."""
        if not text:
            return ""
        
        if self.tokenizer is not None:
            try:
                tokens = self.tokenizer.encode(text)
                if len(tokens) <= max_tokens:
                    return text
                
                truncated_tokens = tokens[:max_tokens]
                return self.tokenizer.decode(truncated_tokens)
            except Exception as e:
                st.warning(f"Error with tiktoken: {str(e)}. Using word-based fallback.")
                return self._truncate_fallback(text, max_tokens)
        else:
            return self._truncate_fallback(text, max_tokens)
    
    def _truncate_fallback(self, text: str, max_tokens: int) -> str:
        """Fallback truncation using word-based estimation."""
        words = text.split()
        # Estimate: ~0.75 tokens per word
        max_words = int(max_tokens / 0.75)
        if len(words) <= max_words:
            return text
        
        return ' '.join(words[:max_words])
    
    def split_by_tokens(self, text: str, chunk_size: int) -> List[str]:
        """Split text into chunks of specified token size."""
        if not text:
            return []
        
        if self.tokenizer is not None:
            try:
                return self._split_by_tokens_tiktoken(text, chunk_size)
            except Exception as e:
                st.warning(f"Error with tiktoken: {str(e)}. Using word-based fallback.")
                return self._split_by_tokens_fallback(text, chunk_size)
        else:
            return self._split_by_tokens_fallback(text, chunk_size)
    
    def _split_by_tokens_tiktoken(self, text: str, chunk_size: int) -> List[str]:
        """Split text using tiktoken."""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), chunk_size):
            chunk_tokens = tokens[i:i + chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
        
        return chunks
    
    def _split_by_tokens_fallback(self, text: str, chunk_size: int) -> List[str]:
        """Split text using word-based estimation."""
        words = text.split()
        # Estimate: ~0.75 tokens per word
        words_per_chunk = int(chunk_size / 0.75)
        chunks = []
        
        for i in range(0, len(words), words_per_chunk):
            chunk_words = words[i:i + words_per_chunk]
            chunks.append(' '.join(chunk_words))
        
        return chunks
    
    def get_token_positions(self, text: str) -> List[tuple]:
        """Get character positions for each token."""
        if not text:
            return []
        
        # Simple word-based position tracking
        words = text.split()
        positions = []
        current_pos = 0
        
        for word in words:
            start_pos = text.find(word, current_pos)
            end_pos = start_pos + len(word)
            positions.append((start_pos, end_pos))
            current_pos = end_pos
        
        return positions 