"""
Compliance Agent
-------------------
Inputs:   document_id — checks that document's embedded chunks against
          every known regulation clause
Outputs:  Coverage report: list of {clause_ref, standard, coverage_status}
Memory:   Reads regulation clauses from Postgres, document chunks from ChromaDB
Talks to: Orchestrator, Knowledge Graph Agent (future integration)
"""
from app.db.postgres import SessionLocal
from app.db.vector_store import _collection as collection
from app.models.orm_models import Regulation, ComplianceMapping
 
COVERED_THRESHOLD = 1.2
PARTIAL_THRESHOLD = 1.5

 
class ComplianceAgent:
    def check_coverage(self, document_id: str) -> list[dict]:
        db = SessionLocal()
        regulations = db.query(Regulation).all()
        report = []
 
        for reg in regulations:
            results = collection.query(
                query_texts=[reg.clause_text],
                n_results=1,
                where={"document_id": document_id},
            )
 
            if not results["documents"][0]:
                status = "missing"
                print(f"{reg.clause_ref}: NO MATCH FOUND")
            else:
                distance = results["distances"][0][0]
                print(f"{reg.clause_ref}: distance={distance}")
                if distance < COVERED_THRESHOLD:
                    status = "covered"
                elif distance < PARTIAL_THRESHOLD:
                    status = "partial"
                else:
                    status = "missing"
 
            db.add(
                ComplianceMapping(
                    document_id=document_id,
                    regulation_id=reg.id,
                    coverage_status=status,
                )
            )
            report.append(
                {"clause_ref": reg.clause_ref, "standard": reg.standard, "coverage_status": status}
            )
 
        db.commit()
        db.close()
        return report
