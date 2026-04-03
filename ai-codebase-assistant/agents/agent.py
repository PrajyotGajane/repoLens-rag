from rag.generator import generate_answer
from vectordb.retriever import retrieve_chunks
from vectordb.reranker import simple_rerank
from vectordb.context_builder import build_context
from agents.tools import read_file


def run_agent(query: str):
    print("\n[AGENT] Thinking...\n")

    # Step 1: Search
    chunks = retrieve_chunks(query, top_k=10)

    # Step 2: Rerank
    reranked = simple_rerank(query, chunks)

    # Step 3: Build context
    context = build_context(reranked)

    # Step 4: (Optional) Read full file if needed
    # (we’ll make this smarter in LangGraph)

    # Step 5: Generate answer
    answer = generate_answer(query, context)

    return answer