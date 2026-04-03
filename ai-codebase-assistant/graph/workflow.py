from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.nodes import (
    retrieve_node,
    build_context_node,
    evaluate_context_node,
    read_more_node,
    retrieve_again_node,
    answer_node
)


def decide_next_step(state):
    if state["needs_more_context"]:
        return "read_more"
    return "answer"


def create_workflow():
    workflow = StateGraph(GraphState)

    # Nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("build_context", build_context_node)
    workflow.add_node("evaluate", evaluate_context_node)
    workflow.add_node("read_more", read_more_node)
    workflow.add_node("retrieve_again", retrieve_again_node)
    workflow.add_node("answer", answer_node)

    # Entry
    workflow.set_entry_point("retrieve")

    # Initial flow
    workflow.add_edge("retrieve", "build_context")
    workflow.add_edge("build_context", "evaluate")

    # Conditional branching
    workflow.add_conditional_edges(
        "evaluate",
        decide_next_step,
        {
            "read_more": "read_more",
            "answer": "answer"
        }
    )

    # Loop path
    workflow.add_edge("read_more", "retrieve_again")
    workflow.add_edge("retrieve_again", "build_context")

    # Exit
    workflow.add_edge("answer", END)

    return workflow.compile()