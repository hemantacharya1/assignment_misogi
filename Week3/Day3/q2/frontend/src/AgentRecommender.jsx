import { useState } from "react";

export default function AgentRecommender() {
  const [task, setTask] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!task.trim()) return;
    setLoading(true);
    setResults([]);
    try {
      const res = await fetch("http://localhost:5000/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task }),
      });
      const data = await res.json();
      if (data.results) setResults(data.results);
    } catch (err) {
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-4 text-center">🧠 Agent Recommender</h1>
        <textarea
          rows={4}
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Describe your coding task..."
          className="w-full p-4 rounded-xl bg-gray-800 border border-gray-700 mb-4"
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-xl w-full"
        >
          {loading ? "Recommending..." : "Get Recommendations"}
        </button>

        {results.length > 0 && (
          <div className="mt-8 space-y-6">
            {results.map((agent, index) => (
              <div key={index} className="p-4 border border-gray-700 rounded-xl bg-gray-800">
                <h2 className="text-xl font-semibold">{index + 1}. {agent.name} <span className="text-sm text-gray-400">(Score: {agent.score})</span></h2>
                <p className="text-gray-300 mt-1">{agent.description}</p>
                <ul className="list-disc list-inside mt-2 text-green-400 text-sm">
                  {agent.reasons.map((reason, i) => (
                    <li key={i}>{reason}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
