# RAG Chunking Strategy Visualizer

A comprehensive Streamlit web application for exploring and comparing different text chunking strategies used in Retrieval-Augmented Generation (RAG) systems.

## 🎯 Overview

This application allows you to:
- Upload PDF documents and extract text
- Apply different chunking strategies to your text
- Visualize and compare the results
- Understand the trade-offs between different approaches
- Analyze chunking performance with detailed metrics

## 🚀 Features

### PDF Processing
- **Multi-backend support**: Uses `pdfplumber` or `PyMuPDF` for robust text extraction
- **Metadata extraction**: Extracts document information and statistics
- **Large file handling**: Efficient processing of large PDF documents

### Chunking Strategies

#### 1. **Fixed-Length Token Chunking**
- Splits text into chunks of exactly the specified number of tokens
- **Parameters**: `chunk_size` (100-1000 tokens, default: 512)
- **Best for**: Consistent processing requirements, simple RAG implementations

#### 2. **Sliding Window Chunking**
- Creates overlapping chunks to maintain context across boundaries
- **Parameters**: 
  - `chunk_size` (100-1000 tokens, default: 512)
  - `overlap` (0-200 tokens, default: 50)
- **Best for**: Question answering systems, context preservation

#### 3. **Sentence-Based Chunking**
- Groups complete sentences to maintain semantic coherence
- **Parameters**: `sentences_per_chunk` (1-10 sentences, default: 5)
- **Best for**: Literature analysis, legal documents, educational content

#### 4. **Paragraph-Based Chunking**
- Splits text at paragraph boundaries for topical coherence
- **Parameters**: `paragraphs_per_chunk` (1-5 paragraphs, default: 1)
- **Best for**: Academic papers, books, well-structured documents

#### 5. **Semantic Chunking**
- Groups semantically similar sentences using embedding similarity
- **Parameters**: 
  - `similarity_threshold` (0.1-0.9, default: 0.7)
  - `max_chunk_size` (200-1000 tokens, default: 600)
- **Best for**: High-quality RAG systems, complex document analysis

### Visualization & Analysis

#### Interactive Dashboard
- **Document Preview**: View original text with statistics
- **Chunk Viewer**: Browse generated chunks with metadata
- **Analytics**: Detailed performance metrics and visualizations
- **Advanced Visualizations**: Heatmaps, clustering, and semantic analysis

#### Performance Metrics
- Token distribution analysis
- Overlap efficiency calculations
- Coverage and redundancy metrics
- Semantic coherence scoring (for semantic chunking)

## 📦 Installation

### Prerequisites
```bash
python >= 3.8
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Optional Dependencies
For enhanced functionality, install additional NLP libraries:

```bash
# For better sentence tokenization
pip install nltk
python -c "import nltk; nltk.download('punkt')"

# For spaCy-based sentence tokenization
pip install spacy
python -m spacy download en_core_web_sm
```

## 🏃 Usage

### Running the Application
```bash
streamlit run app.py
```

### Using the Interface

1. **Upload PDF**: Use the sidebar to upload your PDF document
2. **Select Strategy**: Choose from the 5 available chunking strategies
3. **Configure Parameters**: Adjust strategy-specific parameters
4. **Process Document**: Click "Process Document" to generate chunks
5. **Explore Results**: Navigate through different tabs to analyze results

### Example Workflow

```python
# Example: Processing a document with semantic chunking
1. Upload your PDF file
2. Select "Semantic Chunking" from the dropdown
3. Set similarity_threshold = 0.7
4. Set max_chunk_size = 600
5. Click "Process Document"
6. Explore the generated chunks in the "Chunks" tab
7. Analyze performance in the "Analytics" tab
8. View semantic relationships in "Visualizations"
```

## 🏗️ Project Structure

```
Week4/Day3/q3/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── pdf_processor.py           # PDF text extraction
│   ├── tokenizer.py               # Tokenization utilities
│   └── visualizations.py          # Advanced plotting utilities
└── strategies/                     # Chunking strategy implementations
    ├── __init__.py
    ├── fixed_length.py            # Fixed-length token chunking
    ├── sliding_window.py          # Sliding window chunking
    ├── sentence_based.py          # Sentence-based chunking
    ├── paragraph_based.py         # Paragraph-based chunking
    └── semantic_chunking.py       # Semantic chunking
