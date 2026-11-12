import json
import openai
from app.graph import build_graph
from fastapi import APIRouter, FastAPI, HTTPException, Request, status
from contextlib import asynccontextmanager
from app.schemas import ChatResponse, ChatRequest
from app.vector_store import get_vector_store
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.messages import AnyMessage


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.graph = build_graph()
    get_vector_store()
    print("app started")
    yield
    print("app stopped")


app = FastAPI(lifespan=lifespan)

router = APIRouter(prefix="/v1")


def extract_sources(messages: list[AnyMessage]) -> list[str]:
    sources = set() 
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            break
        if isinstance(msg, ToolMessage) and msg.name == "search_docs":
            for chunks in json.loads(msg.content):
                sources.add(chunks["source"])
    return sources

@router.post("/chat", response_model=ChatResponse)
async def get_chat(request: Request, body: ChatRequest):
    config = {"configurable":{"thread_id": str(body.thread_id)}}
    graph = request.app.state.graph

    try:
        response = await graph.ainvoke({"messages": [HumanMessage(body.question)]}, config=config)
    except openai.APITimeoutError as e:
        raise HTTPException(status.HTTP_504_GATEWAY_TIMEOUT, "LLM provider timed out") from e
    except openai.APIError as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "LLM provider error") from e

    messages = response["messages"]

    return ChatResponse(
        answer= messages[-1].content,
        thread_id=str(body.thread_id),
        sources= extract_sources(messages)
    )

app.include_router(router)