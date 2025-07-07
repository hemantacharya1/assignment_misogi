import os
import uuid
from app.utils import extract_text_from_file, chunk_text
from app.embedder import embed_chunks
from app.vector_store import get_chroma_collection


UPLOAD_DIR = "uploads/"

def process_and_store_document(filename, file_bytes):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    text = extract_text_from_file(file_path)
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)

    collection = get_chroma_collection()

    metadatas = [{"document_name": filename, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=[f"{filename}_{i}" for i in range(len(chunks))]
    )

    # REMOVE this line:
    # collection.add(...)

    return len(chunks)
