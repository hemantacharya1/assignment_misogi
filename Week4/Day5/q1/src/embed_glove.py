# src/embed_glove.py
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import string
import joblib

nltk.download('punkt')
nltk.download('stopwords')

GLOVE_PATH = "data/glove/glove.6B.100d.txt"
DATA_PATH = "data/raw/articles.csv"
OUTPUT_EMB_PATH = "embeddings/glove_embeddings.npy"
OUTPUT_LABEL_PATH = "embeddings/glove_labels.npy"

# Load GloVe vectors
def load_glove_vectors(glove_path):
    glove = {}
    with open(glove_path, 'r', encoding='utf8') as f:
        for line in tqdm(f, desc="Loading GloVe"):
            parts = line.split()
            word = parts[0]
            vector = np.array(parts[1:], dtype='float32')
            glove[word] = vector
    return glove

# Preprocess text
def preprocess(text):
    tokens = wordpunct_tokenize(text.lower())  # <- safer tokenizer
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in string.punctuation and t not in stop_words]
    return tokens

# Convert article to vector
def text_to_vector(tokens, glove, dim=100):
    vectors = [glove[word] for word in tokens if word in glove]
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(dim)

def main():
    df = pd.read_csv(DATA_PATH)
    glove = load_glove_vectors(GLOVE_PATH)
    dim = len(next(iter(glove.values())))

    embeddings = []
    labels = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Generating GloVe embeddings"):
        tokens = preprocess(row['text'])
        vec = text_to_vector(tokens, glove, dim)
        embeddings.append(vec)
        labels.append(row['label'])

    embeddings = np.array(embeddings)
    labels = np.array(labels)

    np.save(OUTPUT_EMB_PATH, embeddings)
    np.save(OUTPUT_LABEL_PATH, labels)
    print("✅ Saved GloVe embeddings and labels.")

if __name__ == "__main__":
    main()
