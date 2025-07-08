import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import ChatPage from "./pages/ChatPage";

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow p-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-blue-600">Lecture Q&A</h1>
          <div className="space-x-4">
            <Link to="/" className="text-blue-500 hover:underline">Upload</Link>
            <Link to="/chat" className="text-blue-500 hover:underline">Chat</Link>
          </div>
        </nav>
        <main className="p-6">
          <Routes>
            <Route path="/" element={<UploadPage />} />
            <Route path="/chat" element={<ChatPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
