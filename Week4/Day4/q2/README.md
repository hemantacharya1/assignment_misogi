🎓 Lecture Q&A App (Local)
A fullstack local application that allows students to upload long lecture videos (2–3 hours), automatically transcribes them, chunks them semantically, and enables natural language conversation using RAG (Retrieval-Augmented Generation) with Gemini API.
🔧 Tech Stack
Backend

FastAPI (Python 3.11+)
FFmpeg — Audio extraction from video files
Faster Whisper — High-performance transcription
ChromaDB — Vector database for semantic search
Gemini API — LLM for answering queries
Pydantic — Data validation and serialization
Sentence Transformers — Text embeddings

Frontend

React.js with Vite
Tailwind CSS v3.x
React Router DOM
Axios — HTTP client

🗂 Project Structure
q2/
├── backend/
│   ├── api/                 # FastAPI routes
│   │   ├── __init__.py
│   │   ├── upload.py        # Video upload endpoints
│   │   └── chat.py          # Chat/query endpoints
│   ├── core/                # Core business logic
│   │   ├── __init__.py
│   │   ├── chunking.py      # Text chunking strategies
│   │   ├── rag.py           # RAG implementation
│   │   └── embeddings.py    # Vector embeddings
│   ├── services/            # External service integrations
│   │   ├── __init__.py
│   │   ├── whisper_service.py
│   │   ├── ffmpeg_service.py
│   │   └── gemini_service.py
│   ├── db/                  # Database operations
│   │   ├── __init__.py
│   │   └── chroma_client.py
│   ├── models/              # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   └── chat.py
│   ├── utils/               # Helper utilities
│   │   ├── __init__.py
│   │   ├── text_processing.py
│   │   └── file_handling.py
│   ├── config.py            # Configuration settings
│   ├── main.py              # FastAPI application entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── UploadPage.jsx
│   │   │   ├── ChatPage.jsx
│   │   │   └── HomePage.jsx
│   │   ├── components/
│   │   │   ├── VideoUploader.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── TranscriptionStatus.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   ├── api/
│   │   │   └── client.js    # Axios configuration
│   │   ├── hooks/           # Custom React hooks
│   │   ├── utils/           # Frontend utilities
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── data/                    # Data storage (gitignored)
│   ├── uploads/             # Raw video files
│   ├── audio/               # Extracted audio files
│   ├── transcriptions/      # Transcription results
│   └── db/                  # ChromaDB files
├── .env                     # Environment variables
├── .gitignore
├── docker-compose.yml       # Optional containerization
└── README.md
✅ Prerequisites

Python 3.11+
Node.js 18+ and npm
FFmpeg installed and added to system PATH
Gemini API key from Google AI Studio

🚀 Getting Started
1. Clone and Setup
bashgit clone https://github.com/your-username/q2.git
cd q2
2. Backend Setup
bashcd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Verify FFmpeg installation:
bashffmpeg -version
3. Frontend Setup
bashcd ../frontend
npm install
4. Environment Configuration
Create a .env file in the root directory:
env# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration
CHROMA_PERSIST_DIR=./data/db

# File Upload Configuration
UPLOAD_DIR=./data/uploads
AUDIO_DIR=./data/audio
TRANSCRIPTION_DIR=./data/transcriptions
MAX_FILE_SIZE=2147483648  # 2GB in bytes

# API Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173

# Whisper Configuration
WHISPER_MODEL=base  # Options: tiny, base, small, medium, large
WHISPER_DEVICE=cpu  # Options: cpu, cuda

# Chunking Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
🏃‍♂️ Running the Application
Start Backend (FastAPI)
bashcd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
Backend API will be available at: http://127.0.0.1:8000
API Documentation: http://127.0.0.1:8000/docs
Start Frontend (React)
bashcd frontend
npm run dev
Frontend will be available at: http://localhost:5173
📦 API Endpoints
Upload Endpoints

POST /api/upload - Upload video file for processing
GET /api/upload/status/{upload_id} - Check processing status
GET /api/upload/transcription/{upload_id} - Get transcription result

Chat Endpoints

POST /api/chat - Ask questions about uploaded lecture
GET /api/chat/history/{session_id} - Retrieve chat history

Health Check

GET /api/health - Application health status

🔧 Key Features
Video Processing Pipeline

Video Upload - Accepts MP4, AVI, MOV formats
Audio Extraction - Uses FFmpeg to extract audio
Transcription - Faster Whisper for speech-to-text
Semantic Chunking - Intelligent text segmentation
Vector Indexing - ChromaDB for similarity search

RAG Implementation

Retrieval: Semantic search using embeddings
Augmentation: Context-aware prompt engineering
Generation: Gemini API for natural responses

Frontend Features

Drag & Drop Upload - Intuitive file upload
Real-time Status - Processing progress updates
Chat Interface - Natural language Q&A
Responsive Design - Mobile-friendly UI

🛠 Troubleshooting
Common Issues
FFmpeg not found (WinError 2)

Install FFmpeg from https://ffmpeg.org/download.html
Add FFmpeg to system PATH
Restart terminal/IDE

Module not found errors
bash# Backend
pip install -r requirements.txt

# Frontend
npm install
CORS errors

Check that frontend URL is correctly configured in backend CORS settings
Verify API endpoints are accessible

Gemini API errors

Verify API key is valid and has quota
Check network connectivity
Review API usage limits

ChromaDB initialization errors

Ensure write permissions for data directory
Check disk space availability
Verify ChromaDB version compatibility

Performance Optimization
For large video files:

Use medium or large Whisper model for better accuracy
Enable GPU acceleration if available (set WHISPER_DEVICE=cuda)
Increase chunk size for faster processing

For better search results:

Adjust chunk size and overlap parameters
Use higher-quality embedding models
Fine-tune similarity search thresholds

📋 Requirements Files
Backend (requirements.txt)
txtfastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
faster-whisper==0.9.0
chromadb==0.4.15
google-generativeai==0.3.1
sentence-transformers==2.2.2
pydantic==2.5.0
python-dotenv==1.0.0
aiofiles==23.2.1
numpy==1.25.2
librosa==0.10.1
Frontend (package.json dependencies)
json{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "axios": "^1.6.0",
    "tailwindcss": "^3.3.6"
  }
}
📚 Credits
Built with ❤️ for educational purposes.
Powered by:

OpenAI Whisper - Speech recognition
Google Gemini - Large language model
ChromaDB - Vector database
FastAPI - Modern web framework
React - Frontend library

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.