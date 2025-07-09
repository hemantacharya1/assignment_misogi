# 🧠 Smart Customer Support Ticketing System

An intelligent customer support platform that auto-categorizes tickets and generates smart replies using a Retrieval-Augmented Generation (RAG) architecture.

![Project Structure](https://img.shields.io/badge/status-active-success) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green) ![React](https://img.shields.io/badge/React-18+-61DAFB)

## 🌟 Features

- **Auto-categorization** of support tickets using AI
- **Smart reply generation** with RAG architecture
- **Priority assignment** based on content analysis
- **Similar case retrieval** via vector embeddings
- **Confidence scoring** for automatic escalation
- **Modern UI** with React and Tailwind CSS

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with pgvector extension
- **Embeddings**: Open Source BGE (BAAI General Embedding)
- **Vector Search**: Semantic search with vector DB

### Frontend
- **Framework**: React.js (Vite)
- **Styling**: Tailwind CSS 3.x

### AI Components
- **LLM**: Gemini API / Open-source models
- **RAG Pipeline**: Custom retrieval-augmented generation

## 📂 Project Structure
📦 root/
├── app/ # FastAPI backend
│ ├── api/ # API routes
│ ├── core/ # Config & setup
│ ├── db/ # DB models & session
│ ├── rag/ # Embedding & vector store
│ ├── services/ # Ticket processing logic
│ └── main.py # FastAPI entrypoint
├── support-frontend/ # React + Vite + Tailwind frontend
├── .gitignore
├── README.md
└── requirements.txt

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+ with pgvector extension
- API key for Gemini (or alternative LLM setup)

### Installation

#### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# or
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory with:

text
DATABASE_URL=postgresql://user:password@localhost/dbname
EMBEDDING_MODEL=BAAI/bge-small-en
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_api_key
Run the FastAPI server:

bash
uvicorn app.main:app --reload
Frontend Setup
Navigate to frontend directory:

bash
cd support-frontend
Install dependencies:

bash
npm install
Run development server:

bash
npm run dev
🔧 Configuration
Ensure CORS is properly configured in the backend for the frontend URL (default: http://localhost:5173).

🧪 Sample Use Cases
Customer Query	Auto-Tag	Priority	Suggested Action
"Where is my order?"	Shipping Issue	Medium	Provide tracking info
"Refund for broken item"	Returns	High	Initiate return process
"How to reset password?"	Account	Low	Send password reset link
🤝 Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

📬 Contact
Created by Hemant Acharya for learning purposes 🚀

For questions or suggestions, please open an issue on GitHub.

📝 License
This project is open-source and available under the MIT License.