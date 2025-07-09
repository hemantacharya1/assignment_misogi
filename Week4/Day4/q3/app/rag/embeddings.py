from sentence_transformers import SentenceTransformer

# Load model once globally (takes some time on first run)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> list[float]:
    """
    Generate embedding vector for the input text.
    """
    embedding = model.encode(text)
    return embedding.tolist()  # Convert numpy array to list
