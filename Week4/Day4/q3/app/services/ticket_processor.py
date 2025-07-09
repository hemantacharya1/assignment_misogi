from app.rag.embeddings import get_embedding
from app.rag.loader import vector_store
from app.core.config import settings
import google.generativeai as genai

genai.configure(api_key=settings.GEMINI_API_KEY)

def process_ticket(title: str, description: str) -> dict:
    """
    Enrich a new ticket using RAG:
    - Retrieve similar KB/docs
    - Generate smart response via Gemini
    - Assign category, tags, priority
    """

    full_text = f"{title.strip()}\n{description.strip()}"
    ticket_vector = get_embedding(full_text)

    # Retrieve similar documents
    relevant_chunks = vector_store.search(ticket_vector, top_k=5)

    # Build context for Gemini
    context = "\n\n".join([
        f"[{c['source'].upper()}] {c.get('section') or c.get('title')}: {c['content'] or c['description']}\nResponse: {c.get('response', '')}"
        for c in relevant_chunks
    ])

    # Prompt Gemini
    prompt = f"""
You are a helpful customer support agent. Use the following context to answer the customer's issue.

Context:
{context}

Customer Query:
{full_text}

Provide:
- A helpful response
- Category
- Priority (high/medium/low)
- Tags (comma-separated)
Format the output as JSON with keys: response, category, priority, tags.
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(prompt)
    
    try:
        import json
        parsed = json.loads(result.text)
    except Exception:
        parsed = {
            "response": result.text.strip(),
            "category": "Uncategorized",
            "priority": "medium",
            "tags": "general"
        }

    parsed["confidence_score"] = 1.0  # Can be adjusted later based on logic
    return parsed
