"""
Entity Extraction Agent
------------------------
Inputs:   Cleaned document text
Outputs:  Structured entities (equipment tags, dates, personnel, standards)
Memory:   None
Talks to: Knowledge Graph Agent
"""
 
 
class EntityExtractionAgent:
    def extract(self, text: str) -> list[dict]:
        """NER + LLM-based structured extraction, validated against taxonomy."""
        raise NotImplementedError("Implement during entity extraction phase")
