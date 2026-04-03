from vectordb.chroma_store import get_or_create_collection
from embeddings.embedder import generate_embedding


def retrieve_chunks(query: str, top_k=10):
    collection = get_or_create_collection()

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = []

    for i in range(len(results["documents"][0])):
        chunks.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "score": results["distances"][0][i]
        })

    return chunks