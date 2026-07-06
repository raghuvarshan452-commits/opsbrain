from fastapi import APIRouter
 
from app.db.neo4j_client import neo4j_client
 
router = APIRouter()
 
 
@router.get("/graph")
def get_graph():
    contains_records = neo4j_client.run_query(
        """
        MATCH (d:Document)-[:CONTAINS]->(e:Entity)
        RETURN d.id AS doc_id, d.filename AS doc_name, e.value AS entity_value,
               e.entity_type AS entity_type, e.confidence AS confidence,
               e.reference_count AS reference_count
        """
    )
    conflict_records = neo4j_client.run_query(
        """
        MATCH (a:Entity)-[:CONFLICTS_WITH]->(b:Entity)
        RETURN a.value AS value_a, a.entity_type AS type_a,
               b.value AS value_b, b.entity_type AS type_b
        """
    )
 
    nodes = {}
    links = []
 
    for rec in contains_records:
        doc_key = f"doc-{rec['doc_id']}"
        entity_key = f"entity-{rec['entity_value']}-{rec['entity_type']}"
        nodes[doc_key] = {"id": doc_key, "label": rec["doc_name"], "type": "document"}
        nodes[entity_key] = {
            "id": entity_key,
            "label": rec["entity_value"],
            "type": rec["entity_type"],
            "confidence": rec["confidence"],
            "reference_count": rec["reference_count"],
        }
        links.append({"source": doc_key, "target": entity_key, "kind": "contains"})
 
    for rec in conflict_records:
        a_key = f"entity-{rec['value_a']}-{rec['type_a']}"
        b_key = f"entity-{rec['value_b']}-{rec['type_b']}"
        links.append({"source": a_key, "target": b_key, "kind": "conflict"})
 
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
