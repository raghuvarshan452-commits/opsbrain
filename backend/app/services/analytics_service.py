from sqlalchemy import func
 
from app.db.postgres import SessionLocal
from app.models.orm_models import Document, Query, Response, Entity, AuditLog
 
 
def get_analytics_summary() -> dict:
    db = SessionLocal()
 
    total_documents = db.query(func.count(Document.id)).scalar()
    total_queries = db.query(func.count(Query.id)).scalar()
    total_entities = db.query(func.count(Entity.id)).scalar()
    avg_confidence = db.query(func.avg(Response.confidence)).scalar() or 0.0
 
    agent_activity = (
        db.query(AuditLog.agent_name, func.count(AuditLog.id))
        .filter(AuditLog.agent_name.isnot(None))
        .group_by(AuditLog.agent_name)
        .all()
    )
 
    query_volume = (
        db.query(func.date(Query.asked_at).label("day"), func.count(Query.id))
        .group_by(func.date(Query.asked_at))
        .order_by(func.date(Query.asked_at))
        .all()
    )
 
    db.close()
 
    return {
        "total_documents": total_documents,
        "total_queries": total_queries,
        "total_entities": total_entities,
        "avg_confidence": round(float(avg_confidence), 2),
        "agent_activity": [{"agent": a, "count": c} for a, c in agent_activity],
        "query_volume": [{"date": str(d), "count": c} for d, c in query_volume],
    }
