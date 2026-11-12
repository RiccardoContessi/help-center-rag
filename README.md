# Help Center RAG

A RAG chatbot that answers questions about FjordBooks, a fictional Swiss accounting app,
using only its help-center articles and internal policies (VAT, expenses, travel, pricing...).

- Answers only from the documents, with the sources cited.
- Says "I don't know" when the documents don't cover the question, and declines off-topic questions.
- Remembers the conversation within the same chat.
- A router sends each message to the right path: document questions, support requests or off-topic.
- Numbers (like prices with discounts) are computed by a tool, not by the model.

**Stack:** Python, FastAPI, LangGraph, LangChain, OpenAI, Chroma.

**Run:**
    uv sync
    uv run python -m app.ingestion
    uv run uvicorn app.main:app --reload


---

ENDPOINTS:

| operation | path     | header | path_params | query_params | input_body                       | output_body                      | status_code                                                                              |
|-----------|----------|--------|-------------|--------------|----------------------------------|----------------------------------|------------------------------------------------------------------------------------------|
| POST      | /v1/chat |        |             |              | question, thread_id (optional)   | answer, thread_id, sources       | 200 – OK<br>422 – Unprocessable Content<br>502 – Bad Gateway<br>504 – Gateway Timeout     |
| GET       | /health  |        |             |              |                                  |                                  | 200 – OK                                                                                 |

