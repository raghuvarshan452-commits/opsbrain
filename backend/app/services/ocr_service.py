import pytesseract
from pdf2image import convert_from_path
from PIL import Image
 
 
def _average_confidence(data: dict) -> float:
    confidences = [int(c) for c in data["conf"] if c not in ("-1", "")]
    return (sum(confidences) / len(confidences) / 100) if confidences else 0.0
 
 
def extract_text_from_image(image_path: str) -> dict:
    image = Image.open(image_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    text = " ".join([w for w in data["text"] if w.strip()])
    return {"text": text, "confidence": _average_confidence(data)}
 
 
def extract_text_from_scanned_pdf(pdf_path: str) -> dict:
    pages = convert_from_path(pdf_path)
    full_text, all_confidences = [], []
    for page in pages:
        data = pytesseract.image_to_data(page, output_type=pytesseract.Output.DICT)
        full_text.append(" ".join([w for w in data["text"] if w.strip()]))
        all_confidences.append(_average_confidence(data))
    avg = sum(all_confidences) / len(all_confidences) if all_confidences else 0.0
    return {"text": "\n".join(full_text), "confidence": avg}
