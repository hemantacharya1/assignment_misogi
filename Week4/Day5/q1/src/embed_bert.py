# src/embed_bert.py
import pandas as pd
import numpy as np
from tqdm import tqdm
import torch
from transformers import BertTokenizer, BertModel
import joblib

DATA_PATH = "data/raw/articles.csv"
EMB_PATH = "embeddings/bert_embeddings.npy"
LABEL_PATH = "embeddings/bert_labels.npy"

MODEL_NAME = "bert-base-uncased"

def preprocess(text):
    return text.strip()

def main():
    df = pd.read_csv(DATA_PATH)
    texts = df['text'].apply(preprocess).tolist()
    labels = df['label'].tolist()

    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertModel.from_pretrained(MODEL_NAME)
    model.eval()  # inference mode

    embeddings = []

    with torch.no_grad():
        for text in tqdm(texts, desc="Generating BERT embeddings"):
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            outputs = model(**inputs)
            cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()  # CLS token
            embeddings.append(cls_embedding)

    embeddings = np.array(embeddings)
    labels = np.array(labels)

    np.save(EMB_PATH, embeddings)
    np.save(LABEL_PATH, labels)
    print("✅ Saved BERT embeddings and labels.")

if __name__ == "__main__":
    main()
