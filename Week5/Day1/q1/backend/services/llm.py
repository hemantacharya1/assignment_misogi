import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_answer(question: str, contexts: list) -> str:
    context_text = "\n\n".join(contexts)
    prompt = f"""You are a helpful medical assistant. Use the following context to answer the question.

Context:
{context_text}

Question: {question}
Answer:"""

    response = model.generate_content(prompt)
    return response.text.strip()
