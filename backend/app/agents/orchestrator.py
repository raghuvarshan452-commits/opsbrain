from typing import TypedDict, Optional, List, Dict, Any
from langgraph.graph import StateGraph, END
from app.agents.copilot_agent import CopilotAgent
from app.agents.knowledge_graph_agent import KnowledgeGraphAgent

copilot_agent = CopilotAgent()
kg_agent = KnowledgeGraphAgent()

class OrchestratorState(TypedDict):
    event: Dict[str, Any]
    trace: List[Dict[str, str]]
    result: Optional[Dict[str, Any]]

def _route(state: OrchestratorState) -> str:
    return "handle_query" if state["event"]["type"] == "query" else "handle_ingest"

def _handle_query(state: OrchestratorState) -> OrchestratorState:
    question = state["event"]["question"]
    result = copilot_agent.answer(question)
    state["trace"].append({"agent": "copilot_agent", "action": "retrieved context and answered query"})
    state["result"] = result
    return state

def _handle_ingest(state: OrchestratorState) -> OrchestratorState:
    event = state["event"]
    result = kg_agent.merge(event["document_id"], event["filename"], event["entities"])
    state["trace"].append({"agent": "knowledge_graph_agent", "action": "merged entities into graph"})
    state["result"] = result
    return state

_graph = StateGraph(OrchestratorState)
_graph.add_node("handle_query", _handle_query)
_graph.add_node("handle_ingest", _handle_ingest)
_graph.set_conditional_entry_point(
    _route, {"handle_query": "handle_query", "handle_ingest": "handle_ingest"}
)
_graph.add_edge("handle_query", END)
_graph.add_edge("handle_ingest", END)
_compiled_graph = _graph.compile()

class OrchestratorAgent:
    def route(self, event: dict) -> dict:
        initial_state: OrchestratorState = {"event": event, "trace": [], "result": None}
        final_state = _compiled_graph.invoke(initial_state)
        return {"result": final_state["result"], "trace": final_state["trace"]}