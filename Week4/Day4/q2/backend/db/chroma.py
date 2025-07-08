# backend/db/chroma.py
import os
import json
import chromadb
from chromadb.config import Settings
from backend.config import settings

client = chromadb.Client(Settings(persist_directory=settings.CHROMA_DB_PATH))
collection = client.get_or_create_collection(name="lecture_chunks")

CHUNK_OUTPUT_DIR = "data/chunks"

def store_chunks(video_id: str):
    chunk_path = os.path.join(CHUNK_OUTPUT_DIR, f"{video_id}.json")
    with open(chunk_path, "r") as f:
        chunks = json.load(f)

    for idx, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk["text"]],
            embeddings=[chunk["embedding"]],
            ids=[f"{video_id}_{idx}"],
            metadatas=[{"start": chunk["start"], "end": chunk["end"], "video_id": video_id}]
        )

    return len(chunks)

def query_chunks(query_embedding, top_k=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results
