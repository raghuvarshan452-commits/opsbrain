from fastapi import APIRouter
 
from app.db.vector_store import query_chunks
 
router = APIRouter()
 
 
@router.get("/vector-search")
def vector_search(q: str):
    return query_chunks(q)
