from embeddings.chunker import chunk_documents
from embeddings.embedder import embed_documents


def process_documents(documents):
    print("[INFO] Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"[INFO] Created {len(chunks)} chunks")

    print("[INFO] Generating embeddings...")
    embedded_docs = embed_documents(chunks)
    print(f"[INFO] Generated {len(embedded_docs)} embeddings")

    return embedded_docs