from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: list[str]) -> list[list[float]]:
    return model.encode(chunks, convert_to_numpy=True).tolist()
