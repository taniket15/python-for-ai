"""
05 — Calling an LLM (OpenAI)
============================

THEORY (read first)
-------------------
1. Setup: `uv add openai` (already done). Put your key in an env var, never in code:
       export OPENAI_API_KEY="sk-..."
   Read env vars with os.environ["X"] (KeyError if missing) or os.getenv("X", default),
   the same idea as process.env.X. For local dev, people often use a .env file plus
   `python-dotenv`. Add .env to .gitignore!
2. Imports: `import openai` or `from openai import OpenAI`. A module is a file and a
   package is a folder. `if __name__ == "__main__":` means "only run this when the file
   is executed directly, not when it's imported" (like `require.main === module`).
3. The Chat Completions API is STATELESS: you send the whole conversation every time as a
   list of {"role": ..., "content": ...} dicts. Roles: "system" (or "developer") for
   instructions, "user", "assistant". `max_completion_tokens` caps the output length.
4. The response: response.choices[0].message.content is the text (it can be None!).
   response.choices[0].finish_reason tells you why it stopped:
       "stop" (finished)  |  "length" (hit the token cap, output is CUT OFF)
       "content_filter"   |  "tool_calls" (the model wants to call a tool)
   response.usage.prompt_tokens / completion_tokens are what you pay for.
5. Tokens: roughly 4 characters of English is 1 token. You pay per input + output token,
   and the context window limits the total. Every chat turn re-sends (and re-bills) the
   whole history.
6. Sync vs async: the Python SDK is synchronous by default, so calls block. For
   concurrency, use `AsyncOpenAI()` with `await`. (In TS, everything is async.)
7. Python calls use KEYWORD ARGUMENTS where TS passes one object. You'll often build
   the options as a dict and spread it:  client.chat.completions.create(**request)
8. Duck typing makes testing easy: these tests pass a FAKE client that only has
   `.chat.completions.create()`. Python doesn't check the type, just that the attribute
   exists, so you can test LLM code offline for free.
9. Other SDKs look almost the same (Anthropic: client.messages.create(...), where
   system is a separate parameter and the text is in response.content blocks).

TS / JS  ->  Python
-------------------
    import OpenAI from "openai"                 from openai import OpenAI
    const client = new OpenAI()                 client = OpenAI()
    const res = await client.chat.completions   res = client.chat.completions.create(
      .create({ model, messages })                  model=MODEL, messages=messages
                                                )
    res.choices[0].message.content              res.choices[0].message.content
    process.env.OPENAI_API_KEY                  os.environ["OPENAI_API_KEY"]

Run tests:      uv run python src/05_call_llm.py
Call for real:  uv run python src/05_call_llm.py --live   (needs OPENAI_API_KEY)
"""
import os
import sys
from types import SimpleNamespace

from _check import FakeOpenAI, eq, raises, run

# Change this (or set the OPENAI_MODEL env var) to any chat model your account can use.
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Build the keyword arguments for client.chat.completions.create(...) as a dict:
#   {"model": MODEL, "max_completion_tokens": max_tokens, "messages": [...]}
# messages = an optional {"role": "system", ...} message (ONLY if system is given),
#            then {"role": "user", "content": prompt}
#
#   build_request("Hi")  ->  {"model": MODEL, "max_completion_tokens": 1024,
#                             "messages": [{"role": "user", "content": "Hi"}]}
def build_request(prompt: str, system: str | None = None, max_tokens: int = 1024) -> dict:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# Pull the text out of a response: response.choices[0].message.content.
# The content can be None, so return "" in that case.
def extract_text(response) -> str:
    raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# Put it together: call client.chat.completions.create(**build_request(...)) and
# return the text.
# If finish_reason is "length", the answer was cut off: raise RuntimeError.
def ask(client, prompt: str, system: str | None = None) -> str:
    raise NotImplementedError  # TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# Estimate the cost in dollars from response.usage. Prices are per 1 MILLION tokens.
#
#   estimate_cost(usage(prompt_tokens=1000, completion_tokens=500),
#                 input_price=0.10, output_price=0.40)
#     -> 1000 * 0.10 / 1_000_000 + 500 * 0.40 / 1_000_000 = 0.0003
#
# (Python allows underscores in numbers for readability: 1_000_000)
def estimate_cost(usage, input_price: float, output_price: float) -> float:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_build_request():
    eq(build_request("Hi"), {
        "model": MODEL,
        "max_completion_tokens": 1024,
        "messages": [{"role": "user", "content": "Hi"}],
    })
    req = build_request("Hi", system="Be brief", max_tokens=50)
    eq(req["messages"], [{"role": "system", "content": "Be brief"}, {"role": "user", "content": "Hi"}])
    eq(req["max_completion_tokens"], 50)


def test_q2_extract_text():
    fake = FakeOpenAI(reply="Paris")
    eq(extract_text(fake.chat.completions.create(model="x", messages=[])), "Paris")
    empty = FakeOpenAI(reply=None)
    eq(extract_text(empty.chat.completions.create(model="x", messages=[])), "")


def test_q3_ask():
    fake = FakeOpenAI(reply="Paris")
    eq(ask(fake, "Capital of France?", system="One word."), "Paris")
    eq(fake.calls[0]["messages"][-1], {"role": "user", "content": "Capital of France?"})
    eq(fake.calls[0]["model"], MODEL)
    raises(RuntimeError, ask, FakeOpenAI(finish_reason="length"), "Write a novel")


def test_q4_estimate_cost():
    usage = SimpleNamespace(prompt_tokens=1000, completion_tokens=500)
    eq(round(estimate_cost(usage, input_price=0.10, output_price=0.40), 8), 0.0003)


def live_demo():
    from openai import OpenAI

    client = OpenAI()  # reads OPENAI_API_KEY from the environment
    print(ask(client, "Explain Python list comprehensions to a TypeScript developer.",
              system="Answer in 3 short sentences."))


if __name__ == "__main__":
    if "--live" in sys.argv:
        live_demo()
    else:
        run(globals())
