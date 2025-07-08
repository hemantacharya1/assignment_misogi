import FileUpload from "../components/FileUpload";

export default function UploadPage() {
  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-semibold mb-4">Upload a Lecture Video</h2>
      <FileUpload />
    </div>
  );
}
