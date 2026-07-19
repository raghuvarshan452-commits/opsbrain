import { useEffect, useState } from "react";
import { listDocuments, checkCompliance } from "../services/api";
 
interface DocRecord {
  id: string;
  filename: string;
}
 
interface ClauseResult {
  clause_ref: string;
  standard: string;
  coverage_status: "covered" | "partial" | "missing";
}
 
const statusColor: Record<string, string> = {
  covered: "bg-emerald-500",
  partial: "bg-amber",
  missing: "bg-red-500",
};
 
export default function Compliance() {
  const [documents, setDocuments] = useState<DocRecord[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<string>("");
  const [report, setReport] = useState<ClauseResult[]>([]);
  const [summary, setSummary] = useState<{ covered: number; partial: number; missing: number } | null>(null);
  const [loading, setLoading] = useState(false);
 
  useEffect(() => {
    listDocuments().then((res) => setDocuments(res.data)).catch(() => {});
  }, []);
 
  const runCheck = async () => {
    if (!selectedDoc) return;
    setLoading(true);
    const res = await checkCompliance(selectedDoc);
    setReport(res.data.clauses);
    setSummary(res.data.summary);
    setLoading(false);
  };
 
  return (
    <div className="p-8">
      <h1 className="mb-6 text-3xl font-bold text-amber">Compliance Dashboard</h1>
 
      <div className="mb-6 flex gap-3">
        <select
          className="rounded bg-graphite p-2 text-white"
          value={selectedDoc}
          onChange={(e) => setSelectedDoc(e.target.value)}
        >
          <option value="">Select a document...</option>
          {documents.map((d) => (
            <option key={d.id} value={d.id}>
              {d.filename}
            </option>
          ))}
        </select>
        <button onClick={runCheck} className="rounded bg-amber px-6 font-semibold text-navy">
          Run Compliance Check
        </button>
      </div>
 
      {loading && <p className="text-gray-400">Checking against regulation corpus...</p>}
 
      {summary && (
        <div className="mb-6 flex gap-4">
          <div className="rounded-xl bg-graphite p-4">
            <p className="text-sm text-gray-400">Covered</p>
            <p className="text-2xl font-bold text-emerald-400">{summary.covered}</p>
          </div>
          <div className="rounded-xl bg-graphite p-4">
            <p className="text-sm text-gray-400">Partial</p>
            <p className="text-2xl font-bold text-amber">{summary.partial}</p>
          </div>
          <div className="rounded-xl bg-graphite p-4">
            <p className="text-sm text-gray-400">Missing</p>
            <p className="text-2xl font-bold text-red-400">{summary.missing}</p>
          </div>
        </div>
      )}
 
      <div className="space-y-2">
        {report.map((clause, i) => (
          <div key={i} className="flex items-center justify-between rounded bg-graphite p-3">
            <div>
              <p className="text-gray-200">{clause.clause_ref}</p>
              <p className="text-xs text-gray-500">{clause.standard}</p>
            </div>
            <span
              className={`rounded px-3 py-1 text-xs font-semibold text-navy ${statusColor[clause.coverage_status]}`}
            >
              {clause.coverage_status.toUpperCase()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
