import { useCallback, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import { uploadDocument, listDocuments } from "../services/api";
 
interface FileStatus {
  name: string;
  status: "uploading" | "done" | "error";
  confidence?: number;
}
 
interface DocRecord {
  id: string;
  filename: string;
  doc_type: string;
  status: string;
  uploaded_at: string;
  entity_count: number;
}
 
export default function Upload() {
  const [files, setFiles] = useState<FileStatus[]>([]);
  const [documents, setDocuments] = useState<DocRecord[]>([]);
 
  const refreshDocuments = () => {
    listDocuments().then((res) => setDocuments(res.data)).catch(() => {});
  };
 
  useEffect(() => {
    refreshDocuments();
  }, []);
 
  const onDrop = useCallback((acceptedFiles: File[]) => {
    acceptedFiles.forEach(async (file) => {
      setFiles((prev) => [...prev, { name: file.name, status: "uploading" }]);
      try {
        const res = await uploadDocument(file);
        setFiles((prev) =>
          prev.map((f) =>
            f.name === file.name
              ? { ...f, status: "done", confidence: res.data.extracted_confidence }
              : f
          )
        );
        refreshDocuments();
      } catch {
        setFiles((prev) => prev.map((f) => (f.name === file.name ? { ...f, status: "error" } : f)));
      }
    });
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
          <div key={i} className="rounded bg-graphite p-3">
            <div className="flex justify-between">
              <span className="text-gray-200">{f.name}</span>
              <span
                className={`text-sm ${
                  f.status === "done" ? "text-teal" : f.status === "error" ? "text-red-400" : "text-amber"
                }`}
              >
                {f.status}
              </span>
            </div>
            {f.confidence !== undefined && (
              <p className="mt-1 text-xs text-gray-400">
                Confidence: {(f.confidence * 100).toFixed(0)}%
              </p>
            )}
          </div>
        ))}
      </div>
 
      <h2 className="mb-3 mt-10 text-xl font-semibold text-teal">Ingested Documents</h2>
      <table className="w-full text-left text-sm text-gray-300">
        <thead>
          <tr className="border-b border-gray-700 text-gray-400">
            <th className="py-2">Filename</th>
            <th>Type</th>
            <th>Status</th>
            <th>Entities</th>
            <th>Uploaded</th>
          </tr>
        </thead>
        <tbody>
          {documents.map((d) => (
            <tr key={d.id} className="border-b border-gray-800">
              <td className="py-2">{d.filename}</td>
              <td>{d.doc_type}</td>
              <td>{d.status}</td>
              <td className="text-teal">{d.entity_count}</td> 
              <td>{new Date(d.uploaded_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
