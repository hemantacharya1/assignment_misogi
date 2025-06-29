import { useState } from "react";
import "./index.css";

const tools = [
  { value: "cursor", label: "Cursor AI" },
  { value: "copilot", label: "GitHub Copilot" },
  { value: "replit", label: "Replit" },
  { value: "codewhisperer", label: "Amazon CodeWhisperer" },
  { value: "tabnine", label: "Tabnine" },
];

function App() {
  const [prompt, setPrompt] = useState("");
  const [tool, setTool] = useState(tools[0].value);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleOptimize = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setResult(null);

    const res = await fetch("http://localhost:5000/api/optimize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, tool }),
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="w-full max-w-4xl bg-white shadow-xl rounded-2xl p-8 space-y-6">
        <h1 className="text-3xl font-bold text-center text-blue-700">Adaptive Prompt Optimizer</h1>

        <div className="space-y-2">
          <label className="font-semibold">Select Tool:</label>
          <select
            value={tool}
            onChange={(e) => setTool(e.target.value)}
            className="w-full p-2 border rounded-md"
          >
            {tools.map((t) => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <label className="font-semibold">Enter Base Prompt:</label>
          <textarea
            rows={5}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full p-3 border rounded-md resize-none"
            placeholder="e.g., Sort a list of integers in Python"
          />
        </div>

        <button
          onClick={handleOptimize}
          disabled={loading}
          className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition"
        >
          {loading ? "Optimizing..." : "Optimize Prompt"}
        </button>

        {result && (
          <div className="space-y-4 mt-4">
            {result.error ? (
              <p className="text-red-600 font-medium">{result.error}</p>
            ) : (
              <>
                <div>
                  <h3 className="font-semibold text-lg text-gray-700">🔧 Optimized Prompt:</h3>
                  <pre className="bg-gray-50 border p-4 rounded-md text-sm whitespace-pre-wrap">
                    {result.optimized_prompt}
                  </pre>
                </div>
                <div>
                  <h3 className="font-semibold text-lg text-gray-700">🧠 Explanation:</h3>
                  <p className="bg-gray-50 border p-4 rounded-md text-sm whitespace-pre-wrap">
                    {result.explanation}
                  </p>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
