import { useState } from 'react';

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setStatus("Uploading...");

    try {
      const res = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setStatus(`Success! Chunks stored: ${data.chunks_stored}`);
    } catch (err) {
      setStatus("Upload failed.");
    }
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-lg font-semibold mb-2">Upload HR Document</h2>
      <input type="file" onChange={e => setFile(e.target.files[0])} className="mb-2" />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
      >
        Upload
      </button>
      <p className="mt-2 text-sm text-gray-600">{status}</p>
    </div>
  );
}
