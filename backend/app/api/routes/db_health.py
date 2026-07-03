from fastapi import APIRouter
from sqlalchemy import text
 
from app.db.postgres import SessionLocal
from app.db.neo4j_client import neo4j_client
 
router = APIRouter()
 
 
@router.get("/db-health")
def db_health_check():
    result = {"postgres": "unknown", "neo4j": "unknown"}
 
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        result["postgres"] = "connected"
    except Exception as e:
        result["postgres"] = f"error: {str(e)}"
 
    try:
        result["neo4j"] = "connected" if neo4j_client.verify_connection() else "unreachable"
    except Exception as e:
        result["neo4j"] = f"error: {str(e)}"
 
    return result
