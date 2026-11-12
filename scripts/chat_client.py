import httpx

thread_id = None  # first request: the server creates a new conversation

while True:
    question = input("You: ").strip()
    if question in {"exit", "quit"}:
        break
    if not question:
        continue

    payload = {"question": question}
    if thread_id:
        payload["thread_id"] = thread_id  # same thread = the bot remembers

    response = httpx.post("http://127.0.0.1:8000/v1/chat", json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    thread_id = data["thread_id"]

    print(f"Bot: {data['answer']}")
    print(f"Sources: {data['sources']}\n")