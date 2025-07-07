import chromadb

def get_chroma_collection():
    client = chromadb.PersistentClient(path="chroma_store")  # ✅ new-style client
    return client.get_or_create_collection(name="hr_docs")
