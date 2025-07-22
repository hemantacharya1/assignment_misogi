# src/embed_sbert.py
import pandas as pd
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import joblib

DATA_PATH = "data/raw/articles.csv"
EMB_PATH = "embeddings/sbert_embeddings.npy"
LABEL_PATH = "embeddings/sbert_labels.npy"

MODEL_NAME = "all-MiniLM-L6-v2"

def preprocess(text):
    return text.strip()

def main():
    df = pd.read_csv(DATA_PATH)
    texts = df['text'].apply(preprocess).tolist()
    labels = df['label'].tolist()

    model = SentenceTransformer(MODEL_NAME)

    print("Generating SBERT embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    np.save(EMB_PATH, embeddings)
    np.save(LABEL_PATH, np.array(labels))
    print("✅ Saved SBERT embeddings and labels.")

if __name__ == "__main__":
    main()
