import os
import chromadb
import requests
from sentence_transformers import SentenceTransformer
from app.utils.classifier import classify_intent

# Setup embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Setup ChromaDB client
chroma_client = chromadb.Client()

# Define intent to collection mapping
INTENT_COLLECTIONS = {
    "tech_support": "tech_support_docs",
    "billing": "billing_docs",
    "feature_requests": "feature_request_docs",
}

def embed_texts(texts):
    return embedder.encode(texts).tolist()

def load_documents_from_folder(folder_path):
    docs = []
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        if os.path.isfile(fpath) and fname.endswith((".txt", ".md")):
            with open(fpath, "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs

def ingest_documents(base_path="docs"):
    print("Ingesting documents into Chroma...")
    for intent, collection_name in INTENT_COLLECTIONS.items():
        folder = os.path.join(base_path, intent)
        if not os.path.exists(folder):
            print(f"Skipping {intent}: folder not found")
            continue

        documents = load_documents_from_folder(folder)
        embeddings = embed_texts(documents)

        # Delete and recreate collection
        try:
            chroma_client.delete_collection(name=collection_name)
        except Exception:
            pass  # Collection may not exist

        collection = chroma_client.create_collection(name=collection_name)

        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            collection.add(documents=[doc], embeddings=[emb], ids=[f"{intent}_{i}"])

        print(f"Ingested {len(documents)} docs into {collection_name}.")

def retrieve_context(intent, query, top_k=3):
    collection_name = INTENT_COLLECTIONS.get(intent)
    if not collection_name:
        raise ValueError(f"Unknown intent: {intent}")

    collection = chroma_client.get_collection(name=collection_name)
    query_emb = embed_texts([query])[0]
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)

    return results["documents"][0] if results and results["documents"] else []

# -------------------------------------------
# LLM-based Answer Generation
# -------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_ollama(prompt, model="llama2:7b"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=20,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"Ollama failed: {e}")
        return None

def call_gemini(prompt):
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": GEMINI_API_KEY}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Gemini fallback failed: {e}")
        return "Sorry, I couldn't generate an answer at this time."

def build_prompt(context_chunks, query):
    context = "\n\n".join(context_chunks)
    return f"""You are a helpful assistant. Use the following context to answer the user's question.

Context:
{context}

User question: {query}
Answer:"""

def answer_query(query):
    # 1. Classify intent
    intent_label, _ = classify_intent(query)
    print(intent_label)
    intent = intent_label.lower().replace("/", "_") 
    print(intent)

    # 2. Retrieve context
    context_chunks = retrieve_context(intent, query)

    # 3. Build prompt
    prompt = build_prompt(context_chunks, query)

    # 4. Generate answer
    answer = call_ollama(prompt)
    if not answer:
        answer = call_gemini(prompt)

    return {
        "intent": intent,
        "context": context_chunks,
        "answer": answer
    }
