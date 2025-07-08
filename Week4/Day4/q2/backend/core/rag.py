# backend/core/rag.py
from sentence_transformers import SentenceTransformer
from backend.db.chroma import query_chunks
from backend.services.gemini_client import ask_gemini

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def rag_chat(question: str):
    query_embedding = embedder.encode(question).tolist()
    results = query_chunks(query_embedding)

    retrieved_chunks = results["documents"][0]
    context = "\n\n".join(retrieved_chunks)

    answer = ask_gemini(question, context)
    return {
        "answer": answer,
        "references": results["metadatas"][0]
    }
