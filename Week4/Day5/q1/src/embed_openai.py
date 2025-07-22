# src/embed_openai.py
import os
import time
import pandas as pd
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv
import openai

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DATA_PATH = "data/raw/articles.csv"
EMB_PATH = "embeddings/openai_embeddings.npy"
LABEL_PATH = "embeddings/openai_labels.npy"

EMBED_MODEL = "text-embedding-ada-002"

def get_openai_embedding(text):
    try:
        response = openai.Embedding.create(
            model=EMBED_MODEL,
            input=text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Error fetching embedding: {e}")
        return [0.0] * 1536  # fallback zero vector if failed

def preprocess(text):
    return text.strip().replace("\n", " ")

def main():
    df = pd.read_csv(DATA_PATH)
    texts = df['text'].apply(preprocess).tolist()
    labels = df['label'].tolist()

    embeddings = []

    print("Generating OpenAI embeddings...")
    for text in tqdm(texts):
        emb = get_openai_embedding(text)
        embeddings.append(emb)
        time.sleep(0.5)  # avoid rate limits (optional for small usage)

    embeddings = np.array(embeddings)
    labels = np.array(labels)

    np.save(EMB_PATH, embeddings)
    np.save(LABEL_PATH, labels)
    print("✅ Saved OpenAI embeddings and labels.")

if __name__ == "__main__":
    main()
