# Solutions for 11_fastapi.py
# Test them with:  uv run python src/11_fastapi.py --solution
# (`app`, `ITEMS`, `CHAT_HISTORY` and `ChatResponse` come from the exercise file.)
import asyncio

from fastapi import HTTPException, Query
from pydantic import BaseModel, Field


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    return ITEMS[item_id]


@app.get("/search")
def search(q: str, limit: int = Query(5, ge=1, le=20)):
    results = []
    for item in ITEMS.values():
        if q.lower() in item["name"].lower():
            results.append(item["name"])
    return {"results": results[:limit]}


class ChatRequest(BaseModel):
    user_id: str
    message: str = Field(min_length=1)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if request.user_id not in CHAT_HISTORY:
        CHAT_HISTORY[request.user_id] = []
    CHAT_HISTORY[request.user_id].append(request.message)
    return ChatResponse(
        reply=f"You said: {request.message}",
        history_length=len(CHAT_HISTORY[request.user_id]),
    )


@app.get("/slow-sum")
async def slow_sum(a: int, b: int):
    await asyncio.sleep(0.01)
    return {"sum": a + b}
