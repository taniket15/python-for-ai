# 13 — Capstone Project: **DocChat API**

A FastAPI service that answers questions about **your own documents** using an LLM, with
per-session chat memory stored in SQLite. It uses every topic from files 01–12.

```
           ┌─────────── POST /chat {session_id, question} ───────────┐
           ▼                                                         │
  retrieve top chunks  ──►  build prompt (context + history)  ──►  OpenAI  ──►  save turn in SQLite
  (01 chunk + 03 cosine)          (02 dicts, 07 memory)            (05, 06 retry)       (12)
```

Write your code in `src/13_project/`. Split it into modules however you
like. A suggested layout:

```
13_project/
  main.py        # FastAPI app + routes                    (11)
  ingest.py      # load + chunk documents                  (01, 09)
  retrieve.py    # score chunks against a question         (01, 03)
  llm.py         # OpenAI calls, retries, structured output (05, 06, 08)
  db.py          # SQLite chat memory                      (12)
  models.py      # Pydantic request/response models        (08, 11)
  data/          # your .txt documents
```

Run it with `uv run uvicorn main:app --reload --app-dir src/13_project`,
then open http://127.0.0.1:8000/docs

---

## Milestones (do them in order and check each one before moving on)

### M1 — Ingest (files 01, 09)
- [ ] Put 3–5 `.txt` files in `data/` (paste in any articles or docs you like).
- [ ] On startup, load them (`load_documents`), clean them, and split each into chunks of
      ~150 words with 30 words of overlap (`chunk_words`).
- [ ] Keep the chunks in memory as a list of dicts: `{"doc": "name", "chunk_id": 0, "text": "..."}`.

### M2 — Retrieve (files 01, 02, 03)
- [ ] Turn a text into a bag-of-words vector (a word -> count `Counter` over a shared
      vocabulary). Score every chunk against the question with `cosine_similarity`.
- [ ] Return the top 3 chunks (`top_k`).

### M3 — Answer (files 05, 06)
- [ ] System prompt: *"Answer ONLY from the provided context. If the answer isn't there,
      say you don't know. Cite the document names you used."*
- [ ] Put the retrieved chunks in the user message, clearly marked:
      `<context doc="name">...</context>`
- [ ] Wrap the OpenAI call in `with_retry`, retrying on `openai.RateLimitError` and
      `openai.APITimeoutError`.

### M4 — Memory (files 07, 12)
- [ ] Save every user question and assistant answer to SQLite, keyed by `session_id`.
- [ ] Send the last 10 messages of the session (`get_history(..., limit=10)` +
      `trim_history`) along with the new question.

### M5 — API (files 08, 10, 11)
| Method | Path | Body / Params | Returns |
|---|---|---|---|
| GET | `/health` | | `{"status": "ok", "chunks": <count>}` |
| POST | `/chat` | `{"session_id": str, "question": str (min 1 char)}` | `{"answer": str, "sources": [doc names]}` |
| GET | `/history/{session_id}` | | list of `{"role", "content"}` |
| DELETE | `/history/{session_id}` | | `{"deleted": <count>}` |
| POST | `/ingest-url` | `{"url": str, "name": str}` | fetches the page with `requests` (timeout!), saves it to `data/<name>.txt`, re-chunks; `{"chunks_added": int}` |
| POST | `/extract-ticket` | `{"text": str}` | a `Ticket` (from file 08) via structured output |

- [ ] Errors map to proper HTTP codes: an unknown session gives `404`; the LLM failing
      after retries gives `503`; a bad URL in ingest gives `400`.

### M6 — Production polish
- [ ] Settings from env vars (`OPENAI_API_KEY`, `OPENAI_MODEL`, `DB_PATH`). Bonus:
      `pydantic-settings`.
- [ ] Use the `logging` module instead of `print` (log the token usage of each call).
- [ ] Tests: use `TestClient` + `FakeOpenAI` from `_check.py` so tests never hit the real API.
- [ ] `uvx ruff check .` and `uvx pyright` pass.

### Stretch goals
- **Streaming**: `stream=True` in the OpenAI call plus FastAPI's `StreamingResponse`,
  with a generator that yields chunks (file 03, Q5).
- **Real embeddings**: replace bag-of-words with `client.embeddings.create(...)` and cache
  the vectors in SQLite.
- **Async**: switch to `AsyncOpenAI` and `async def` routes.
- **Tool calling**: let the model call a `search_docs(query)` tool itself, instead of you
  always retrieving.
- **Eval set**: a JSONL file of `{question, expected_doc}` and a script that measures
  retrieval accuracy (file 09).
