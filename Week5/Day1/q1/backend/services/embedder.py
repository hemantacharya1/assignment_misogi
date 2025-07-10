from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: list) -> list:
    return model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)

def embed_query(query: str) -> list:
    return model.encode([query], convert_to_numpy=True)[0]