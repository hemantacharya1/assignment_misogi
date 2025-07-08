import { useState } from "react";

export default function ChatBox() {
  const [input, setInput] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setChat((prev) => [...prev, { role: "user", text: input }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });
      const data = await res.json();
      if (res.ok) {
        setChat((prev) => [...prev, { role: "bot", text: data.answer }]);
      } else {
        setChat((prev) => [...prev, { role: "bot", text: "Error: " + data.detail }]);
      }
    } catch (err) {
      setChat((prev) => [...prev, { role: "bot", text: "Request failed." }]);
    }
    setLoading(false);
  };

  return (
    <div className="bg-white shadow p-6 rounded-lg space-y-4">
      <div className="h-64 overflow-y-auto border rounded p-3 bg-gray-50">
        {chat.map((msg, idx) => (
          <div key={idx} className={`mb-2 ${msg.role === "user" ? "text-right" : "text-left"}`}>
            <span className={`inline-block px-3 py-2 rounded ${msg.role === "user" ? "bg-blue-200" : "bg-gray-200"}`}>
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border px-3 py-2 rounded"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
