import { useEffect, useState } from "react";
import GraphExplorer from "../components/graph/GraphExplorer";
import { getGraphData, detectContradictions } from "../services/api";
 
interface GraphData {
  nodes: any[];
  links: any[];
}
 
export default function GraphExplorerPage() {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [scanning, setScanning] = useState(false);
 
  const refresh = () => {
    getGraphData().then((res) => setGraphData(res.data)).catch(() => {});
  };
 
  useEffect(() => {
    refresh();
  }, []);
 
  const runScan = async () => {
    setScanning(true);
    await detectContradictions();
    refresh();
    setScanning(false);
  };
 
  return (
    <div className="flex h-full flex-col p-8">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-amber">Knowledge Graph Explorer</h1>
        <button
          onClick={runScan}
          disabled={scanning}
          className="rounded bg-amber px-4 py-2 text-sm font-semibold text-navy disabled:opacity-50"
        >
          {scanning ? "Scanning..." : "Scan for Contradictions"}
        </button>
      </div>
      <div className="h-[600px] overflow-hidden rounded-xl bg-graphite">
        <GraphExplorer graphData={graphData} />
      </div>
    </div>
  );
}
