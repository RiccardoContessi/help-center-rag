from langchain_core.tools import tool
from simpleeval import simple_eval
from app.state import State
from app.vector_store import get_vector_store
from app.config import get_settings
import json
from functools import lru_cache
from langchain_openai import ChatOpenAI
from app.prompt import SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import ToolNode


settings = get_settings()

@tool
def calculate(expression: str) -> str:
    """
    this calculate tool is able to answer to complex mathematical problems, solving
    them 1 step at a time. 
    Compute real operation, never do them in your mind.
    Es: 5 + (6*30) -> step1: 5 + 180. step2 -> 185. so you need 2 tool calls to answer this
    """
    try:
        return str(round(simple_eval(expr=expression), 3))
    except Exception as e:
        return f"Error: {e}"


@tool
def search_docs(query: str) -> str:
    """Search the FjordBooks help center docs (VAT, QR-bills, pricing, data retention).
    Use it before answering any question about FjordBooks."""
        
    vector_store = get_vector_store()
    result = vector_store.similarity_search_with_relevance_scores(
        query=query, 
        k= settings.top_k, 
        score_threshold= settings.score_threshold
    )
    # for doc, score in result:
    #     print(doc.metadata)
    #     print(score)

    chunks = [{
        "content": doc.page_content,
        "source": doc.metadata["source"],
        "page": doc.metadata.get("page"),
        "score": round(score, 2),
    } for doc, score in result]

    # TEST VARI:
    # doc = result[0][0]
    # print(type(doc))                   # langchain_core.documents.base.Document
    # print(doc.model_dump().keys())      # its fields: id, metadata, page_content, type
    # print(dir(doc))                     # everything, methods included (noisier)

    return json.dumps(chunks, ensure_ascii=False)

TOOLS = [calculate, search_docs] 


@lru_cache
def build_llm():
    llm = ChatOpenAI(
        model = settings.llm_model,
        api_key= settings.hcr_openai_api_key.get_secret_value(),
        temperature=0.0,
        base_url=settings.openai_base_url
    )
    return llm.bind_tools(tools=TOOLS)


prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("messages")
])


def call_model_node(state: State):
    chain = prompt | build_llm()
    response = chain.invoke({"messages": state["messages"]})
    return {"messages" : [response]}



tool_node = ToolNode(TOOLS)



def conditional_tool_edge(state: State):
    if state["messages"][-1].tool_calls:
        return "CONTINUE"
    return "END"