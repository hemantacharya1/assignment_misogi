import chromadb

# Use the new Chroma client (no deprecated Settings API)
client = chromadb.PersistentClient(path="./db")

collection_name = "pdf_chunks"

if collection_name in [c.name for c in client.list_collections()]:
    collection = client.get_collection(collection_name)
else:
    collection = client.create_collection(name=collection_name)

def add_chunks_to_vector_db(chunks: list[str], embeddings: list[list[float]], source: str):
    ids = [f"{source}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]

    collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)

def query_vector_db(query_embedding: list[float], top_k=5):
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results
