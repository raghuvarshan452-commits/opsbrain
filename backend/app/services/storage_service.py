import uuid
from pathlib import Path
 
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
 
 
def save_upload(file_bytes: bytes, original_filename: str) -> str:
    """Save raw uploaded bytes to local disk and return the stored path.
    TODO (later phase): swap this for Supabase Storage / S3 once deployed."""
    ext = Path(original_filename).suffix
    stored_name = f"{uuid.uuid4()}{ext}"
    stored_path = UPLOAD_DIR / stored_name
    with open(stored_path, "wb") as f:
        f.write(file_bytes)
    return str(stored_path)
