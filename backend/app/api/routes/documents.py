from datetime import datetime
 
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
 
from app.db.postgres import get_db
from app.models.orm_models import Document, AuditLog
from app.services.storage_service import save_upload
from app.agents.ingestion_agent import IngestionAgent
 
router = APIRouter()
ingestion_agent = IngestionAgent()
 
 
@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_bytes = await file.read()
    stored_path = save_upload(file_bytes, file.filename)
 
    doc = Document(
        filename=file.filename,
        doc_type=file.filename.split(".")[-1],
        status="processing",
        uploaded_at=datetime.utcnow(),
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    db.add(AuditLog(document_id=doc.id, action="uploaded", agent_name="ingestion_agent"))
    db.commit()
 
    result = ingestion_agent.ingest(stored_path, file.filename)
 
    doc.status = "processed"
    db.commit()
    db.add(AuditLog(document_id=doc.id, action="text_extracted", agent_name="ingestion_agent"))
    db.commit()
 
    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "extracted_confidence": result["confidence"],
        "preview": result["text"][:300],
    }
 
 
@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "doc_type": d.doc_type,
            "status": d.status,
            "uploaded_at": d.uploaded_at,
        }
        for d in docs
    ]
