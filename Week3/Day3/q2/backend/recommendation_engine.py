import json
import subprocess
import re
from typing import List, Dict

OLLAMA_MODEL = "mistral:instruct"


def call_ollama(prompt: str) -> List[str]:
    """Call Ollama model to extract relevant task tags."""
    ollama_prompt = f"""
    You are an AI assistant helping classify software development tasks.
    Given the following task description, return 3–5 relevant tags from this list:
    ["scripting", "debugging", "refactor", "cloud", "frontend", "api", "testing", "education", "data", "privacy", "chat", "completion"]

    Task: "{prompt}"

    Respond only with a JSON list, like:
    ["scripting", "data", "cloud"]
    """

    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=ollama_prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=900
    )

    output = result.stdout.decode().strip()
 # Extract JSON array from LLM output using regex
    match = re.search(r'\[.*?\]', output)
    if match:
        try:
            tags = json.loads(match.group(0))
            return tags if isinstance(tags, list) else []
        except json.JSONDecodeError:
            print("⚠️ Failed to parse JSON list:", match.group(0))
            return []
    else:
        print("⚠️ No JSON list found in LLM output:", output)
        return []

def load_agents_db(filepath: str = "agents_db.json") -> List[Dict]:
    with open(filepath, "r") as f:
        return json.load(f)


def score_agents(task_tags: List[str], agents: List[Dict]) -> List[Dict]:
    scored = []
    for agent in agents:
        print(f"🔍 Scoring {agent['name']}")
        print("Agent Tags:", agent.get("tags", []))
        print("Agent Best For:", agent.get("best_for", []))
        score = 0
        reasons = []
        for tag in task_tags:
            if tag in agent.get("tags", []) or tag in agent.get("best_for", []):
                score += 1
                reasons.append(f"Matches tag: '{tag}'")
        scored.append({
            "id": agent["id"],
            "name": agent["name"],
            "score": score,
            "reasons": reasons,
            "description": agent["description"]
        })
    return sorted(scored, key=lambda x: x["score"], reverse=True)



def recommend(task_description: str, top_k: int = 3) -> List[Dict]:
    print("🔎 Classifying task via Mistral...")
    tags = call_ollama(task_description)
    print("📌 Tags:", tags)

    agents = load_agents_db()
    ranked = score_agents(tags, agents)
    return ranked[:top_k]


if __name__ == "__main__":
    task = input("Describe your coding task: ")
    results = recommend(task)

    print("\n✅ Recommended Agents:")
    for agent in results:
        print(f"\n➡️ {agent['name']} (Score: {agent['score']})")
        print(f"   {agent['description']}")
        for reason in agent['reasons']:
            print(f"   • {reason}")