```

## 🔧 Technical Details

### Architecture
- **Modular Design**: Each chunking strategy is implemented as a separate class
- **Fallback Mechanisms**: Graceful degradation when optional dependencies are unavailable
- **Performance Optimized**: Efficient processing of large documents
- **Extensible**: Easy to add new chunking strategies

### Dependencies
- **Core**: `streamlit`, `numpy`, `pandas`, `matplotlib`, `plotly`
- **PDF Processing**: `pdfplumber`, `PyMuPDF`
- **Tokenization**: `tiktoken`
- **NLP**: `nltk`, `spacy` (optional)
- **Semantic Analysis**: `sentence-transformers`, `scikit-learn`

### Token Counting
The application uses `tiktoken` for accurate token counting with fallback to word-based estimation when unavailable.

### Embedding Models
For semantic chunking, the application uses sentence-transformers with the default `all-MiniLM-L6-v2` model.

## 📊 Interpreting Results

### Chunk Metadata
Each chunk includes:
- **Content**: The actual text content
- **Token Count**: Number of tokens in the chunk
- **Position**: Start and end character positions
- **Overlap**: Number of overlapping tokens (if applicable)
- **Strategy-specific**: Additional metadata based on the chunking method

### Performance Metrics
- **Coverage**: Percentage of original text covered by unique tokens
- **Efficiency**: Ratio of unique tokens to total tokens
- **Redundancy**: Percentage of tokens that are duplicated across chunks
- **Coherence**: Semantic similarity between chunks (semantic chunking only)

## 🎨 Visualizations

### Basic Visualizations
- **Token Distribution**: Histogram of token counts per chunk
- **Chunk Timeline**: Visual representation of chunk positions
- **Overlap Analysis**: Analysis of overlapping content

### Advanced Visualizations (Semantic Chunking)
- **Similarity Heatmaps**: Cosine similarity between chunks
- **Clustering Visualization**: 2D PCA plot of semantic clusters
- **Performance Metrics**: Comprehensive analysis dashboard

## 🔍 Comparison Guidelines

### When to Use Each Strategy

| Strategy | Best For | Avoid When |
|----------|----------|------------|
| **Fixed-Length** | Consistent processing, simple RAG | Context is crucial |
| **Sliding Window** | QA systems, context preservation | Storage is limited |
| **Sentence-Based** | Literature, legal docs | Variable sizes problematic |
| **Paragraph-Based** | Academic papers, books | Paragraphs are very long |
| **Semantic** | High-quality RAG, research | Speed is critical |

### Performance Considerations
- **Speed**: Fixed-Length > Sentence-Based > Paragraph-Based > Sliding Window > Semantic
- **Quality**: Semantic > Sentence-Based > Paragraph-Based > Sliding Window > Fixed-Length
- **Consistency**: Fixed-Length > Sliding Window > Sentence-Based > Paragraph-Based > Semantic

## 🛠️ Customization

### Adding New Strategies
To add a new chunking strategy:

1. Create a new file in `strategies/` directory
2. Implement the required methods:
   ```python
   class YourChunker:
       def __init__(self):
           pass
       
       def chunk_text(self, text: str, **kwargs) -> List[Dict[str, Any]]:
           # Your implementation
           pass
       
       def get_strategy_info(self) -> Dict[str, Any]:
           # Strategy information
           pass
   ```
3. Add it to the main app's strategy dictionary

### Modifying Visualizations
The visualization utilities in `utils/visualizations.py` can be extended with additional plotting functions.

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Install missing dependencies
2. **PDF Processing Fails**: Ensure PDF is text-based (not image-based)
3. **Slow Processing**: Reduce document size or use simpler strategies
4. **Memory Issues**: Close other applications or use chunk size limits

### Performance Tips
- Use smaller chunk sizes for faster processing
- Disable advanced visualizations for large documents
- Consider using fallback tokenization for speed

## 📈 Future Enhancements

- [ ] Support for additional file formats (DOCX, TXT)
- [ ] Custom embedding model selection
- [ ] Batch processing capabilities
- [ ] Export functionality for chunks
- [ ] Integration with vector databases
- [ ] A/B testing framework for strategies

## 🤝 Contributing

Feel free to contribute by:
- Adding new chunking strategies
- Improving visualizations
- Enhancing performance
- Fixing bugs
- Adding tests

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

## 📧 Support

For questions or issues, please refer to the code comments or create an issue in the repository.

---

**Happy Chunking!** 🚀
