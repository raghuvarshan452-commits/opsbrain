"""
Knowledge Graph Agent (v2 — Day 5)
--------------------------------------
Inputs:   Document metadata + extracted entities
Outputs:  Updated graph nodes/edges, plus CONFLICTS_WITH edges when the
          same entity value is seen under two different entity_types
Memory:   Persistent (Neo4j = long-term memory)
Talks to: Expert Copilot Agent, RCA Agent, Compliance Agent (later phases)
 
New in v2:
- reference_count on each Entity node (how many documents mention it)
- CONFLICTS_WITH relationship when a value is tagged inconsistently
  across documents
"""
from app.db.neo4j_client import neo4j_client
 
 
class KnowledgeGraphAgent:
    def merge(self, document_id: str, filename: str, entities: list[dict]) -> dict:
        neo4j_client.run_query(
            "MERGE (d:Document {id: $document_id}) SET d.filename = $filename",
            {"document_id": document_id, "filename": filename},
        )
 
        conflicts = []
 
        for entity in entities:
            value = entity.get("value")
            entity_type = entity.get("entity_type")
            confidence = entity.get("confidence", 0.0)
 
            existing = neo4j_client.run_query(
                "MATCH (e:Entity {value: $value}) WHERE e.entity_type <> $entity_type "
                "RETURN e.entity_type AS existing_type LIMIT 1",
                {"value": value, "entity_type": entity_type},
            )
            if existing:
                conflicts.append(
                    {
                        "value": value,
                        "new_type": entity_type,
                        "existing_type": existing[0]["existing_type"],
                    }
                )
 
            neo4j_client.run_query(
                """
                MERGE (e:Entity {value: $value, entity_type: $entity_type})
                ON CREATE SET e.confidence = $confidence, e.reference_count = 1
                ON MATCH SET e.reference_count = coalesce(e.reference_count, 1) + 1
                WITH e
                MATCH (d:Document {id: $document_id})
                MERGE (d)-[:CONTAINS]->(e)
                """,
                {
                    "value": value,
                    "entity_type": entity_type,
                    "confidence": confidence,
                    "document_id": document_id,
                },
            )
 
        for c in conflicts:
            neo4j_client.run_query(
                """
                MATCH (a:Entity {value: $value, entity_type: $new_type})
                MATCH (b:Entity {value: $value, entity_type: $existing_type})
                MERGE (a)-[:CONFLICTS_WITH]->(b)
                """,
                c,
            )
 
        return {"status": "merged", "entity_count": len(entities), "conflicts_found": len(conflicts)}
