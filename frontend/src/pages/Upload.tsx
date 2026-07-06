import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
 
interface FileStatus {
  name: string;
  status: "queued" | "uploading" | "done";
}
 
export default function Upload() {
  const [files, setFiles] = useState<FileStatus[]>([]);
 
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map((f) => ({ name: f.name, status: "queued" as const }));
    setFiles((prev) => [...prev, ...newFiles]);
    // TODO Day 4+: POST to /api/documents/upload, update status per file
  }, []);
 
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });
 
  return (
    <div className="p-8">
      <h1 className="mb-6 text-3xl font-bold text-amber">Upload Center</h1>
      <div
        {...getRootProps()}
        className={`rounded-xl border-2 border-dashed p-12 text-center ${
          isDragActive ? "border-teal bg-graphite" : "border-gray-600"
        }`}
      >
        <input {...getInputProps()} />
        <p className="text-gray-300">
          {isDragActive ? "Drop the files here..." : "Drag & drop documents here, or click to browse"}
        </p>
      </div>
      <div className="mt-6 space-y-2">
        {files.map((f, i) => (
          <div key={i} className="flex justify-between rounded bg-graphite p-3">
            <span className="text-gray-200">{f.name}</span>
            <span className="text-sm text-teal">{f.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
