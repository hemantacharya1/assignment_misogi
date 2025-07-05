from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from similarity_analyzer import PlagiarismDetector
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Plagiarism Detector API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the plagiarism detector
detector = PlagiarismDetector()

class TextAnalysisRequest(BaseModel):
    texts: List[str]

class TextAnalysisResponse(BaseModel):
    similarity_matrix: List[List[float]]
    flagged_pairs: List[dict]
    text_count: int
    threshold_percentage: float
    highest_similarity: float

@app.get("/")
async def root():
    """Root endpoint for API health check."""
    return {"message": "Plagiarism Detector API is running"}

@app.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_texts(request: TextAnalysisRequest):
    """
    Analyze multiple texts for plagiarism detection.
    
    Args:
        request: Contains list of texts to analyze
        
    Returns:
        Analysis results with similarity matrix and flagged pairs
    """
    try:
        # Validate input
        if not request.texts:
            raise HTTPException(status_code=400, detail="No texts provided")
        
        if len(request.texts) < 2:
            raise HTTPException(status_code=400, detail="At least 2 texts required for comparison")
        
        if len(request.texts) > 4:
            raise HTTPException(status_code=400, detail="Maximum 4 texts allowed")
        
        # Filter out empty texts
        non_empty_texts = [text.strip() for text in request.texts if text.strip()]
        
        if len(non_empty_texts) < 2:
            raise HTTPException(status_code=400, detail="At least 2 non-empty texts required")
        
        # Preprocess texts
        processed_texts = [detector.preprocess_text(text) for text in non_empty_texts]
        
        logger.info(f"Analyzing {len(processed_texts)} texts")
        
        # Analyze texts
        results = detector.analyze_texts(processed_texts)
        
        logger.info(f"Analysis complete. Found {len(results['flagged_pairs'])} flagged pairs")
        
        return TextAnalysisResponse(**results)
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model": "all-MiniLM-L6-v2"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 