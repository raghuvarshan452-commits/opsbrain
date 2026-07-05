from fastapi import APIRouter
 
from app.db.neo4j_client import neo4j_client
 
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
 
    return {"nodes": list(nodes.values()), "links": links}
