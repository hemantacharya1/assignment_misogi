# backend/services/gemini_client.py
import google.generativeai as genai
from backend.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def ask_gemini(question: str, context: str) -> str:
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    response = model.generate_content(prompt)
    return response.text.strip()
