from fastapi import APIRouter
 
from app.agents.compliance_agent import ComplianceAgent
 
router = APIRouter()
compliance_agent = ComplianceAgent()
 
 
@router.post("/compliance/check/{document_id}")
def check_compliance(document_id: str):
    report = compliance_agent.check_coverage(document_id)
    covered = sum(1 for r in report if r["coverage_status"] == "covered")
    partial = sum(1 for r in report if r["coverage_status"] == "partial")
    missing = sum(1 for r in report if r["coverage_status"] == "missing")
    return {
        "document_id": document_id,
        "summary": {"covered": covered, "partial": partial, "missing": missing},
        "clauses": report,
    }
