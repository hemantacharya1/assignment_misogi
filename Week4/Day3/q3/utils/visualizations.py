import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from typing import List, Dict, Any, Optional
import streamlit as st

class VisualizationUtils:
    """Utilities for creating advanced visualizations."""
    
    def __init__(self):
        self.color_palette = px.colors.qualitative.Set3
    
    def create_similarity_heatmap(self, embeddings: np.ndarray, chunk_labels: List[str] = None) -> go.Figure:
        """Create a similarity heatmap for chunk embeddings."""
        if embeddings is None or len(embeddings) == 0:
            return go.Figure()
        
        # Calculate cosine similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Create labels if not provided
        if chunk_labels is None:
            chunk_labels = [f"Chunk {i+1}" for i in range(len(embeddings))]
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=similarity_matrix,
            x=chunk_labels,
            y=chunk_labels,
            colorscale='RdYlBu_r',
            colorbar=dict(title="Cosine Similarity"),
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Chunk Similarity Heatmap",
            xaxis_title="Chunks",
            yaxis_title="Chunks",
            width=800,
            height=600
        )
        
        return fig
    
    def create_clustering_visualization(self, embeddings: np.ndarray, chunk_labels: List[str] = None, n_clusters: int = 5) -> go.Figure:
        """Create a 2D clustering visualization using PCA."""
        if embeddings is None or len(embeddings) == 0:
            return go.Figure()
        
        # Apply PCA for dimensionality reduction
        pca = PCA(n_components=2)
        embeddings_2d = pca.fit_transform(embeddings)
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=min(n_clusters, len(embeddings)), random_state=42)
        cluster_labels = kmeans.fit_predict(embeddings)
        
        # Create labels if not provided
        if chunk_labels is None:
            chunk_labels = [f"Chunk {i+1}" for i in range(len(embeddings))]
        
        # Create scatter plot
        fig = go.Figure()
        
        for cluster_id in range(n_clusters):
            mask = cluster_labels == cluster_id
            if np.any(mask):
                fig.add_trace(go.Scatter(
                    x=embeddings_2d[mask, 0],
                    y=embeddings_2d[mask, 1],
                    mode='markers',
                    name=f'Cluster {cluster_id + 1}',
                    text=[chunk_labels[i] for i in range(len(chunk_labels)) if mask[i]],
                    hovertemplate='%{text}<br>PC1: %{x:.3f}<br>PC2: %{y:.3f}<extra></extra>',
                    marker=dict(size=10, opacity=0.7)
                ))
        
        fig.update_layout(
            title="Chunk Clustering Visualization (PCA)",
            xaxis_title=f"PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)",
            yaxis_title=f"PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)",
            showlegend=True,
            width=800,
            height=600
        )
        
        return fig
    
    def create_chunk_timeline(self, chunks: List[Dict[str, Any]]) -> go.Figure:
        """Create a timeline visualization of chunks."""
        if not chunks:
            return go.Figure()
        
        # Prepare data
        chunk_data = []
        for i, chunk in enumerate(chunks):
            chunk_data.append({
                'chunk_id': i,
                'start_pos': chunk.get('start_pos', 0),
                'end_pos': chunk.get('end_pos', 0),
                'token_count': chunk.get('token_count', 0),
                'overlap': chunk.get('overlap', 0)
            })
        
        df = pd.DataFrame(chunk_data)
        
        # Create timeline
        fig = go.Figure()
        
        for i, row in df.iterrows():
            # Main chunk bar
            fig.add_trace(go.Scatter(
                x=[row['start_pos'], row['end_pos']],
                y=[i, i],
                mode='lines+markers',
                name=f'Chunk {i+1}',
                line=dict(width=8, color=self.color_palette[i % len(self.color_palette)]),
                hovertemplate=f'Chunk {i+1}<br>Tokens: {row["token_count"]}<br>Position: {row["start_pos"]}-{row["end_pos"]}<extra></extra>',
                showlegend=False
            ))
            
            # Overlap indicator
            if row['overlap'] > 0:
                fig.add_trace(go.Scatter(
                    x=[row['start_pos']],
                    y=[i],
                    mode='markers',
                    marker=dict(symbol='diamond', size=10, color='red'),
                    name='Overlap',
                    hovertemplate=f'Overlap: {row["overlap"]} tokens<extra></extra>',
                    showlegend=False
                ))
        
        fig.update_layout(
            title="Chunk Timeline",
            xaxis_title="Character Position",
            yaxis_title="Chunk Index",
            height=max(400, len(chunks) * 30),
            showlegend=False
        )
        
        return fig
    
    def create_token_distribution(self, chunks: List[Dict[str, Any]]) -> go.Figure:
        """Create token distribution visualization."""
        if not chunks:
            return go.Figure()
        
        token_counts = [chunk.get('token_count', 0) for chunk in chunks]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Token Count Distribution', 'Token Count Over Chunks', 
                          'Box Plot', 'Cumulative Distribution'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Histogram
        fig.add_trace(
            go.Histogram(x=token_counts, nbinsx=20, name='Distribution'),
            row=1, col=1
        )
        
        # Line plot
        fig.add_trace(
            go.Scatter(x=list(range(len(token_counts))), y=token_counts, 
                      mode='lines+markers', name='Token Count'),
            row=1, col=2
        )
        
        # Box plot
        fig.add_trace(
            go.Box(y=token_counts, name='Token Count'),
            row=2, col=1
        )
        
        # Cumulative distribution
        sorted_tokens = np.sort(token_counts)
        y_vals = np.arange(1, len(sorted_tokens) + 1) / len(sorted_tokens)
        fig.add_trace(
            go.Scatter(x=sorted_tokens, y=y_vals, 
                      mode='lines', name='Cumulative'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Token Analysis Dashboard",
            height=800,
            showlegend=False
        )
        
        return fig
    
    def create_overlap_analysis(self, chunks: List[Dict[str, Any]]) -> go.Figure:
        """Create overlap analysis visualization."""
        if not chunks:
            return go.Figure()
        
        # Extract overlap data
        overlap_data = []
        for i, chunk in enumerate(chunks):
            overlap_data.append({
                'chunk_id': i,
                'overlap': chunk.get('overlap', 0),
                'token_count': chunk.get('token_count', 0)
            })
        
        df = pd.DataFrame(overlap_data)
        
        # Filter chunks with overlap
        overlap_chunks = df[df['overlap'] > 0]
        
        if len(overlap_chunks) == 0:
            # No overlap to visualize
            fig = go.Figure()
            fig.add_annotation(
                text="No overlapping chunks found",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20)
            )
            fig.update_layout(title="Overlap Analysis")
            return fig
        
        # Create overlap visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Overlap Distribution', 'Overlap vs Token Count', 
                          'Overlap Timeline', 'Overlap Efficiency'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Overlap distribution
        fig.add_trace(
            go.Histogram(x=overlap_chunks['overlap'], nbinsx=15, name='Overlap Distribution'),
            row=1, col=1
        )
        
        # Overlap vs token count
        fig.add_trace(
            go.Scatter(x=overlap_chunks['token_count'], y=overlap_chunks['overlap'], 
                      mode='markers', name='Overlap vs Tokens',
                      hovertemplate='Tokens: %{x}<br>Overlap: %{y}<extra></extra>'),
            row=1, col=2
        )
        
        # Overlap timeline
        fig.add_trace(
            go.Scatter(x=overlap_chunks['chunk_id'], y=overlap_chunks['overlap'], 
                      mode='lines+markers', name='Overlap Timeline'),
            row=2, col=1
        )
        
        # Overlap efficiency (overlap ratio)
        efficiency = overlap_chunks['overlap'] / overlap_chunks['token_count']
        fig.add_trace(
            go.Scatter(x=overlap_chunks['chunk_id'], y=efficiency, 
                      mode='lines+markers', name='Overlap Ratio'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Overlap Analysis Dashboard",
            height=800,
            showlegend=False
        )
        
        return fig
    
    def create_performance_metrics(self, chunks: List[Dict[str, Any]], original_text: str) -> go.Figure:
        """Create performance metrics visualization."""
        if not chunks:
            return go.Figure()
        
        # Calculate metrics
        total_tokens = sum(chunk.get('token_count', 0) for chunk in chunks)
        total_overlap = sum(chunk.get('overlap', 0) for chunk in chunks)
        unique_tokens = total_tokens - total_overlap
        
        from utils.tokenizer import TokenizerUtils
        tokenizer = TokenizerUtils()
        original_tokens = tokenizer.count_tokens(original_text)
        
        # Coverage and efficiency metrics
        coverage = unique_tokens / original_tokens if original_tokens > 0 else 0
        efficiency = unique_tokens / total_tokens if total_tokens > 0 else 0
        redundancy = total_overlap / total_tokens if total_tokens > 0 else 0
        
        # Create metrics visualization
        fig = go.Figure()
        
        # Add metrics as a donut chart
        metrics = ['Coverage', 'Efficiency', 'Redundancy']
        values = [coverage, efficiency, redundancy]
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        
        fig.add_trace(go.Pie(
            labels=metrics,
            values=values,
            hole=0.3,
            marker=dict(colors=colors),
            hovertemplate='%{label}: %{value:.1%}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Chunking Performance Metrics",
            annotations=[dict(text='Metrics', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        return fig 