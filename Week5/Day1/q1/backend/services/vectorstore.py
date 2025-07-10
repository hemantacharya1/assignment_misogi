import chromadb

# ✅ Correct new client initialization (local persistent)
client = chromadb.PersistentClient(path="./chroma_db")

# ✅ Create or get the collection
collection = client.get_or_create_collection(name="medical_docs")

def store_chunks(chunks: list, embeddings: list):
    documents = [chunk for chunk in chunks]
    ids = [f"chunk-{i}" for i in range(len(chunks))]

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"source": "pdf"} for _ in chunks]
    )
