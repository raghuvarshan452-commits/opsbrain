import { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { getGraphData } from "../services/api";
 
interface GraphNode {
  id: string;
  label: string;
  type: string;
  confidence?: number;
}
interface GraphLink {
  source: string;
  target: string;
}
 
const typeColors: Record<string, string> = {
  document: "#2DD4BF",
  equipment_tag: "#F5A623",
  date: "#60A5FA",
  personnel: "#F472B6",
  standard_reference: "#A78BFA",
};
 
export default function GraphExplorer() {
  const [graphData, setGraphData] = useState<{ nodes: GraphNode[]; links: GraphLink[] }>({
    nodes: [],
    links: [],
  });
  const [selected, setSelected] = useState<GraphNode | null>(null);
 
  useEffect(() => {
    getGraphData().then((res) => setGraphData(res.data)).catch(() => {});
  }, []);
 
  return (
    <div className="flex h-full">
      <div className="flex-1 p-4">
        <h1 className="mb-4 text-3xl font-bold text-amber">Knowledge Graph Explorer</h1>
        <div className="h-[600px] rounded-xl bg-graphite">
          <ForceGraph2D
            graphData={graphData}
            nodeLabel="label"
            nodeColor={(node: any) => typeColors[node.type] || "#999"}
            onNodeClick={(node: any) => setSelected(node)}
            backgroundColor="#1E2A38"
          />
        </div>
      </div>
      {selected && (
        <div className="w-72 border-l border-gray-700 p-4">
          <h2 className="mb-2 text-lg font-semibold text-teal">{selected.label}</h2>
          <p className="text-sm text-gray-400">Type: {selected.type}</p>
          {selected.confidence !== undefined && (
            <p className="text-sm text-gray-400">
              Confidence: {(selected.confidence * 100).toFixed(0)}%
            </p>
          )}
        </div>
      )}
    </div>
  );
}
