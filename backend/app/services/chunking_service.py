def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    """Character-based chunking with overlap — simple and fast, good enough
    for hackathon-speed RAG. Token-aware chunking is a later refinement."""
    if not text:
        return []
 
    chunks = []
    start = 0
    text_length = len(text)
 
    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
 
    return [c.strip() for c in chunks if c.strip()]
