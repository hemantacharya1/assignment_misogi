import ChatBox from "./ChatBox";

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              🤖 MCP Q&A Chatbot
            </h1>
            <p className="text-gray-600">
              Ask questions about Model Context Protocol (MCP)
            </p>
          </div>
          <ChatBox />
        </div>
      </div>
    </div>
  );
}

export default App;
