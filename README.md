# Python for AI Engineers

**A hands-on introduction to Python for developers who want to move into AI engineering.**
It's written with TypeScript/JavaScript developers in mind, so every topic shows the
TS/JS equivalent. You don't need to know any TS to use it, though.

There are 12 topic files and 50 exercises, ending in a capstone project. You'll go from
Python syntax to calling LLMs, structured output, chat memory, FastAPI and databases.
Every exercise has tests that run **offline and for free**: the LLM exercises use a fake
client, so you only need an API key if you want to try them for real.

---

## Quick start

1. **Install [uv](https://docs.astral.sh/uv/)**, the Python package manager (think npm + nvm in one):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh     # macOS / Linux
   # Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
2. **Get the code.** Fork this repo (so you can commit your answers), then:
   ```bash
   git clone https://github.com/<you>/python-for-ai.git
   cd python-for-ai
   uv sync            # installs Python + all dependencies into .venv
   ```
3. **Start solving:**
   ```bash
   uv run python src/01_basics.py
   ```
   ```
   ⬜ q1_clean_tokens: not started
   ⬜ q2_chunk_words: not started
   ...
   0/4 passed
   ```
   Open the file, read the **THEORY** section at the top, then replace each
   `raise NotImplementedError  # TODO` with your code. Re-run until everything is ✅.

> Using pip instead of uv? `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`,
> then run with `python src/01_basics.py`.

---

## What's inside

Each file has the same layout:

1. **THEORY**: the Python concepts you need, the classic gotchas, and a TS/JS → Python table
2. **WHY THIS MATTERS FOR AI**: where you'll meet the concept in real AI work
3. **Questions**: function or class stubs with hints
4. **Tests**: don't edit these. Run the file to check your answers.

| # | File | Topic | What you'll build |
|---|---|---|---|
| 01 | [`01_basics.py`](src/01_basics.py) | Data types, lists, for loops | Text cleaning, RAG chunking, top-k ranking |
| 02 | [`02_dicts_tuples.py`](src/02_dicts_tuples.py) | Dicts, tuples, sets | Chat messages, labelled data, config merging |
| 03 | [`03_functions.py`](src/03_functions.py) | Functions, `*args`/`**kwargs`, decorators, generators | Prompt templates, cosine similarity, streaming |
| 04 | [`04_classes.py`](src/04_classes.py) | Classes, dataclasses, inheritance | Conversation objects, swappable model backends |
| 05 | [`05_call_llm.py`](src/05_call_llm.py) | Calling an LLM (OpenAI) | Requests, responses, finish reasons, cost estimates |
| 06 | [`06_errors.py`](src/06_errors.py) | Error handling | Custom exceptions, retry with exponential backoff |
| 07 | [`07_chatbot_memory.py`](src/07_chatbot_memory.py) | Chatbot with memory | History windows, closures, a live terminal chat |
| 08 | [`08_structured_output.py`](src/08_structured_output.py) | Pydantic + structured output | Validating LLM JSON, `response_format` |
| 09 | [`09_files.py`](src/09_files.py) | File handling | JSONL datasets, loading documents |
| 10 | [`10_requests.py`](src/10_requests.py) | HTTP with `requests` | Timeouts, errors, testable API clients |
| 11 | [`11_fastapi.py`](src/11_fastapi.py) | FastAPI | Serving AI behind an API, async routes |
| 12 | [`12_database.py`](src/12_database.py) | SQLite | Persistent chat memory, avoiding SQL injection |
| 13 | [`13_project/`](src/13_project/README.md) | **Capstone: DocChat API** | RAG + memory + structured output, end to end |

**Brand new to Python?** Start with the 5 optional warm-ups in [`src/extra/`](src/extra/):
FizzBuzz, strings, comprehensions, dicts and classes.

```bash
uv run python src/extra/ex1_fizzbuzz.py
```

### Stuck? Check the solutions

Every exercise has a solution with the same file name in [`src/solutions/`](src/solutions/)
(warm-ups: [`src/extra/solutions/`](src/extra/solutions/)), written as plain, beginner-friendly code. Try the exercise yourself first! To see the
tests pass with the official answers:

```bash
uv run python src/01_basics.py --solution
```

There's usually more than one correct answer. If your tests pass, your solution is right.

### Trying the LLM exercises for real (optional)

Files 05, 07 and 08 can call the real OpenAI API with `--live`. (File 10's `--live`
calls a free public test API and needs no key.)

```bash
cp .env.example .env        # then put your key in it, or just:
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=<any chat model your account can use>

uv run python src/07_chatbot_memory.py --live
```

The tests themselves never need a key.

---

## Tooling: npm → uv

| npm / Node | uv / Python |
|---|---|
| `npm init` | `uv init` |
| `npm install pkg` | `uv add pkg` |
| `npm install -D pkg` | `uv add --dev pkg` |
| `npx tool` | `uvx tool` (e.g. `uvx ruff check .`) |
| `node file.js` | `uv run python file.py` |
| `package.json` / `package-lock.json` | `pyproject.toml` / `uv.lock` |
| `node_modules/` (per project) | `.venv/` (per-project virtual environment) |
| `.nvmrc` | `.python-version` |
| ESLint + Prettier | `ruff check` + `ruff format` |
| `tsc --noEmit` | `pyright` or `mypy` |
| Jest / Vitest | `pytest` |

## The 15 Python things that trip up TS developers

1. **Indentation is syntax.** A colon plus 4 spaces opens a block. No braces, no semicolons.
2. **`None`** is the only null. There's no `undefined`. A missing dict key or list index
   **raises** (`KeyError` / `IndexError`) instead of returning `undefined`.
3. **Empty containers are falsy:** `[]`, `{}`, `""`, `0`. (In JS, `[]` and `{}` are truthy.)
4. **`==` compares values** (`[1, 2] == [1, 2]` is `True`); **`is`** compares identity.
   Use `is None`.
5. **No implicit coercion:** `"1" + 1` is a `TypeError`.
6. **`/` always gives a float**; `//` is floor division; `**` is power.
7. **No block scope:** variables from inside `if`/`for` live on after the block (like `var`).
8. **Mutable default arguments are shared** between calls. Use `None` and create the
   value inside.
9. **Type hints are not enforced at runtime.** Run `pyright` or `mypy` to get TS-like checking.
10. **Keyword arguments** replace "options objects": `create(model="x", messages=m)`.
11. **`self` is explicit** in every method; there's no `new`.
12. **Comprehensions** replace most `.map`/`.filter` chains: `[f(x) for x in xs if cond]`.
13. **Sync by default.** Async exists (`async`/`await`/`asyncio`), but you opt in, and you
    need an async library (httpx, AsyncOpenAI). Blocking inside `async def` freezes the
    event loop.
14. **`if __name__ == "__main__":`** means "run only when executed directly", not when imported.
15. **Strings:** f-strings `f"{x}"`; single and double quotes are the same; triple quotes
    make multi-line strings; strings are immutable.

## Theory every AI engineer should know (beyond these files)

- **Generators & `yield`**: lazy iteration. Used for streaming LLM tokens and processing
  big datasets without loading them into memory.
- **Context managers (`with`)**: guaranteed cleanup for files, DB connections, HTTP
  sessions and locks. You can write your own with `@contextlib.contextmanager`.
- **Concurrency model**: the GIL means one thread runs Python bytecode at a time.
  - I/O-bound work (API calls), which is most AI apps: use **asyncio** (or threads).
  - CPU-bound work (heavy number crunching): use **multiprocessing**, or libraries like
    NumPy/PyTorch that run outside the GIL.
  - `asyncio.gather(...)` ≈ `Promise.all(...)`. Use it to call an LLM on many inputs in
    parallel (with a `Semaphore` to respect rate limits).
- **Typing**: `list[str]`, `dict[str, int]`, `X | None`, `Literal[...]`,
  `Callable[[A], B]`, `TypedDict` (≈ TS object types), `Protocol` (≈ TS interfaces).
- **Pydantic everywhere**: LLM outputs, FastAPI bodies, settings, tool schemas.
- **The data stack**: NumPy (arrays/vectors), pandas (tables), and later PyTorch /
  Hugging Face `transformers` if you go beyond API calls.
- **Environment & secrets**: env vars, `.env` + `python-dotenv`, never commit keys.
- **Testing**: `pytest`, fakes and mocks (`unittest.mock`), keeping LLM calls behind an
  interface so tests run offline. The `FakeOpenAI` in [`src/_check.py`](src/_check.py)
  is an example.

---

## Repo layout

```
src/
  01_basics.py ... 12_database.py   # topic files: theory + exercises + tests
  13_project/README.md              # capstone spec (build it in that folder)
  solutions/                        # answers for every exercise (same file names)
  _check.py                         # tiny test runner + FakeOpenAI (no need to edit)
  extra/                            # optional warm-ups for total beginners
    ex1_fizzbuzz.py ... ex5_classes.py
    solutions/                      # answers for the warm-ups
    _check.py                       # the same test runner
```

## Contributing

Found a bug in a test, a confusing hint, or have an idea for an exercise? Issues and
pull requests are welcome. Please keep exercises beginner-friendly, keep tests offline,
and include a TS/JS comparison where it helps.

## License

[MIT](LICENSE)
