"""
Document Ingestion Agent
-------------------------
Inputs:   Raw file path + original filename
Outputs:  {text, confidence, doc_type}
Memory:   None (stateless per file)
Talks to: OCR Agent
"""
from pathlib import Path
 
from app.agents.ocr_agent import OCRAgent
from app.services.text_extraction_service import (
    is_pdf_text_based,
    extract_text_from_digital_pdf,
)
 
 
class IngestionAgent:
    def __init__(self):
        self.ocr_agent = OCRAgent()
 
    def ingest(self, file_path: str, original_filename: str) -> dict:
        ext = Path(original_filename).suffix.lower()
 
        if ext == ".pdf":
            if is_pdf_text_based(file_path):
                text, confidence = extract_text_from_digital_pdf(file_path), 1.0
            else:
                result = self.ocr_agent.extract_text(file_path, "pdf")
                text, confidence = result["text"], result["confidence"]
        elif ext in (".png", ".jpg", ".jpeg"):
            result = self.ocr_agent.extract_text(file_path, "image")
            text, confidence = result["text"], result["confidence"]
        else:
            with open(file_path, "r", errors="ignore") as f:
                text = f.read()
            confidence = 1.0
 
        return {"text": text, "confidence": confidence, "doc_type": ext.lstrip(".")}
