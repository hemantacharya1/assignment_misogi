# HR Onboarding Knowledge Assistant

Replace time-consuming HR induction calls with an AI assistant that instantly answers employee questions based on uploaded HR policy documents.

## Features

* Upload HR documents (PDF, DOCX, TXT)
* Text extraction and intelligent chunking
* Vector embedding storage using ChromaDB
* Semantic search for relevant policy chunks
* LLM-based summarization for natural answers
* Metadata with document names and chunk indexes
* Simple React + Tailwind frontend for upload and chat
* CORS enabled backend API with FastAPI and Uvicorn

## Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Vector Store:** ChromaDB (local embedding database)
* **Embeddings:** HuggingFace or other open-source models
* **Frontend:** React (Vite), Tailwind CSS
* **AI Summarization:** Gemini API / OpenAI (configurable)

## Getting Started

### Prerequisites

* Python 3.10+
* Node.js 16+
* Git

### Backend Setup

1. Clone repo:

```bash
git clone https://github.com/yourusername/hr-onboarding-assistant.git
cd hr-onboarding-assistant/backend
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run backend server:

```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd ../frontend
```

2. Install dependencies:

```bash
npm install
```

3. Run frontend:

```bash
npm run dev
```

4. Open `http://localhost:5173` in your browser.

## Usage

* Upload HR documents via the frontend UI.
* Ask questions related to company policies in the chat box.
* Get summarized, context-aware answers with citations to original documents.

## Project Structure

```
backend/
├─ app/
│  ├─ main.py           # FastAPI app and routes
│  ├─ ingestion.py      # Document processing & storage
│  ├─ utils.py          # File extraction and chunking helpers
│  ├─ embedder.py       # Embedding model code
│  └─ vector_store.py   # ChromaDB client setup
frontend/
├─ src/
│  ├─ components/       # React components
│  ├─ App.jsx           # Main React app
│  └─ main.jsx          # React entrypoint
```

## Configuration

* Update your AI API keys and endpoints in backend environment variables or config.
* Adjust chunking strategy or embedding models in `utils.py` and `embedder.py`.

## Notes

* This project uses ChromaDB as a local vector store for development.
* CORS middleware is enabled for frontend-backend communication.
* Summarization is done by sending combined retrieved chunks to an LLM API.

## License

MIT License