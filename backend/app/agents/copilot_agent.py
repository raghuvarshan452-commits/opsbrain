"""
Expert Copilot Agent
----------------------
Inputs:   User natural-language query
Outputs:  Cited, confidence-scored answer
Memory:   Reads Vector DB + Knowledge Graph
Talks to: Orchestrator, Knowledge Graph Agent
"""
 
 
class CopilotAgent:
    def answer(self, query: str) -> dict:
        """Retrieve chunks (RAG), cross-reference the graph, generate a cited answer."""
        raise NotImplementedError("Implement during RAG pipeline phase")
