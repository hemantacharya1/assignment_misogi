# backend/core/chunking.py
import os
import json
from sentence_transformers import SentenceTransformer
from backend.utils.text_utils import split_into_chunks
from backend.config import settings

model = SentenceTransformer("all-MiniLM-L6-v2")

CHUNK_OUTPUT_DIR = "data/chunks"
TRANSCRIPT_DIR = "data/transcripts"

os.makedirs(CHUNK_OUTPUT_DIR, exist_ok=True)

def process_transcript(video_id: str):
    transcript_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}.json")
    if not os.path.exists(transcript_path):
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")

    with open(transcript_path, "r") as f:
        transcript = json.load(f)

    segments = transcript["segments"]
    chunks = split_into_chunks(segments)

    for chunk in chunks:
        chunk["embedding"] = model.encode(chunk["text"]).tolist()

    chunk_path = os.path.join(CHUNK_OUTPUT_DIR, f"{video_id}.json")
    with open(chunk_path, "w") as f:
        json.dump(chunks, f, indent=2)

    return chunk_path
