from sqlalchemy import func
 
from app.db.postgres import SessionLocal
from app.models.orm_models import Document, Query
 
MINUTES_SAVED_PER_QUERY = 12
MINUTES_SAVED_PER_DOCUMENT_INDEXED = 8
 
 
def calculate_roi() -> dict:
    db = SessionLocal()
    total_queries = db.query(func.count(Query.id)).scalar() or 0
    total_documents = db.query(func.count(Document.id)).scalar() or 0
    db.close()
 
    total_minutes_saved = (total_queries * MINUTES_SAVED_PER_QUERY) + (
        total_documents * MINUTES_SAVED_PER_DOCUMENT_INDEXED
    )
    hours_saved = round(total_minutes_saved / 60, 1)
 
    return {
        "hours_saved": hours_saved,
        "total_queries": total_queries,
        "total_documents": total_documents,
        "assumptions": {
            "minutes_saved_per_query": MINUTES_SAVED_PER_QUERY,
            "minutes_saved_per_document_indexed": MINUTES_SAVED_PER_DOCUMENT_INDEXED,
        },
    }
