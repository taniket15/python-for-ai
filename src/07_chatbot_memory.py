"""
07 — Chatbot with Memory
========================

THEORY (read first)
-------------------
1. LLMs have NO memory. "Memory" means YOU store the conversation and re-send it on
   every turn.
2. Cost and latency grow with the history, because you pay for every input token on
   every turn, and the context window is finite. So you trim:
     - sliding window: keep only the last N messages (Q1)
     - summarization: replace old turns with an LLM-written summary
     - retrieval: store everything, then fetch only the relevant past messages
       (vector memory)
   Always keep the system prompt.
3. After trimming, the window should start with a "user" message. Starting with an
   orphaned assistant reply confuses the model.
4. Lists are passed BY REFERENCE (like JS arrays). If something mutates the list you
   handed it, your list changes too. Copy when needed: list(xs), xs[:], copy.deepcopy(xs).
5. Interactive loops: input("You: ") reads one line from the terminal (like readline).
   Use `while True:` with `break`.
6. Dependency injection with callables: ChatBot takes an `llm` FUNCTION shaped like
   (messages) -> str. Use a fake in tests and OpenAI in production. In TS you'd type it
   `(messages: Message[]) => Promise<string>`; in Python, Callable[[list[dict]], str].
7. Closures (Q3): a function that returns a function which "remembers" the client,
   just like in JS.

Run tests:  uv run python src/07_chatbot_memory.py
Chat live:  uv run python src/07_chatbot_memory.py --live   (needs OPENAI_API_KEY)
"""
import os
import sys
from collections.abc import Callable

from _check import FakeOpenAI, eq, run

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")
LLMFn = Callable[[list[dict]], str]  # a type alias, like `type LLMFn = (m: Message[]) => string`


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Return a NEW list with the last `max_messages` messages. Then drop messages from the
# FRONT until the first one has role "user". Don't modify the input list.
#
#   h = [u1, a1, u2, a2, u3]
#   trim_history(h, 3)  -> [u2, a2, u3]
#   trim_history(h, 2)  -> [u3]          ([a2, u3] starts with assistant, so drop a2)
def trim_history(messages: list[dict], max_messages: int) -> list[dict]:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# A chatbot that remembers. `history` keeps EVERY message, but the llm only sees:
#     [system message (if any)] + trim_history(history, max_messages)
# send(text):
#   1. append {"role": "user", "content": text} to history
#   2. call self.llm(messages_to_send)
#   3. append {"role": "assistant", "content": reply} to history
#   4. return reply
# reset(): forget the conversation (empty the history).
class ChatBot:
    def __init__(self, llm: LLMFn, system: str = "", max_messages: int = 20):
        self.llm = llm
        self.system = system
        self.max_messages = max_messages
        self.history: list[dict] = []

    def send(self, text: str) -> str:
        raise NotImplementedError  # TODO

    def reset(self) -> None:
        raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# Return an `llm(messages) -> str` function (a CLOSURE over `client`) that calls
#   client.chat.completions.create(model=MODEL, messages=messages, max_completion_tokens=1024)
# and returns the reply text ("" if the content is None).
def openai_llm(client) -> LLMFn:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def _m(role, text):
    return {"role": role, "content": text}


def test_q1_trim_history():
    h = [_m("user", "u1"), _m("assistant", "a1"), _m("user", "u2"), _m("assistant", "a2"), _m("user", "u3")]
    eq(trim_history(h, 3), h[2:])
    eq(trim_history(h, 2), [h[4]])
    full = trim_history(h, 10)
    eq(full, h)
    assert full is not h, "return a NEW list"
    eq(len(h), 5)


def test_q2_chatbot():
    seen = []

    def fake_llm(messages):
        seen.append(list(messages))
        return f"reply {len(messages)}"

    bot = ChatBot(fake_llm, system="Be brief", max_messages=2)
    eq(bot.send("hi"), "reply 2")  # system + 1 user message
    eq(seen[0], [_m("system", "Be brief"), _m("user", "hi")])
    eq(bot.history, [_m("user", "hi"), _m("assistant", "reply 2")])

    bot.send("again")
    eq(seen[1], [_m("system", "Be brief"), _m("user", "again")])  # window of 2 -> trimmed
    eq(len(bot.history), 4)  # but the full history is kept

    bot.reset()
    eq(bot.history, [])

    no_system = ChatBot(fake_llm)
    no_system.send("hey")
    eq(seen[-1], [_m("user", "hey")])


def test_q3_openai_llm():
    fake = FakeOpenAI(reply=lambda kwargs: f"you said {kwargs['messages'][-1]['content']}")
    bot = ChatBot(openai_llm(fake), system="Be brief")
    eq(bot.send("hi"), "you said hi")
    eq(fake.calls[0]["model"], MODEL)
    eq(fake.calls[0]["messages"], [_m("system", "Be brief"), _m("user", "hi")])
    bot.send("bye")
    eq(len(fake.calls[1]["messages"]), 4)  # system + u + a + u: memory works!


def live_chat():
    from openai import OpenAI

    bot = ChatBot(openai_llm(OpenAI()), system="You are a friendly Python tutor. Keep answers short.")
    print("Chat with the model. Type 'reset' to clear memory, 'quit' to exit.")
    while True:
        text = input("You: ").strip()
        if text == "quit":
            break
        if text == "reset":
            bot.reset()
            print("(memory cleared)")
            continue
        print("AI:", bot.send(text))


if __name__ == "__main__":
    if "--live" in sys.argv:
        live_chat()
    else:
        run(globals())
