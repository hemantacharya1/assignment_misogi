import json
from pathlib import Path
from app.rag.embeddings import get_embedding
from app.rag.vector_store import VectorStore

# Instantiate the shared vector store
vector_store = VectorStore()

def load_kb(kb_path: Path = Path("app/kb/docs.json")):
    with open(kb_path, "r", encoding="utf-8") as f:
        kb_data = json.load(f)
    for doc in kb_data:
        content = doc["content"]
        embedding = get_embedding(content)
        vector_store.add(
            id=doc["id"],
            vector=embedding,
            metadata={
                "source": "kb",
                "section": doc.get("section", ""),
                "content": content
            }
        )

def load_historical_tickets(path: Path = Path("data/historical_tickets.json")):
    with open(path, "r", encoding="utf-8") as f:
        tickets = json.load(f)
    for i, t in enumerate(tickets):
        full_text = f"{t['title']}\n{t['description']}"
        embedding = get_embedding(full_text)
        vector_store.add(
            id=t.get("id", f"ht_{i}"),
            vector=embedding,
            metadata={
                "source": "history",
                "title": t["title"],
                "description": t["description"],
                "response": t.get("response", ""),
                "category": t.get("category", "")
            }
        )

def initialize_vector_store():
    load_kb()
    load_historical_tickets()
    print(f"Vector store initialized with {len(vector_store.vectors)} entries.")
