from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def embed_documents(chunked_docs):
    embedded_docs = []

    for doc in chunked_docs:
        embedding = generate_embedding(doc["content"])

        embedded_docs.append({
            "embedding": embedding,
            "content": doc["content"],
            "metadata": doc["metadata"]
        })

    return embedded_docs