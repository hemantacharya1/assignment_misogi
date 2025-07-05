# 🔍 Plagiarism Detector - Semantic Similarity Analyzer

A web-based plagiarism detection tool that uses semantic similarity analysis with HuggingFace embeddings to identify potential plagiarism between multiple text inputs.

## Features

- **Semantic Analysis**: Uses HuggingFace `all-MiniLM-L6-v2` model for accurate text embeddings
- **Multiple Text Comparison**: Compare up to 4 texts simultaneously
- **Similarity Matrix**: Visual representation of similarity percentages between all text pairs
- **Automated Detection**: Highlights potential plagiarism with 80% similarity threshold
- **Clean Interface**: Modern, responsive React frontend
- **Real-time Results**: Fast analysis with clear visual feedback

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Sentence Transformers**: HuggingFace embedding models
- **scikit-learn**: Cosine similarity calculations
- **NumPy**: Matrix operations

### Frontend
- **React**: Component-based UI framework
- **Vite**: Fast build tool and dev server
- **CSS3**: Custom styling with modern design

## Project Structure

```
Week4/Day3/q2/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── similarity_analyzer.py   # Core plagiarism detection logic
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── App.css            # Styling
│   │   └── main.jsx           # React entry point
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   └── index.html             # HTML template
└── README.md                  # This file
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the backend server**:
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

1. **Open the Application**: Navigate to `http://localhost:3000` in your browser
2. **Enter Texts**: Input 2-4 texts in the provided text areas
3. **Analyze**: Click "Analyze Texts" to start the similarity analysis
4. **View Results**: 
   - Similarity matrix shows percentage similarity between all text pairs
   - High similarity pairs (≥80%) are highlighted in red
   - Flagged pairs are listed separately for easy identification

## API Endpoints

### `POST /analyze`
Analyzes multiple texts for plagiarism detection.

**Request Body**:
```json
{
  "texts": ["text1", "text2", "text3", "text4"]
}
```

**Response**:
```json
{
  "similarity_matrix": [[100.0, 85.2, 12.3, 45.6], ...],
  "flagged_pairs": [
    {
      "text1_index": 0,
      "text2_index": 1,
      "similarity_percentage": 85.2,
      "status": "High Similarity - Potential Plagiarism"
    }
  ],
  "text_count": 4,
  "threshold_percentage": 80.0,
  "highest_similarity": 0.852
}
```

### `GET /health`
Health check endpoint.

## How It Works

1. **Text Preprocessing**: Input texts are cleaned and normalized
2. **Embedding Generation**: Uses HuggingFace `all-MiniLM-L6-v2` model to convert texts to vector embeddings
3. **Similarity Calculation**: Computes cosine similarity between all text pairs
4. **Threshold Analysis**: Identifies pairs with similarity ≥80% as potential plagiarism
5. **Results Display**: Shows similarity matrix and highlights flagged pairs

## Model Information

- **Model**: `all-MiniLM-L6-v2`
- **Type**: Sentence Transformer
- **Advantages**: 
  - Fast inference
  - Good balance of accuracy and speed
  - Semantic understanding beyond keyword matching
  - Free to use (no API keys required)

## Similarity Threshold

- **Default**: 80% similarity
- **Logic**: Pairs with ≥80% similarity are flagged as potential plagiarism
- **Visual**: High similarity pairs are highlighted in red with animation

## Testing the Application

Try these example texts to see the detector in action:

**Example 1 (High Similarity)**:
- Text 1: "The quick brown fox jumps over the lazy dog."
- Text 2: "A fast brown fox leaps over a sleepy dog."

**Example 2 (Low Similarity)**:
- Text 1: "Machine learning is a subset of artificial intelligence."
- Text 2: "The weather today is sunny and warm."

## Troubleshooting

### Common Issues

1. **Backend won't start**: 
   - Check if all dependencies are installed
   - Ensure virtual environment is activated
   - Port 8000 might be in use

2. **Frontend can't connect to backend**:
   - Verify backend is running on port 8000
   - Check CORS settings in main.py

3. **Slow analysis**:
   - First-time model download may take time
   - Subsequent analyses will be faster

### Model Download

On first run, the system will download the embedding model (~90MB). This is a one-time process.

## Performance

- **Model Size**: ~90MB (downloaded once)
- **Analysis Speed**: ~1-3 seconds for 4 texts
- **Memory Usage**: ~200MB during analysis
- **Accuracy**: High semantic similarity detection

## Future Enhancements

- [ ] Support for file uploads
- [ ] Multiple embedding model comparison
- [ ] Adjustable similarity thresholds
- [ ] Export results to PDF/CSV
- [ ] Batch processing for large datasets
- [ ] Advanced text preprocessing options

## License

This project is for educational purposes as part of the assignment.
