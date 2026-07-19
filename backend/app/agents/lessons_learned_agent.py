"""
Lessons-Learned Agent
------------------------
Inputs:   None directly — scans current graph + incident state on each call
Outputs:  List of proactive alerts: equipment referenced across multiple
          documents AND with a recorded history of incidents
Memory:   Reads Neo4j (cross-referenced entities) + Postgres (incident history)
Talks to: Orchestrator (surfaces alerts to the Notifications UI)
"""
from app.agents.knowledge_graph_agent import KnowledgeGraphAgent
from app.db.postgres import SessionLocal
from app.models.orm_models import Equipment, Incident
 
kg_agent = KnowledgeGraphAgent()
 
 
class LessonsLearnedAgent:
    @staticmethod
    def _normalize(value: str) -> str:
        return value.strip().upper().replace(" ", "")
 
    def scan_for_patterns(self) -> list[dict]:
        cross_referenced = kg_agent.get_cross_referenced_entities()
        equipment_entities = [e for e in cross_referenced if e["entity_type"] == "equipment_tag"]
 
        if not equipment_entities:
            return []
 
        db = SessionLocal()
        all_equipment = db.query(Equipment).all()
        alerts = []
 
        for entity in equipment_entities:
            normalized_entity_value = self._normalize(entity["value"])
            equipment = next(
                (eq for eq in all_equipment if self._normalize(eq.tag_number) == normalized_entity_value),
                None,
            )
            if not equipment:
                continue
 
            incident_count = db.query(Incident).filter(Incident.equipment_id == equipment.id).count()
            if incident_count > 0:
                alerts.append(
                    {
                        "equipment_tag": equipment.tag_number,
                        "document_reference_count": entity["reference_count"],
                        "incident_count": incident_count,
                        "message": (
                            f"Equipment {equipment.tag_number} appears in "
                            f"{entity['reference_count']} ingested documents and has "
                            f"{incident_count} recorded incident(s) — recommend proactive "
                            f"inspection before next shift changeover."
                        ),
                    }
                )
 
        db.close()
        return alerts
