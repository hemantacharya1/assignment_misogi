import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import io
import time
from typing import List, Dict, Any, Optional

# Import our custom modules
from utils.pdf_processor import PDFProcessor
from utils.tokenizer import TokenizerUtils
from strategies.fixed_length import FixedLengthChunker
from strategies.sliding_window import SlidingWindowChunker
from strategies.sentence_based import SentenceBasedChunker
from strategies.paragraph_based import ParagraphBasedChunker
from strategies.semantic_chunking import SemanticChunker
from utils.visualizations import VisualizationUtils

# Page configuration
st.set_page_config(
    page_title="RAG Chunking Strategy Visualizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chunk-container {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .chunk-header {
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .chunk-metadata {
        font-size: 0.8em;
        color: #7f8c8d;
        margin-top: 10px;
    }
    .strategy-explanation {
        background-color: #e8f4f8;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
        border-left: 4px solid #3498db;
    }
</style>
""", unsafe_allow_html=True)

class RAGChunkingApp:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.tokenizer_utils = TokenizerUtils()
        self.viz_utils = VisualizationUtils()
        
        # Initialize chunking strategies
        self.strategies = {
            "Fixed-Length Token": FixedLengthChunker(),
            "Sliding Window": SlidingWindowChunker(),
            "Sentence-Based": SentenceBasedChunker(),
            "Paragraph-Based": ParagraphBasedChunker(),
            "Semantic Chunking": SemanticChunker()
        }
        
        # Initialize session state
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = None
        if 'extracted_text' not in st.session_state:
            st.session_state.extracted_text = ""
        if 'chunks' not in st.session_state:
            st.session_state.chunks = []
        if 'current_strategy' not in st.session_state:
            st.session_state.current_strategy = "Fixed-Length Token"
    
    def render_header(self):
        st.title("🧠 RAG Chunking Strategy Visualizer")
        st.markdown("""
        **Explore different text chunking strategies for Retrieval-Augmented Generation (RAG) systems.**
        
        Upload a PDF document and experiment with various chunking approaches to understand their impact on text retrieval and processing.
        """)
    
    def render_sidebar(self):
        st.sidebar.header("📋 Configuration")
        
        # File upload
        uploaded_file = st.sidebar.file_uploader(
            "Upload PDF Document", 
            type=['pdf'],
            help="Choose a PDF file to analyze with different chunking strategies"
        )
        
        if uploaded_file is not None:
            if uploaded_file != st.session_state.uploaded_file:
                st.session_state.uploaded_file = uploaded_file
                with st.spinner("Extracting text from PDF..."):
                    st.session_state.extracted_text = self.pdf_processor.extract_text(uploaded_file)
                st.success("PDF processed successfully!")
        
        # Strategy selection
        st.sidebar.subheader("🔧 Chunking Strategy")
        strategy = st.sidebar.selectbox(
            "Select Strategy",
            list(self.strategies.keys()),
            index=list(self.strategies.keys()).index(st.session_state.current_strategy)
        )
        
        if strategy != st.session_state.current_strategy:
            st.session_state.current_strategy = strategy
            st.session_state.chunks = []  # Clear previous chunks
        
        # Strategy-specific parameters
        self.render_strategy_parameters(strategy)
        
        # Processing button
        if st.sidebar.button("🚀 Process Document", type="primary"):
            if st.session_state.extracted_text:
                self.process_document(strategy)
            else:
                st.sidebar.error("Please upload a PDF first!")
    
    def render_strategy_parameters(self, strategy: str):
        st.sidebar.subheader("⚙️ Parameters")
        
        if strategy == "Fixed-Length Token":
            st.session_state.chunk_size = st.sidebar.slider("Chunk Size (tokens)", 100, 1000, 512)
            
        elif strategy == "Sliding Window":
            st.session_state.chunk_size = st.sidebar.slider("Chunk Size (tokens)", 100, 1000, 512)
            st.session_state.overlap = st.sidebar.slider("Overlap (tokens)", 0, 200, 50)
            
        elif strategy == "Sentence-Based":
            st.session_state.sentences_per_chunk = st.sidebar.slider("Sentences per chunk", 1, 10, 5)
            
        elif strategy == "Paragraph-Based":
            st.session_state.paragraphs_per_chunk = st.sidebar.slider("Paragraphs per chunk", 1, 5, 1)
            
        elif strategy == "Semantic Chunking":
            st.session_state.similarity_threshold = st.sidebar.slider("Similarity Threshold", 0.1, 0.9, 0.7)
            st.session_state.max_chunk_size = st.sidebar.slider("Max Chunk Size (tokens)", 200, 1000, 600)
    
    def process_document(self, strategy: str):
        with st.spinner(f"Processing document with {strategy} strategy..."):
            chunker = self.strategies[strategy]
            
            # Get parameters from session state
            params = self.get_strategy_params(strategy)
            
            # Process chunks
            st.session_state.chunks = chunker.chunk_text(
                st.session_state.extracted_text, 
                **params
            )
            
            st.success(f"Document processed! Generated {len(st.session_state.chunks)} chunks.")
    
    def get_strategy_params(self, strategy: str) -> Dict[str, Any]:
        params = {}
        
        if strategy == "Fixed-Length Token":
            params['chunk_size'] = st.session_state.get('chunk_size', 512)
            
        elif strategy == "Sliding Window":
            params['chunk_size'] = st.session_state.get('chunk_size', 512)
            params['overlap'] = st.session_state.get('overlap', 50)
            
        elif strategy == "Sentence-Based":
            params['sentences_per_chunk'] = st.session_state.get('sentences_per_chunk', 5)
            
        elif strategy == "Paragraph-Based":
            params['paragraphs_per_chunk'] = st.session_state.get('paragraphs_per_chunk', 1)
            
        elif strategy == "Semantic Chunking":
            params['similarity_threshold'] = st.session_state.get('similarity_threshold', 0.7)
            params['max_chunk_size'] = st.session_state.get('max_chunk_size', 600)
        
        return params
    
    def render_main_content(self):
        if not st.session_state.extracted_text:
            st.info("👆 Please upload a PDF document to get started!")
            return
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Document Preview", "🔍 Chunks", "📊 Analytics", "🎨 Visualizations"])
        
        with tab1:
            self.render_document_preview()
        
        with tab2:
            self.render_chunks_view()
        
        with tab3:
            self.render_analytics()
        
        with tab4:
            self.render_visualizations()
    
    def render_document_preview(self):
        st.subheader("📄 Original Document")
        
        # Document statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Characters", len(st.session_state.extracted_text))
        with col2:
            st.metric("Total Words", len(st.session_state.extracted_text.split()))
        with col3:
            tokens = self.tokenizer_utils.count_tokens(st.session_state.extracted_text)
            st.metric("Total Tokens", tokens)
        with col4:
            paragraphs = len([p for p in st.session_state.extracted_text.split('\n\n') if p.strip()])
            st.metric("Paragraphs", paragraphs)
        
        # Text preview
        st.text_area(
            "Document Content (First 2000 characters)",
            st.session_state.extracted_text[:2000] + "..." if len(st.session_state.extracted_text) > 2000 else st.session_state.extracted_text,
            height=300
        )
    
    def render_chunks_view(self):
        if not st.session_state.chunks:
            st.info("Process the document first to see chunks!")
            return
        
        st.subheader("🔍 Generated Chunks")
        
        # Strategy explanation
        self.render_strategy_explanation(st.session_state.current_strategy)
        
        # Chunk statistics
        total_chunks = len(st.session_state.chunks)
        avg_tokens = np.mean([chunk.get('token_count', 0) for chunk in st.session_state.chunks])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Chunks", total_chunks)
        with col2:
            st.metric("Average Tokens/Chunk", f"{avg_tokens:.1f}")
        with col3:
            overlap_chunks = len([c for c in st.session_state.chunks if c.get('overlap', 0) > 0])
            st.metric("Chunks with Overlap", overlap_chunks)
        
        # Chunk display controls
        col1, col2 = st.columns([3, 1])
        with col1:
            max_chunks = st.slider("Max chunks to display", 1, min(50, total_chunks), min(10, total_chunks))
        with col2:
            show_metadata = st.checkbox("Show metadata", value=True)
        
        # Display chunks
        for i, chunk in enumerate(st.session_state.chunks[:max_chunks]):
            self.render_chunk(chunk, i, show_metadata)
    
    def render_chunk(self, chunk: Dict[str, Any], index: int, show_metadata: bool):
        with st.container():
            st.markdown(f'<div class="chunk-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="chunk-header">Chunk {index + 1}</div>', unsafe_allow_html=True)
            
            # Chunk content
            st.markdown(chunk['content'])
            
            if show_metadata:
                metadata_text = f"""
                **Tokens:** {chunk.get('token_count', 'N/A')} | 
                **Position:** {chunk.get('start_pos', 'N/A')}-{chunk.get('end_pos', 'N/A')} | 
                **Overlap:** {chunk.get('overlap', 0)} tokens
                """
                
                if chunk.get('similarity_score'):
                    metadata_text += f" | **Similarity:** {chunk['similarity_score']:.3f}"
                
                st.markdown(f'<div class="chunk-metadata">{metadata_text}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def render_strategy_explanation(self, strategy: str):
        explanations = {
            "Fixed-Length Token": {
                "description": "Divides text into chunks of exactly the specified number of tokens.",
                "how_it_works": "Uses a tokenizer to count tokens and splits text at token boundaries.",
                "pros": ["Predictable chunk sizes", "Simple to implement", "Good for consistent processing"],
                "cons": ["May break sentences/paragraphs", "Context loss at boundaries", "Inflexible"],
                "use_cases": ["When you need consistent chunk sizes", "Simple RAG implementations", "Token-constrained models"]
            },
            "Sliding Window": {
                "description": "Creates overlapping chunks with specified overlap to maintain context.",
                "how_it_works": "Moves a window of fixed size across the text with configurable overlap.",
                "pros": ["Maintains context across chunks", "Reduces information loss", "Better for question answering"],
                "cons": ["Increased storage requirements", "Processing overhead", "Potential redundancy"],
                "use_cases": ["Question answering systems", "When context preservation is crucial", "Complex document analysis"]
            },
            "Sentence-Based": {
                "description": "Groups complete sentences together to maintain semantic coherence.",
                "how_it_works": "Uses NLP to detect sentence boundaries and groups them into chunks.",
                "pros": ["Preserves sentence integrity", "Natural language boundaries", "Good readability"],
                "cons": ["Variable chunk sizes", "Dependent on sentence detection accuracy", "May create very small/large chunks"],
                "use_cases": ["Literature analysis", "Legal documents", "When sentence integrity matters"]
            },
            "Paragraph-Based": {
                "description": "Splits text at paragraph boundaries to maintain topical coherence.",
                "how_it_works": "Identifies paragraph breaks and groups paragraphs into chunks.",
                "pros": ["Maintains topical coherence", "Natural document structure", "Good for structured documents"],
                "cons": ["Highly variable chunk sizes", "Depends on document formatting", "May create very large chunks"],
                "use_cases": ["Academic papers", "Books", "Well-structured documents"]
            },
            "Semantic Chunking": {
                "description": "Groups semantically similar sentences using embedding similarity.",
                "how_it_works": "Computes sentence embeddings and groups similar sentences based on cosine similarity.",
                "pros": ["Maintains semantic coherence", "Adaptive to content", "Better retrieval quality"],
                "cons": ["Computationally expensive", "Requires embedding models", "Complex implementation"],
                "use_cases": ["High-quality RAG systems", "Complex documents", "When semantic coherence is priority"]
            }
        }
        
        if strategy in explanations:
            explanation = explanations[strategy]
            
            st.markdown(f'<div class="strategy-explanation">', unsafe_allow_html=True)
            st.markdown(f"**{strategy} Strategy**")
            st.markdown(f"*{explanation['description']}*")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**How it works:**")
                st.markdown(explanation['how_it_works'])
                
                st.markdown("**Pros:**")
                for pro in explanation['pros']:
                    st.markdown(f"• {pro}")
            
            with col2:
                st.markdown("**Cons:**")
                for con in explanation['cons']:
                    st.markdown(f"• {con}")
                
                st.markdown("**Best use cases:**")
                for use_case in explanation['use_cases']:
                    st.markdown(f"• {use_case}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def render_analytics(self):
        if not st.session_state.chunks:
            st.info("Process the document first to see analytics!")
            return
        
        st.subheader("📊 Chunking Analytics")
        
        # Prepare data for analysis
        chunk_data = []
        for i, chunk in enumerate(st.session_state.chunks):
            chunk_data.append({
                'chunk_id': i,
                'token_count': chunk.get('token_count', 0),
                'character_count': len(chunk['content']),
                'word_count': len(chunk['content'].split()),
                'overlap': chunk.get('overlap', 0),
                'start_pos': chunk.get('start_pos', 0),
                'end_pos': chunk.get('end_pos', 0)
            })
        
        df = pd.DataFrame(chunk_data)
        
        # Analytics visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Token distribution
            fig = px.histogram(df, x='token_count', nbins=20, title='Token Count Distribution')
            st.plotly_chart(fig, use_container_width=True)
            
            # Token count over chunks
            fig = px.line(df, x='chunk_id', y='token_count', title='Token Count per Chunk')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Word vs Token relationship
            fig = px.scatter(df, x='word_count', y='token_count', title='Words vs Tokens')
            st.plotly_chart(fig, use_container_width=True)
            
            # Chunk overlap analysis
            if df['overlap'].sum() > 0:
                fig = px.bar(df, x='chunk_id', y='overlap', title='Overlap per Chunk')
                st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.subheader("📈 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Min Tokens", df['token_count'].min())
            st.metric("Max Tokens", df['token_count'].max())
        
        with col2:
            st.metric("Mean Tokens", f"{df['token_count'].mean():.1f}")
            st.metric("Std Dev", f"{df['token_count'].std():.1f}")
        
        with col3:
            st.metric("Total Overlap", df['overlap'].sum())
            st.metric("Avg Overlap", f"{df['overlap'].mean():.1f}")
        
        with col4:
            coverage = (df['token_count'].sum() - df['overlap'].sum()) / self.tokenizer_utils.count_tokens(st.session_state.extracted_text)
            st.metric("Coverage", f"{coverage:.1%}")
            st.metric("Efficiency", f"{1 - df['overlap'].sum() / df['token_count'].sum():.1%}")
    
    def render_visualizations(self):
        if not st.session_state.chunks:
            st.info("Process the document first to see visualizations!")
            return
        
        st.subheader("🎨 Advanced Visualizations")
        
        # Only show advanced visualizations for semantic chunking
        if st.session_state.current_strategy == "Semantic Chunking":
            self.render_semantic_visualizations()
        else:
            self.render_basic_visualizations()
    
    def render_semantic_visualizations(self):
        st.info("🔄 Generating semantic visualizations...")
        
        # This would require the semantic chunker to store embeddings
        # For now, we'll show a placeholder
        st.markdown("**Semantic Similarity Heatmap**")
        st.info("Advanced semantic visualizations will be available after processing with semantic chunking.")
    
    def render_basic_visualizations(self):
        # Chunk size heatmap
        chunk_sizes = [chunk.get('token_count', 0) for chunk in st.session_state.chunks]
        
        # Create a simple heatmap of chunk sizes
        fig = go.Figure(data=go.Heatmap(
            z=[chunk_sizes],
            colorscale='Viridis',
            colorbar=dict(title="Token Count")
        ))
        fig.update_layout(title="Chunk Size Heatmap", xaxis_title="Chunk Index", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
        
        # Chunk position timeline
        positions = [(chunk.get('start_pos', 0), chunk.get('end_pos', 0)) for chunk in st.session_state.chunks]
        
        fig = go.Figure()
        for i, (start, end) in enumerate(positions):
            fig.add_trace(go.Scatter(
                x=[start, end],
                y=[i, i],
                mode='lines+markers',
                name=f'Chunk {i+1}',
                showlegend=False
            ))
        
        fig.update_layout(title="Chunk Position Timeline", xaxis_title="Character Position", yaxis_title="Chunk Index")
        st.plotly_chart(fig, use_container_width=True)
    
    def run(self):
        self.render_header()
        self.render_sidebar()
        self.render_main_content()

# Run the application
if __name__ == "__main__":
    app = RAGChunkingApp()
    app.run() 