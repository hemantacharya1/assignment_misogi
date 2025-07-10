import requests
import os

SERPER_API_KEY = "6ba4aa9bac9943515d0d47e5b1f4d1198e364c1f"
SERPER_SEARCH_URL = "https://google.serper.dev/search"

def search_web(query: str, num_results: int = 5) -> dict:
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": num_results
    }
    response = requests.post(SERPER_SEARCH_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Serper API error: {response.text}")

    data = response.json()

    # Extract titles, snippets, URLs for summarization and sources
    snippets = []
    sources = []

    for result in data.get("organic", []):
        snippet = result.get("snippet", "")
        url = result.get("link", "")
        title = result.get("title", "")
        snippets.append(snippet)
        sources.append({"type": "web", "source": url, "title": title})

    return {"snippets": snippets, "sources": sources}
