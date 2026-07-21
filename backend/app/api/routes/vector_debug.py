from fastapi import APIRouter
 
from app.core.config import settings
from app.db.vector_store import collection
 
router = APIRouter()
 
if settings.environment != "production":
 
    @router.get("/vector-search")
    def vector_search(q: str, k: int = 5):
        """Debug-only endpoint — not registered at all in production."""
        results = collection.query(query_texts=[q], n_results=k)
        return {
            "query": q,
            "matches": [
                {"text": doc, "metadata": meta, "distance": dist}
                for doc, meta, dist in zip(
                    results["documents"][0], results["metadatas"][0], results["distances"][0]
                )
            ],
        }
