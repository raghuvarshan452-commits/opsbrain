"""
OCR Agent
---------
Inputs:   Scanned image or scanned-PDF file path
Outputs:  Extracted text + average confidence score (0-1)
Memory:   None
Talks to: Document Ingestion Agent
"""
from app.services.ocr_service import extract_text_from_image, extract_text_from_scanned_pdf
 
 
class OCRAgent:
    def extract_text(self, file_path: str, file_type: str) -> dict:
        if file_type == "pdf":
            return extract_text_from_scanned_pdf(file_path)
        return extract_text_from_image(file_path)
