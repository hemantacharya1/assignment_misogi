import requests
import os

GEMINI_API_URL = "https://api.gemini.ai/v1/chat/completions"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Store your key in environment variable

def summarize_answer(query: str, texts: list[str], sources: list[dict]) -> str:
    """
    Summarizes and synthesizes answers using Gemini 1.5 Flash.
    Includes inline citations from sources.
    """
    # Build a prompt that includes query + context texts + source info
    prompt = f"Answer the query based on the following information:\n\n"
    for i, text in enumerate(texts):
        prompt += f"[Source {i+1}]: {text}\n"
    prompt += f"\nProvide a concise answer citing the relevant sources (e.g. [Source 1])."

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gemini-1.5-flash",
        "messages": [
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 512,
        "top_p": 1,
        "n": 1
    }

    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.text}")

    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    return answer
