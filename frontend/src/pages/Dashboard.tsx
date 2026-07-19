import { useEffect, useState } from "react";
import KPICard from "../components/dashboard/KPICard";
import { checkDbHealth } from "../services/api";
import { getROI } from "../services/api";  

export default function Dashboard() {
  const [systemStatus, setSystemStatus] = useState("checking...");
  const [roiHours, setRoiHours] = useState("0.0");
  useEffect(() => {
    checkDbHealth()
      .then((res) => {
        const { postgres, neo4j } = res.data;
        setSystemStatus(postgres === "connected" && neo4j === "connected" ? "All systems operational" : "Degraded");
      })
      .catch(() => setSystemStatus("Backend unreachable"));
 
    getROI()
      .then((res) => setRoiHours(res.data.hours_saved.toFixed(1)))
      .catch(() => {});
  }, []);
  return (
    <div className="p-8">
      <h1 className="mb-2 text-3xl font-bold text-amber">Dashboard</h1>
      <p className="mb-6 text-sm text-gray-400">{systemStatus}</p>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <KPICard label="Documents Ingested" value={0} />
        <KPICard label="Open Compliance Gaps" value={0} accent="amber" />
        <KPICard label="Active Alerts" value={0} accent="amber" />
        <KPICard label="Hours Saved (est.)" value={roiHours} />
      </div>
      {/* TODO Day 3+: recent activity feed, quick-ask Copilot bar */}
    </div>
  );
}
