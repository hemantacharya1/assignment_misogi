from utils import get_llm, get_db_toolkit

llm = get_llm()

db_map = {
    "blinkit": "db/blinkit.db",
    "zepto": "db/zepto.db",
    "bigbasket": "db/bigbasket.db"
}

def choose_db(user_query: str) -> str:
    query_lower = user_query.lower()
    if "blinkit" in query_lower:
        return "blinkit"
    elif "zepto" in query_lower:
        return "zepto"
    elif "bigbasket" in query_lower:
        return "bigbasket"
    return "all"  # default/fallback

def run_agent(user_query: str):
    target = choose_db(user_query)

    if target == "all":
        results = []
        for key, db_path in db_map.items():
            print(f"\n🔍 Searching in {key.title()}...")
            agent = get_db_toolkit(db_path, llm)
            try:
                answer = agent.run(user_query)
                results.append((key, answer))
            except Exception as e:
                results.append((key, f"Error: {str(e)}"))
        return results
    else:
        print("----------------------alll------------------",db_map[target])
        agent = get_db_toolkit(db_map[target], llm)
        print(agent)
        return [(target, agent.run(user_query))]

if __name__ == "__main__":
    while True:
        q = input("\n🧠 Ask your question (or type 'exit'): ")
        if q.strip().lower() == "exit":
            break
        answers = run_agent(q)
        for source, ans in answers:
            print(f"\n📦 {source.title()}:\n{ans}")
