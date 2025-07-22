import os
import numpy as np
import joblib
import torch
from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- missing in your code
from pydantic import BaseModel                      # <-- missing in your code
import openai

from sklearn.linear_model import LogisticRegression
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk                                          # <-- needed for nltk.download()
import string


# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')  
# Load classifiers and label encoders
MODEL_DIR = "models"

classifiers = {
    "glove": joblib.load(os.path.join(MODEL_DIR, "glove_classifier.pkl")),
    "bert": joblib.load(os.path.join(MODEL_DIR, "bert_classifier.pkl")),
    "sbert": joblib.load(os.path.join(MODEL_DIR, "sbert_classifier.pkl")),
    "openai": joblib.load(os.path.join(MODEL_DIR, "openai_classifier.pkl")),
}

encoders = {
    "glove": joblib.load(os.path.join(MODEL_DIR, "glove_label_encoder.pkl")),
    "bert": joblib.load(os.path.join(MODEL_DIR, "bert_label_encoder.pkl")),
    "sbert": joblib.load(os.path.join(MODEL_DIR, "sbert_label_encoder.pkl")),
    "openai": joblib.load(os.path.join(MODEL_DIR, "openai_label_encoder.pkl")),
}

# Load Embedding Models
glove_vectors = {}
with open("data/glove/glove.6B.100d.txt", encoding="utf8") as f:
    for line in f:
        values = line.strip().split()
        glove_vectors[values[0]] = np.array(values[1:], dtype='float32')

bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertModel.from_pretrained("bert-base-uncased")

sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

stop_words = set(stopwords.words("english"))
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in string.punctuation and t not in stop_words]
    return tokens

def embed_glove(text):
    tokens = preprocess_text(text)
    vectors = [glove_vectors[t] for t in tokens if t in glove_vectors]
    return np.mean(vectors, axis=0) if vectors else np.zeros(100)

def embed_bert(text):
    inputs = bert_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    return cls_embedding

def embed_sbert(text):
    return sbert_model.encode([text])[0]

def embed_openai(text):
    try:
        res = openai.Embedding.create(model="text-embedding-ada-002", input=text)
        return res["data"][0]["embedding"]
    except Exception as e:
        print(f"[OpenAI Error] {e}")
        return [0.0] * 1536

def get_prediction(embedding, clf, encoder):
    probs = clf.predict_proba([embedding])[0]
    idx = np.argmax(probs)
    return {
        "label": encoder.inverse_transform([idx])[0],
        "confidence": round(float(probs[idx]), 4)
    }



app = FastAPI(title="Smart Article Categorizer")

# Allow CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ArticleRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Article Categorizer API is running"}

@app.post("/predict")
def predict_article(request: ArticleRequest):
    text = request.text

    embeddings = {
        "glove": embed_glove(text),
        "bert": embed_bert(text),
        "sbert": embed_sbert(text),
        "openai": embed_openai(text),
    }

    results = {}
    for key in embeddings:
        result = get_prediction(
            embeddings[key],
            classifiers[key],
            encoders[key]
        )
        results[key] = result

    return results

