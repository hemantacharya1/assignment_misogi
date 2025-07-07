from app.vector_store import get_chroma_collection
from app.embedder import embed_chunks

def query_hr_docs(question: str, top_k: int = 3) -> str:
    embedding = embed_chunks([question])[0]  # Single vector

    collection = get_chroma_collection()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    # Combine top chunks into a simple answer
    top_chunks = results['documents'][0]
    metadatas = results['metadatas'][0]

    answer = ""
    for i, chunk in enumerate(top_chunks):
        source = metadatas[i].get("document_name", "Unknown")
        answer += f"📄 From `{source}`:\n{chunk}\n\n"

    return answer.strip()
