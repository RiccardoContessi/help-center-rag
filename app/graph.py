from langgraph.graph import StateGraph, START, END
from app.state import State
from app.tools import tool_node, call_model_node, conditional_tool_edge
from langgraph.checkpoint.memory import InMemorySaver



def build_graph():
    graph = StateGraph(State)

    graph.add_node("callModel", call_model_node)
    graph.add_node("ToolNode", tool_node)

    graph.add_edge(START, "callModel")
    graph.add_conditional_edges("callModel", conditional_tool_edge, 
                                {"CONTINUE": "ToolNode",
                                "END": END})
    graph.add_edge("ToolNode", "callModel")

    app = graph.compile(checkpointer=InMemorySaver())
    return app

    