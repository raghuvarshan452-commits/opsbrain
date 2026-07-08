from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
 
from app.db.postgres import get_db
from app.models.orm_models import Query, Response, AuditLog
from app.agents.orchestrator import OrchestratorAgent
 
router = APIRouter()
orchestrator = OrchestratorAgent()
 
 
class QueryRequest(BaseModel):
    question: str
 
 
@router.post("/copilot/query")
def ask_copilot(request: QueryRequest, db: Session = Depends(get_db)):
    routed = orchestrator.route({"type": "query", "question": request.question})
    result = routed["result"]
    trace = routed["trace"]
 
    query_record = Query(query_text=request.question)
    db.add(query_record)
    db.commit()
    db.refresh(query_record)
 
    response_record = Response(
        query_id=query_record.id,
        answer=result["answer"],
        confidence=result["confidence"],
        cited_sources=result["citations"],
    )
    db.add(response_record)
    db.commit()
 
    db.add(AuditLog(action="query_answered", agent_name="orchestrator"))
    db.commit()
 
    return {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "citations": result["citations"],
        "trace": trace,
    }
