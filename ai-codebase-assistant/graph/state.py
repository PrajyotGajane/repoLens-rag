from typing import TypedDict, List, Dict


class GraphState(TypedDict):
    query: str
    chunks: List[Dict]
    context: str
    answer: str
    needs_more_context: bool
    iteration_count: int