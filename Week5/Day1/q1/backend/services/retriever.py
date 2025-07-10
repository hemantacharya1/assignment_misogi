import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="medical_docs")

def retrieve_chunks(query_embedding, k=4):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return [
        {"document": doc, "metadata": meta}
        for doc, meta in zip(documents, metadatas)
    ]
