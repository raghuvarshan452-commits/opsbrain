from fastapi import APIRouter
 
from app.db.neo4j_client import neo4j_client

from app.agents.knowledge_graph_agent import KnowledgeGraphAgent

kg_agent = KnowledgeGraphAgent()
 
router = APIRouter()
 
 
@router.get("/graph")
def get_graph():
    records = neo4j_client.run_query(
        """
        MATCH (d:Document)-[r:CONTAINS]->(e:Entity)
        RETURN d.id AS doc_id, d.filename AS doc_name, e.value AS entity_value,
               e.entity_type AS entity_type, e.confidence AS confidence
        """
    )
 
    nodes = {}
    links = []
 
    for rec in records:
        doc_key = f"doc-{rec['doc_id']}"
        entity_key = f"entity-{rec['entity_value']}-{rec['entity_type']}"
 
        nodes[doc_key] = {"id": doc_key, "label": rec["doc_name"], "type": "document"}
        nodes[entity_key] = {
            "id": entity_key,
            "label": rec["entity_value"],
            "type": rec["entity_type"],
            "confidence": rec["confidence"],
        }
        links.append({"source": doc_key, "target": entity_key})
 
    conflict_records = neo4j_client.run_query(
        """
        MATCH (a:Document)-[r:CONFLICTS_WITH]->(b:Document)
        RETURN a.id AS doc_a, b.id AS doc_b, r.reason AS reason
        """
    )
    for rec in conflict_records:
        links.append(
            {
                "source": f"doc-{rec['doc_a']}",
                "target": f"doc-{rec['doc_b']}",
                "kind": "conflict",
                "reason": rec["reason"],
            }
        )
 
    return {"nodes": list(nodes.values()), "links": links}

 
 
@router.get("/graph/conflicts")
def get_conflicts():
    records = neo4j_client.run_query(
        """
        MATCH (a:Entity)-[:CONFLICTS_WITH]->(b:Entity)
        RETURN a.value AS value, a.entity_type AS type_a, b.entity_type AS type_b
        """
    )
    return [dict(r) for r in records]

@router.post("/graph/detect-contradictions")
def detect_contradictions():
    return kg_agent.detect_contradictions()
