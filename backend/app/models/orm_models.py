import uuid
from datetime import datetime
 
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
 
from app.db.postgres import Base
 
 
def gen_uuid():
    return str(uuid.uuid4())
 
 
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, default="engineer")
    created_at = Column(DateTime, default=datetime.utcnow)
    documents = relationship("Document", back_populates="uploaded_by_user")
 
 
class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    uploaded_by = Column(UUID(as_uuid=False), ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    doc_type = Column(String)
    status = Column(String, default="uploaded")
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by_user = relationship("User", back_populates="documents")
 
 
class Entity(Base):
    __tablename__ = "entities"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    document_id = Column(UUID(as_uuid=False), ForeignKey("documents.id"))
    entity_type = Column(String)
    value = Column(String)
    confidence = Column(Float)
 
 
class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    tag_number = Column(String, unique=True)
    equipment_class = Column(String)
    location = Column(String)
 
 
class Incident(Base):
    __tablename__ = "incidents"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    equipment_id = Column(UUID(as_uuid=False), ForeignKey("equipment.id"))
    description = Column(Text)
    incident_date = Column(DateTime)
    severity = Column(String)
 
 
class RCAReport(Base):
    __tablename__ = "rca_reports"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    incident_id = Column(UUID(as_uuid=False), ForeignKey("incidents.id"))
    root_cause_hypothesis = Column(Text)
    confidence = Column(Float)
 
 
class Regulation(Base):
    __tablename__ = "regulations"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    clause_ref = Column(String)
    clause_text = Column(Text)
    standard = Column(String)
 
 
class ComplianceMapping(Base):
    __tablename__ = "compliance_mappings"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    document_id = Column(UUID(as_uuid=False), ForeignKey("documents.id"))
    regulation_id = Column(UUID(as_uuid=False), ForeignKey("regulations.id"))
    coverage_status = Column(String)
 
 
class Query(Base):
    __tablename__ = "queries"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"))
    query_text = Column(Text)
    asked_at = Column(DateTime, default=datetime.utcnow)
 
 
class Response(Base):
    __tablename__ = "responses"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    query_id = Column(UUID(as_uuid=False), ForeignKey("queries.id"))
    answer = Column(Text)
    confidence = Column(Float)
    cited_sources = Column(JSON)
 
 
class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    document_id = Column(UUID(as_uuid=False), ForeignKey("documents.id"), nullable=True)
    action = Column(String)
    agent_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
