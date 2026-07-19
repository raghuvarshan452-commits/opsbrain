from fastapi import APIRouter
 
from app.services.analytics_service import get_analytics_summary
from app.db.postgres import SessionLocal
from app.models.orm_models import AuditLog
from app.services.roi_service import calculate_roi
 
router = APIRouter()
 
 
@router.get("/analytics/summary")
def analytics_summary():
    return get_analytics_summary()

 
 
@router.get("/audit-log")
def get_audit_log(limit: int = 50):
    db = SessionLocal()
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
    db.close()
    return [
        {
            "id": log.id,
            "document_id": log.document_id,
            "action": log.action,
            "agent_name": log.agent_name,
            "created_at": log.created_at,
        }
        for log in logs
    ]

@router.get("/analytics/roi")
def analytics_roi():
    return calculate_roi()

