"""
OCR Agent
---------
Inputs:   Scanned / image pages
Outputs:  Extracted text + bounding-box confidence scores
Memory:   None
Talks to: Document Ingestion Agent
"""
 
 
class OCRAgent:
    def extract_text(self, image_path: str) -> dict:
        """Run OCR model and flag low-confidence regions for review."""
        raise NotImplementedError("Implement during OCR integration phase")
