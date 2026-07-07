from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
 
from app.db.postgres import get_db
from app.models.orm_models import Query, Response, AuditLog
from app.agents.copilot_agent import CopilotAgent
 
router = APIRouter()
copilot_agent = CopilotAgent()
 
 
class QueryRequest(BaseModel):
    question: str
 
 
@router.post("/copilot/query")
def ask_copilot(request: QueryRequest, db: Session = Depends(get_db)):
    result = copilot_agent.answer(request.question)
 
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
 
    db.add(AuditLog(action="query_answered", agent_name="copilot_agent"))
    db.commit()
 
    return {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "citations": result["citations"],
    }
