"""
Orchestrator Agent
-------------------
Inputs:   User query OR new-document ingestion event
Outputs:  Routed task result merged into a final cited response
Memory:   Session context (short-term). Long-term memory lives in the
          Knowledge Graph Agent (Neo4j) and Copilot Agent (Vector DB).
Talks to: All agents below.
"""
 
 
class OrchestratorAgent:
    def __init__(self):
        # TODO: wire up LangGraph state machine (routing agent)
        pass
 
    def route(self, event: dict) -> dict:
        """Route an incoming event to the correct agent(s)."""
        raise NotImplementedError("Implement during agent orchestration phase")
