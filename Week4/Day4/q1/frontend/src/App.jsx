import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 text-gray-800 p-4">
      <div className="max-w-4xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold text-center">HR Knowledge Assistant</h1>
        <FileUpload />
        <ChatInterface />
      </div>
    </div>
  );
}
