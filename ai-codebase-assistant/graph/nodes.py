from vectordb.retriever import retrieve_chunks
from vectordb.reranker import simple_rerank
from vectordb.context_builder import build_context
from rag.generator import generate_answer
from agents.tools import read_file_raw

MAX_ITERATIONS = 2


def retrieve_node(state):
    print("[TRACE] RETRIEVE NODE")
    query = state["query"]

    chunks = retrieve_chunks(query, top_k=10)
    reranked = simple_rerank(query, chunks)

    return {
        "chunks": reranked
    }


def build_context_node(state):
    print("[TRACE] BUILD CONTEXT NODE")
    context = build_context(state["chunks"])

    return {
        "context": context
    }


def evaluate_context_node(state):
    print("[TRACE] EVALUATE CONTEXT NODE")
    context = state["context"]
    iteration = state.get("iteration_count", 0)

    needs_more = len(context) < 3000 and iteration < MAX_ITERATIONS

    print(f"[DEBUG] Iteration: {iteration} | Context length: {len(context)} | Needs more: {needs_more}")

    return {
        "needs_more_context": needs_more,
        "iteration_count": iteration + 1
    }


def read_more_node(state):
    print("[TRACE] READ MORE NODE")
    chunks = state["chunks"]

    if not chunks:
        return {}

    top_file = chunks[0]["metadata"]["file"]

    print(f"[DEBUG] Reading file: {top_file}")

    full_content = read_file_raw(top_file)

    return {
        "context": state["context"] + "\n\n" + full_content
    }


def retrieve_again_node(state):
    print("[TRACE] RETRIEVE AGAIN NODE")
    # Re-run retrieval with same query but now context is richer
    query = state["query"]

    print("[DEBUG] Re-retrieving with enriched context")

    chunks = retrieve_chunks(query, top_k=10)
    reranked = simple_rerank(query, chunks)

    return {
        "chunks": reranked
    }


def answer_node(state):
    print("[TRACE] ANSWER NODE")
    answer = generate_answer(state["query"], state["context"])

    return {
        "answer": answer
    }
