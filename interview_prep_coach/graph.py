from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# pyrefly: ignore [missing-import]
from models import State
# pyrefly: ignore [missing-import]
from nodes import worker, evaluator, worker_router, route_after_eval
# pyrefly: ignore [missing-import]
from tools import tools

def build_graph():
    graph_builder = StateGraph(State)

    graph_builder.add_node("worker", worker)
    graph_builder.add_node("tools", ToolNode(tools=tools))
    graph_builder.add_node("evaluator", evaluator)

    graph_builder.add_edge(START, "worker")
    graph_builder.add_conditional_edges(
        "worker", 
        worker_router, 
        {"tools": "tools", "evaluator": "evaluator"}
        )
    graph_builder.add_edge("tools", "worker")
    graph_builder.add_conditional_edges(
        "evaluator",
        route_after_eval,
        {"worker": "worker", "END": END}
    )

    memory = MemorySaver()
    return graph_builder.compile(checkpointer=memory)

graph = build_graph()