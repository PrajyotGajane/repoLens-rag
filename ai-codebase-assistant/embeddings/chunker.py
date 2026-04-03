def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and less than chunk_size")

    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == length:
            break
        start = end - overlap

    return chunks


def chunk_documents(documents):
    chunked_docs = []

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for i, chunk in enumerate(chunks):
            chunked_docs.append({
                "content": chunk,
                "metadata": {
                    "file": doc["file"],
                    "language": doc["language"],
                    "chunk_id": i
                }
            })

    return chunked_docs