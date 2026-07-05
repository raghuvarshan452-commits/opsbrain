from datetime import datetime
 
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
 
from app.db.postgres import get_db
from app.models.orm_models import Document, Entity, AuditLog
from app.services.storage_service import save_upload
from app.agents.ingestion_agent import IngestionAgent
from app.agents.entity_extraction_agent import EntityExtractionAgent
from app.agents.knowledge_graph_agent import KnowledgeGraphAgent
 
router = APIRouter()
ingestion_agent = IngestionAgent()
entity_agent = EntityExtractionAgent()
kg_agent = KnowledgeGraphAgent()
 
 
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
 
    entities = entity_agent.extract(result["text"])
    for ent in entities:
        db.add(
            Entity(
                document_id=doc.id,
                entity_type=ent.get("entity_type"),
                value=ent.get("value"),
                confidence=ent.get("confidence", 0.0),
            )
        )
    db.commit()
    db.add(AuditLog(document_id=doc.id, action="entities_extracted", agent_name="entity_extraction_agent"))
    db.commit()
 
    kg_agent.merge(str(doc.id), doc.filename, entities)
    db.add(AuditLog(document_id=doc.id, action="graph_updated", agent_name="knowledge_graph_agent"))
    db.commit()
 
    doc.status = "processed"
    db.commit()
 
    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "extracted_confidence": result["confidence"],
        "preview": result["text"][:300],
        "entity_count": len(entities),
    }
 
 
@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    output = []
    for d in docs:
        entity_count = db.query(func.count(Entity.id)).filter(Entity.document_id == d.id).scalar()
        output.append(
            {
                "id": d.id,
                "filename": d.filename,
                "doc_type": d.doc_type,
                "status": d.status,
                "uploaded_at": d.uploaded_at,
                "entity_count": entity_count,
            }
        )
    return output
