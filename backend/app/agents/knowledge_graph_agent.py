"""
Knowledge Graph Agent (v1)
-----------------------------
Inputs:   Document metadata + extracted entities
Outputs:  New nodes/relationships written to Neo4j
Memory:   Persistent (Neo4j = long-term memory)
Talks to: Expert Copilot Agent, RCA Agent, Compliance Agent (later phases)
 
Day 4 scope: MERGE-based node/relationship creation only.
Day 5 scope: duplicate detection + conflict flagging on top of this.
"""
from app.db.neo4j_client import neo4j_client
 
 
class KnowledgeGraphAgent:
    def merge(self, document_id: str, filename: str, entities: list[dict]) -> dict:
        neo4j_client.run_query(
            "MERGE (d:Document {id: $document_id}) SET d.filename = $filename",
            {"document_id": document_id, "filename": filename},
        )
 
        for entity in entities:
            neo4j_client.run_query(
                """
                MERGE (e:Entity {value: $value, entity_type: $entity_type})
                SET e.confidence = $confidence
                WITH e
                MATCH (d:Document {id: $document_id})
                MERGE (d)-[:CONTAINS]->(e)
                """,
                {
                    "value": entity.get("value"),
                    "entity_type": entity.get("entity_type"),
                    "confidence": entity.get("confidence", 0.0),
                    "document_id": document_id,
                },
            )
 
        return {"status": "merged", "entity_count": len(entities)}
