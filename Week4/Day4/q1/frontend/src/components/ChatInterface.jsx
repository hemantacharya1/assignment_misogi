import { useState } from 'react';

export default function ChatInterface() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleQuery = async () => {
    if (!query) return;

    const res = await fetch("http://localhost:8000/query/", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();
    setResponse(data.answer || "No response");
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-lg font-semibold mb-2">Ask a Question</h2>
      <textarea
        className="w-full border rounded p-2"
        rows={3}
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="e.g. How many vacation days do I get?"
      />
      <button
        onClick={handleQuery}
        className="mt-2 bg-green-600 text-white px-4 py-1 rounded hover:bg-green-700"
      >
        Ask
      </button>
      {response && (
        <div className="mt-4 p-3 border rounded bg-gray-50">
          <p><strong>Response:</strong> {response}</p>
        </div>
      )}
    </div>
  );
}
