import { useEffect, useState } from "react";
import GraphExplorer from "../components/graph/GraphExplorer";
import { getGraphData } from "../services/api";
 
interface GraphData {
  nodes: any[];
  links: any[];
}
 
export default function GraphExplorerPage() {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
 
  useEffect(() => {
    getGraphData()
      .then((res) => setGraphData(res.data))
      .catch(() => {});
  }, []);
 
  return (
    <div className="flex h-full flex-col p-8">
      <h1 className="mb-4 text-3xl font-bold text-amber">Knowledge Graph Explorer</h1>
      <div className="h-[600px] overflow-hidden rounded-xl bg-graphite">
        <GraphExplorer graphData={graphData} />
      </div>
    </div>
  );
}
