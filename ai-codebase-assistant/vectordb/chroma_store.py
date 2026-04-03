import chromadb
from chromadb.config import Settings

CHROMA_DIR = "data/chroma"


def get_chroma_client():
    return chromadb.Client(
        Settings(
            persist_directory=CHROMA_DIR
        )
    )


def get_or_create_collection(collection_name="codebase"):
    client = get_chroma_client()

    return client.get_or_create_collection(
        name=collection_name
    )


def store_embeddings(embedded_docs, collection_name="codebase"):
    collection = get_or_create_collection(collection_name)

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for doc in embedded_docs:
        metadata = doc["metadata"]
        doc_id = f"{metadata['file']}_{metadata['chunk_id']}"

        ids.append(doc_id)
        documents.append(doc["content"])
        metadatas.append(metadata)
        embeddings.append(doc["embedding"])

    print(f"[INFO] Storing {len(ids)} embeddings...")

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print("[INFO] Stored successfully!")

    return collection