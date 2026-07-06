import React, { useState } from "react";
import ForceGraph2D from "react-force-graph-2d";

interface GraphNode {
  id: string;
  label: string;
  type: string; // e.g. "component" | "service" | "database" — narrow this if you know the fixed set
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  [key: string]: unknown;
}

interface GraphLink {
  source: string | GraphNode;
  target: string | GraphNode;
  kind: string; // e.g. "conflict" | "dependency" | "reference"
  [key: string]: unknown;
}

interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

interface GraphExplorerProps {
  graphData: GraphData;
}

const typeColors: Record<string, string> = {
  component: "#60A5FA",
  service: "#34D399",
  database: "#FBBF24",
  // add more types as needed
};

const GraphExplorer: React.FC<GraphExplorerProps> = ({ graphData }) => {
  const [selected, setSelected] = useState<GraphNode | null>(null);

  return (
    <div className="flex h-full">
      <div className="flex-1">
        <ForceGraph2D
          graphData={graphData}
          nodeLabel="label"
          nodeColor={(node: GraphNode) => typeColors[node.type] || "#999"}
          linkColor={(link: GraphLink) =>
            link.kind === "conflict" ? "#F87171" : "#4B5563"
          }
          linkLineDash={(link: GraphLink) =>
            link.kind === "conflict" ? [4, 2] : null
          }
          onNodeClick={(node: GraphNode) => setSelected(node)}
          backgroundColor="#1E2A38"
        />
      </div>

      <div className="w-72 border-l border-gray-700 p-4">
        {selected && (
          <div>
            <h2 className="text-lg font-semibold mb-2">{selected.label}</h2>
            <p className="text-sm text-gray-400 mb-1">
              <span className="font-medium">Type:</span> {selected.type}
            </p>
            <p className="text-sm text-gray-400">
              <span className="font-medium">ID:</span> {selected.id}
            </p>
          </div>
        )}
        {!selected && (
          <p className="text-sm text-gray-500">Select a node to see details</p>
        )}
      </div>
    </div>
  );
};

export default GraphExplorer;