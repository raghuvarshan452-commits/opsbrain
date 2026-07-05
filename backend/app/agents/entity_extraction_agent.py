"""
Entity Extraction Agent
------------------------
Inputs:   Cleaned document text
Outputs:  Structured entities: equipment tags, dates, personnel, standards
Memory:   None
Talks to: Knowledge Graph Agent
"""
from app.services.llm_service import extract_entities
 
 
class EntityExtractionAgent:
    def extract(self, text: str) -> list[dict]:
        if not text or not text.strip():
            return []
        return extract_entities(text)
