from ingest.ingest_service import ingest_repository
from embeddings.pipeline import process_documents
from vectordb.chroma_store import store_embeddings
from graph.workflow import create_workflow


if __name__ == "__main__":
    repo_url = input("Enter GitHub repo URL: ")

    docs = ingest_repository(repo_url)
    embedded_docs = process_documents(docs)
    store_embeddings(embedded_docs)

    app = create_workflow()

    print("\n=== LANGGRAPH READY ===\n")

    while True:
        query = input("\nAsk something (or 'exit'): ")

        if query.lower() == "exit":
            break

        result = app.invoke(
            {
                "query": query,
                "iteration_count": 0
            },
            config={
                "metadata": {
                    "user_query": query
                }
            }
        )
        print("\n=== ANSWER ===\n")
        print(result["answer"])