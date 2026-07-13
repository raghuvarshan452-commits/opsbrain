import { useEffect, useState } from "react";
import { getAlerts } from "../services/api";
 
interface Alert {
  equipment_tag: string;
  document_reference_count: number;
  incident_count: number;
  message: string;
}
 
export default function Notifications() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [dismissed, setDismissed] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
 
  useEffect(() => {
    getAlerts()
      .then((res) => setAlerts(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);
 
  const dismiss = (index: number) => {
    setDismissed((prev) => new Set(prev).add(index));
  };
 
  const visibleAlerts = alerts.filter((_, i) => !dismissed.has(i));
 
  return (
    <div className="p-8">
      <h1 className="mb-6 text-3xl font-bold text-amber">Notifications</h1>
 
      {loading && <p className="text-gray-400">Scanning for patterns...</p>}
      {!loading && visibleAlerts.length === 0 && (
        <p className="text-gray-500">No active alerts. New patterns will appear here automatically.</p>
      )}
 
      <div className="space-y-3">
        {visibleAlerts.map((alert, i) => (
          <div key={i} className="rounded-xl border-l-4 border-amber bg-graphite p-4">
            <div className="flex items-start justify-between">
              <div>
                <p className="font-semibold text-gray-100">⚠ {alert.equipment_tag}</p>
                <p className="mt-1 text-sm text-gray-300">{alert.message}</p>
                <p className="mt-2 text-xs text-gray-500">
                  Referenced in {alert.document_reference_count} document(s) · {alert.incident_count} incident(s) on record
                </p>
              </div>
              <button
                onClick={() => dismiss(i)}
                className="ml-4 text-xs text-gray-400 underline hover:text-gray-200"
              >
                Dismiss
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
