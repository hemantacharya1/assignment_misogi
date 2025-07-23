from chroma.setup import get_chroma_client
from uuid import uuid4

def store_chunks(chunks: list[str], metadata: dict):
    client = get_chroma_client()
    collection = client.get_or_create_collection(name="legal_chunks")

    ids = [str(uuid4()) for _ in chunks]
    metadatas = [metadata for _ in chunks]

    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ Stored {len(chunks)} chunks in ChromaDB.")
