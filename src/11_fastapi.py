"""
11 — FastAPI
============

THEORY (read first)
-------------------
1. FastAPI ≈ Express/Fastify + Zod + automatic Swagger docs. It's the default way to put
   an AI model or agent behind an HTTP API in Python. (Installed: fastapi[standard],
   which includes the uvicorn server and httpx for tests.)
2. Routes are DECORATORS:  @app.get("/path")  above a function. Whatever the function
   returns (dict / list / Pydantic model) is serialized to JSON for you, no res.json().
3. Inputs come from the function SIGNATURE plus type hints:
     path param:   @app.get("/items/{item_id}")  def f(item_id: int)      (req.params)
                   -> converted to int; "/items/abc" gets an automatic 422 error
     query param:  any other simple argument:  def search(q: str, limit: int = 5)
                   -> /search?q=x&limit=3                                 (req.query)
     body:         an argument typed as a Pydantic model -> parsed + validated JSON
                                                                         (req.body + zod)
     Constraints:  limit: int = Query(5, ge=1, le=20)   /   Field(min_length=1) on models
   Invalid input automatically gets a 422 response with details.
4. Errors: raise HTTPException(status_code=404, detail="Not found")
   ≈ res.status(404).json({ detail: "Not found" })
5. response_model=MyModel validates and filters what you return.
6. async def vs def:
     - Use `async def` when you `await` things inside (AsyncOpenAI, httpx.AsyncClient,
       asyncio.sleep).
     - Plain `def` routes run in a thread pool, which is fine for blocking code like
       `requests`.
     ⚠️ Never call blocking code (time.sleep, requests.get, the sync OpenAI client)
       inside an `async def` route. It freezes the whole server, exactly like blocking
       the Node event loop.
7. Python async in one minute: async/await look like JS, but no event loop runs by
   default. asyncio.run(main()) starts one (FastAPI/uvicorn does that for you), and
   asyncio.gather(a(), b()) ≈ Promise.all([a(), b()]).
8. Depends() gives you dependency injection (DB sessions, current user, settings), like
   per-route middleware.
9. Free docs: start the server and open http://127.0.0.1:8000/docs

TS / JS (Express)  ->  Python (FastAPI)
---------------------------------------
    const app = express()                     app = FastAPI()
    app.get("/health", (req, res) =>          @app.get("/health")
      res.json({ status: "ok" }))             def health(): return {"status": "ok"}
    req.params.id                             def f(id: int)          # from "/x/{id}"
    req.query.q                               def f(q: str)
    req.body  (+ zod parse)                   def f(body: MyModel)
    res.status(404).json({...})               raise HTTPException(404, "...")
    app.listen(8000)                          uvicorn.run(app, port=8000)

Run tests:     uv run python src/11_fastapi.py
Run a server:  uv run python src/11_fastapi.py --serve   then open /docs
"""
import asyncio
import inspect
import sys

from fastapi import FastAPI, HTTPException, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from _check import eq, run

app = FastAPI(title="Exercise 11")

ITEMS = {
    1: {"id": 1, "name": "Python Crash Course"},
    2: {"id": 2, "name": "Prompt Engineering Guide"},
    3: {"id": 3, "name": "Python for Data Science"},
}
CHAT_HISTORY: dict[str, list[str]] = {}  # user_id -> messages that user has sent


# Q1 ─────────────────────────────────────────────────────────────────────────────
# GET /health  ->  {"status": "ok"}
# TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# GET /items/{item_id}   (item_id is an int)
#   -> the item dict from ITEMS
#   -> 404 with detail "Item not found" if it doesn't exist
# TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# GET /search?q=python&limit=5
#   -> {"results": [names of ITEMS whose name contains q, case-insensitive]}
#   `limit` defaults to 5 and must be between 1 and 20: Query(5, ge=1, le=20)
#   Return at most `limit` results.
# TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# POST /chat with a JSON body like {"user_id": "u1", "message": "hi"}
#   - make `message` required to be at least 1 character (edit ChatRequest below)
#   - store the message in CHAT_HISTORY[user_id] (create the list on first use)
#   - respond with ChatResponse: reply = "You said: <message>",
#     history_length = how many messages that user has sent so far
class ChatRequest(BaseModel):
    user_id: str
    message: str  # TODO: add a min_length=1 constraint using Field(...)


class ChatResponse(BaseModel):
    reply: str
    history_length: int


# TODO: the POST /chat route (use response_model=ChatResponse)


# Q5 ─────────────────────────────────────────────────────────────────────────────
# GET /slow-sum?a=1&b=2  ->  {"sum": 3}
# Make it an `async def` route that does `await asyncio.sleep(0.01)` first,
# to simulate awaiting an async LLM call.
# TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
client = TestClient(app)  # like supertest: calls the app without starting a server


def test_q1_health():
    r = client.get("/health")
    eq(r.status_code, 200)
    eq(r.json(), {"status": "ok"})


def test_q2_get_item():
    r = client.get("/items/2")
    eq(r.status_code, 200)
    eq(r.json(), {"id": 2, "name": "Prompt Engineering Guide"})
    r = client.get("/items/99")
    eq(r.status_code, 404)
    eq(r.json(), {"detail": "Item not found"})
    eq(client.get("/items/abc").status_code, 422)  # automatic validation


def test_q3_search():
    r = client.get("/search", params={"q": "PYTHON"})
    eq(r.status_code, 200)
    eq(r.json(), {"results": ["Python Crash Course", "Python for Data Science"]})
    eq(client.get("/search", params={"q": "python", "limit": 1}).json(), {"results": ["Python Crash Course"]})
    eq(client.get("/search", params={"q": "python", "limit": 50}).status_code, 422)


def test_q4_chat():
    CHAT_HISTORY.clear()
    r = client.post("/chat", json={"user_id": "u1", "message": "hi"})
    eq(r.status_code, 200)
    eq(r.json(), {"reply": "You said: hi", "history_length": 1})
    eq(client.post("/chat", json={"user_id": "u1", "message": "again"}).json()["history_length"], 2)
    eq(client.post("/chat", json={"user_id": "u2", "message": "yo"}).json()["history_length"], 1)
    eq(client.post("/chat", json={"user_id": "u1", "message": ""}).status_code, 422)
    eq(client.post("/chat", json={"message": "no user"}).status_code, 422)


def test_q5_async_route():
    r = client.get("/slow-sum", params={"a": 1, "b": 2})
    eq(r.status_code, 200)
    eq(r.json(), {"sum": 3})
    route = next(rt for rt in app.routes if getattr(rt, "path", None) == "/slow-sum")
    assert inspect.iscoroutinefunction(route.endpoint), "make it an `async def`"


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn

        uvicorn.run(app, port=8000)
    else:
        run(globals())
