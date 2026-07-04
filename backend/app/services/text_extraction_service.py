import pdfplumber
 
 
def is_pdf_text_based(pdf_path: str) -> bool:
    """Heuristic: if page 1 has extractable text, treat the PDF as digital, not scanned."""
    with pdfplumber.open(pdf_path) as pdf:
        if not pdf.pages:
            return False
        first_page_text = pdf.pages[0].extract_text()
        return bool(first_page_text and len(first_page_text.strip()) > 20)
 
 
def extract_text_from_digital_pdf(pdf_path: str) -> str:
    text_chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return "\n".join(text_chunks)
