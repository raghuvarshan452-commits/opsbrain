from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from app.api.routes import health, db_health, documents, graph, search, copilot, compliance, rca
 
app = FastAPI(title="OpsBrain API", version="0.1.0")
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(db_health.router, prefix="/api", tags=["health"])
app.include_router(documents.router, prefix="/api", tags=["documents"])
app.include_router(graph.router, prefix="/api", tags=["graph"])
app.include_router(search.router, prefix="/api", tags=["search"]) 
app.include_router(copilot.router, prefix="/api", tags=["copilot"])
app.include_router(compliance.router, prefix="/api", tags=["compliance"])
app.include_router(rca.router, prefix="/api", tags=["rca"])
 
@app.get("/")
def root():
    return {"message": "OpsBrain API is running"}
