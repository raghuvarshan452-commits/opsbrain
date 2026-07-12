import chromadb
 
_client = chromadb.PersistentClient(path="./chroma_db")
_collection = _client.get_or_create_collection(name="documents")
 
 
def add_chunks(document_id: str, filename: str, chunks: list[str]):
    if not chunks:
        return
 
    ids = [f"{document_id}-{i}" for i in range(len(chunks))]
    metadatas = [
        {"document_id": document_id, "filename": filename, "chunk_index": i}
        for i in range(len(chunks))
    ]
    _collection.add(documents=chunks, metadatas=metadatas, ids=ids)
 
 
def query_chunks(query_text: str, top_k: int = 5) -> dict:
    return _collection.query(query_texts=[query_text], n_results=top_k)
