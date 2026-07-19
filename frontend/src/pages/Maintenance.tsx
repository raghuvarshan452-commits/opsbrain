import { useState } from "react";
import { getRCA } from "../services/api";
 
interface Hypothesis {
  hypothesis: string;
  confidence: number;
  supporting_evidence: string;
}
 
export default function Maintenance() {
  const [tag, setTag] = useState("");
  const [hypotheses, setHypotheses] = useState<Hypothesis[]>([]);
  const [note, setNote] = useState("");
  const [loading, setLoading] = useState(false);
 
  const runAnalysis = async () => {
    if (!tag.trim()) return;
    setLoading(true);
    const res = await getRCA(tag.trim());
    setHypotheses(res.data.hypotheses || []);
    setNote(res.data.note || "");
    setLoading(false);
  };
 
  return (
    <div className="p-8">
      <h1 className="mb-6 text-3xl font-bold text-amber">Maintenance & RCA</h1>
 
      <div className="mb-6 flex gap-3">
        <input
          className="rounded bg-graphite p-2 text-white"
          placeholder="Equipment tag (e.g. P-204)"
          value={tag}
          onChange={(e) => setTag(e.target.value)}
        />
        <button onClick={runAnalysis} className="rounded bg-amber px-6 font-semibold text-navy">
          Run RCA
        </button>
      </div>
 
      {loading && <p className="text-gray-400">Analyzing incident history...</p>}
      {note && <p className="text-gray-400">{note}</p>}
 
      <div className="space-y-3">
        {hypotheses.map((h, i) => (
          <div key={i} className="rounded-xl bg-graphite p-4">
            <div className="flex justify-between">
              <p className="font-semibold text-gray-100">
                {i + 1}. {h.hypothesis}
              </p>
              <span className="text-teal">{(h.confidence * 100).toFixed(0)}%</span>
            </div>
            <p className="mt-1 text-sm text-gray-400">{h.supporting_evidence}</p>
          </div>
        ))}
      </div>
    </div>
  );
}