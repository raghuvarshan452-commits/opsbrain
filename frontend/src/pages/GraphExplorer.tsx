import { useEffect, useState } from "react";
import GraphExplorer from "../components/graph/GraphExplorer";
import { getGraphData, getConflicts } from "../services/api";

interface GraphNode {
  id: string;
  label: string;
  type: string;
  confidence?: number;
  reference_count?: number;
  [key: string]: unknown;
}

interface GraphLink {
  source: string;
  target: string;
  kind?: string;
  [key: string]: unknown;
}

interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

interface Conflict {
  value: string;
  type_a: string;
  type_b: string;
}

export default function GraphExplorerPage() {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [conflicts, setConflicts] = useState<Conflict[]>([]);

  useEffect(() => {
    getGraphData()
      .then((res) => setGraphData(res.data))
      .catch(() => {});
    getConflicts()
      .then((res) => setConflicts(res.data))
      .catch(() => {});
  }, []);

  return (
    <div className="flex h-full flex-col p-8">
      <h1 className="mb-4 text-3xl font-bold text-amber">Knowledge Graph Explorer</h1>
      <div className="h-[600px] overflow-hidden rounded-xl bg-graphite">
        <GraphExplorer graphData={graphData} conflicts={conflicts} />
      </div>
    </div>
  );
}
