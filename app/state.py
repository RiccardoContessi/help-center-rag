from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class State(TypedDict):
    # Annotated[type, metadata]: Python only sees the type; LangGraph also reads the metadata.
    messages: Annotated[
        list[AnyMessage],  # the conversation: Human, AI and Tool messages with roles, tool calls and ids
        add_messages,      # reducer: node updates are appended to the list instead of replacing it
    ]

# es: Annotated[int, Field(ge=0), "number of receipts", qualcosa_altro]