import React, { useState } from "react";
import ForceGraph2D from "react-force-graph-2d";

interface GraphNode {
  id: string;
  label: string;
  type: string; // matches our backend entity types below
  confidence?: number;
  reference_count?: number;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  [key: string]: unknown;
}

interface GraphLink {
  source: string | GraphNode;
  target: string | GraphNode;
  kind?: string; // "conflict" | "contains"
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

interface GraphExplorerProps {
  graphData: GraphData;
  conflicts?: Conflict[];
}

// Matches our actual backend entity types (app/agents/entity_extraction_agent.py)
const typeColors: Record<string, string> = {
  document: "#2DD4BF",
  equipment_tag: "#F5A623",
  date: "#60A5FA",
  personnel: "#F472B6",
  standard_reference: "#A78BFA",
};

const GraphExplorer: React.FC<GraphExplorerProps> = ({ graphData, conflicts = [] }) => {
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
          <div className="mb-6">
            <h2 className="mb-2 text-lg font-semibold text-teal">{selected.label}</h2>
            <p className="mb-1 text-sm text-gray-400">
              <span className="font-medium">Type:</span> {selected.type}
            </p>
            {selected.confidence !== undefined && (
              <p className="mb-1 text-sm text-gray-400">
                <span className="font-medium">Confidence:</span>{" "}
                {(selected.confidence * 100).toFixed(0)}%
              </p>
            )}
            {selected.reference_count !== undefined && (
              <p className="mb-1 text-sm text-gray-400">
                Referenced in {selected.reference_count} document(s)
              </p>
            )}
            <p className="text-sm text-gray-400">
              <span className="font-medium">ID:</span> {selected.id}
            </p>
          </div>
        )}
        {!selected && (
          <p className="mb-6 text-sm text-gray-500">Select a node to see details</p>
        )}

        <h2 className="mb-2 text-lg font-semibold text-red-400">
          Conflicts Detected ({conflicts.length})
        </h2>
        {conflicts.length === 0 && <p className="text-sm text-gray-500">None found yet.</p>}
        {conflicts.map((c, i) => (
          <div key={i} className="mb-2 rounded bg-graphite p-2 text-xs text-gray-300">
            <strong>{c.value}</strong> tagged as both{" "}
            <span className="text-amber">{c.type_a}</span> and{" "}
            <span className="text-amber">{c.type_b}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default GraphExplorer;
