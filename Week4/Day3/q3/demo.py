#!/usr/bin/env python3
"""
Demonstration script for RAG Chunking Strategy Visualizer
Shows how different chunking strategies work with sample text.
"""

from strategies.fixed_length import FixedLengthChunker
from strategies.sliding_window import SlidingWindowChunker
from strategies.sentence_based import SentenceBasedChunker
from strategies.paragraph_based import ParagraphBasedChunker
from strategies.semantic_chunking import SemanticChunker

def main():
    # Sample text for demonstration
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.

    The term "artificial intelligence" was coined in 1956 by John McCarthy at the Dartmouth Conference. Since then, AI has experienced several waves of optimism and pessimism, with periods of rapid advancement followed by "AI winters" where funding and interest decreased dramatically.

    Modern AI techniques include machine learning, deep learning, natural language processing, computer vision, and robotics. These technologies have found applications in numerous fields including healthcare, finance, transportation, and entertainment.

    The future of AI remains both promising and uncertain. While AI systems continue to achieve remarkable breakthroughs in specific domains, the goal of artificial general intelligence (AGI) - AI that matches or exceeds human intelligence across all cognitive tasks - remains elusive.
    """
    
    print("🧠 RAG Chunking Strategy Visualizer - Demo")
    print("=" * 50)
    print(f"Sample text length: {len(sample_text)} characters")
    print()
    
    # Test each chunking strategy
    strategies = [
        ("Fixed-Length Token", FixedLengthChunker(), {"chunk_size": 100}),
        ("Sliding Window", SlidingWindowChunker(), {"chunk_size": 100, "overlap": 20}),
        ("Sentence-Based", SentenceBasedChunker(), {"sentences_per_chunk": 2}),
        ("Paragraph-Based", ParagraphBasedChunker(), {"paragraphs_per_chunk": 1}),
        ("Semantic Chunking", SemanticChunker(), {"similarity_threshold": 0.7, "max_chunk_size": 150})
    ]
    
    for strategy_name, chunker, params in strategies:
        print(f"\n📄 {strategy_name} Strategy")
        print("-" * 30)
        
        try:
            chunks = chunker.chunk_text(sample_text, **params)
            print(f"Generated {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
                print(f"\nChunk {i+1}:")
                print(f"  Tokens: {chunk.get('token_count', 'N/A')}")
                print(f"  Overlap: {chunk.get('overlap', 0)}")
                print(f"  Content: {chunk['content'][:100]}...")
                
            if len(chunks) > 3:
                print(f"\n... and {len(chunks) - 3} more chunks")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n✅ Demo completed successfully!")
    print("\nTo run the full Streamlit app:")
    print("  streamlit run app.py")

if __name__ == "__main__":
    main() 