import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { getAnalyticsSummary, getAuditLog } from "../services/api";
 
interface Summary {
  total_documents: number;
  total_queries: number;
  total_entities: number;
  avg_confidence: number;
  agent_activity: { agent: string; count: number }[];
  query_volume: { date: string; count: number }[];
}
 
interface AuditEntry {
  id: string;
  action: string;
  agent_name: string;
  created_at: string;
}
 
export default function Analytics() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [auditLog, setAuditLog] = useState<AuditEntry[]>([]);
 
  useEffect(() => {
    getAnalyticsSummary().then((res) => setSummary(res.data)).catch(() => {});
    getAuditLog().then((res) => setAuditLog(res.data)).catch(() => {});
  }, []);
 
  return (
    <div className="p-8">
      <h1 className="mb-6 text-3xl font-bold text-amber">Analytics</h1>
 
      {summary && (
        <>
          <div className="mb-8 grid grid-cols-2 gap-4 md:grid-cols-4">
            <div className="rounded-xl bg-graphite p-4">
              <p className="text-sm text-gray-400">Documents</p>
              <p className="text-2xl font-bold text-teal">{summary.total_documents}</p>
            </div>
            <div className="rounded-xl bg-graphite p-4">
              <p className="text-sm text-gray-400">Queries Answered</p>
              <p className="text-2xl font-bold text-teal">{summary.total_queries}</p>
            </div>
            <div className="rounded-xl bg-graphite p-4">
              <p className="text-sm text-gray-400">Entities Extracted</p>
              <p className="text-2xl font-bold text-teal">{summary.total_entities}</p>
            </div>
            <div className="rounded-xl bg-graphite p-4">
              <p className="text-sm text-gray-400">Avg. Answer Confidence</p>
              <p className="text-2xl font-bold text-teal">{(summary.avg_confidence * 100).toFixed(0)}%</p>
            </div>
          </div>
 
          <div className="mb-8 grid grid-cols-1 gap-6 md:grid-cols-2">
            <div className="rounded-xl bg-graphite p-4">
              <h2 className="mb-3 text-lg font-semibold text-gray-200">Query Volume Over Time</h2>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={summary.query_volume}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="date" stroke="#9CA3AF" fontSize={12} />
                  <YAxis stroke="#9CA3AF" fontSize={12} allowDecimals={false} />
                  <Tooltip contentStyle={{ backgroundColor: "#1E2A38", border: "none" }} />
                  <Line type="monotone" dataKey="count" stroke="#2DD4BF" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
 
            <div className="rounded-xl bg-graphite p-4">
              <h2 className="mb-3 text-lg font-semibold text-gray-200">Agent Activity Breakdown</h2>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={summary.agent_activity}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="agent" stroke="#9CA3AF" fontSize={10} angle={-20} textAnchor="end" height={60} />
                  <YAxis stroke="#9CA3AF" fontSize={12} allowDecimals={false} />
                  <Tooltip contentStyle={{ backgroundColor: "#1E2A38", border: "none" }} />
                  <Bar dataKey="count" fill="#F5A623" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
 
      <h2 className="mb-3 text-lg font-semibold text-gray-200">Recent Audit Trail</h2>
      <div className="space-y-1">
        {auditLog.map((entry) => (
          <div key={entry.id} className="flex justify-between rounded bg-graphite px-3 py-2 text-sm">
            <span className="text-gray-300">
              {entry.agent_name || "system"} → {entry.action}
            </span>
            <span className="text-gray-500">{new Date(entry.created_at).toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

