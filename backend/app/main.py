from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from app.api.routes import health, db_health, documents
 
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
 
@app.get("/")
def root():
    return {"message": "OpsBrain API is running"}
