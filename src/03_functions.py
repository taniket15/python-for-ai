"""
03 — Functions
==============

THEORY (read first)
-------------------
1. `def name(param: type) -> ReturnType:`. A function without `return` returns None.
2. Type hints are NOT checked at runtime, and nothing checks them at all unless you run
   a type checker (`uvx pyright` or `uvx mypy`). TS refuses to compile; Python just runs.
3. Arguments can be passed by position OR by name, in any order:  f(1, b=2)
   Parameters after a bare `*` are KEYWORD-ONLY:  def f(a, *, verbose=False)
   That's Python's version of a TS options object:  f(a, { verbose: true })
4. *args collects extra positional args into a tuple   (JS rest params ...args)
   **kwargs collects extra named args into a dict
   At the call site, `*` and `**` spread:  f(*my_list), f(**my_dict)   (JS f(...arr))
5. ⚠️ MUTABLE DEFAULT GOTCHA: defaults are evaluated ONCE, when `def` runs.
       def add(x, items=[]):   # this ONE list is shared by every call!
   Use None and create the list inside the function. (JS re-evaluates defaults per call.)
6. Functions are first-class values. `lambda x: x * 2` is a single-expression arrow
   function (x => x * 2). There are no multi-line lambdas; write a `def` instead.
7. Scope: there is NO block scope. A variable assigned inside an `if` or `for` is still
   visible after it in the same function (like `var`, not `let`). Closures work like JS,
   but to REASSIGN an outer variable from an inner function you need `nonlocal x`.
8. Decorators: `@decorator` above a def means  fn = decorator(fn), a higher-order
   function that wraps another one. FastAPI routes (@app.get) and LLM tool helpers
   use them everywhere.
9. Generators: a function containing `yield` returns a lazy iterator (JS function* / yield).
   This is how you stream LLM tokens and process huge files without loading them all.
10. Docstrings: a string on the first line of a function documents it (like JSDoc).

TS / JS  ->  Python
-------------------
    function f(a: number, b = 2): number    def f(a: int, b: int = 2) -> int:
    const double = (x) => x * 2             double = lambda x: x * 2
    function f(...args) {}                  def f(*args):
    function f(a, { verbose = false } = {}) def f(a, *, verbose=False):
    f(...arr)                               f(*arr)
    f({ ...opts })                          f(**opts)
    function* gen() { yield 1 }             def gen(): yield 1
    /** docs */                             a "triple-quoted" string on the first line

WHY THIS MATTERS FOR AI
-----------------------
Prompt templates take **kwargs. Cosine similarity is how embedding search ranks
documents. Decorators wrap LLM calls with logging, retries and caching. Generators
stream model output token by token.

Run:  uv run python src/03_functions.py
"""
import inspect
import math

from _check import eq, raises, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Fill a prompt template with any number of named variables.
#
#   render_prompt("Translate {text} to {lang}", text="hi", lang="French")
#     -> "Translate hi to French"
#
# Hint: str.format(**variables)
def render_prompt(template: str, **variables: str) -> str:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# Append {"role": role, "content": content} to `history` and return the history.
# If no history is passed, start a NEW list. Two calls without a history must NOT
# share the same list (avoid the mutable-default gotcha: default to None!).
#
#   add_message("hi")                      -> [{"role": "user", "content": "hi"}]
#   add_message("yo", role="assistant", history=h)   # appends to h and returns h
def add_message(content: str, role: str = "user", history: list[dict] | None = None) -> list[dict]:
    raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# Cosine similarity between two vectors (this is how embedding search works):
#     dot(a, b) / (|a| * |b|)     where |a| = sqrt(sum of squares)
# Raise ValueError if the lengths differ. Return 0.0 if either vector is all zeros.
#
#   cosine_similarity([1, 0], [0, 1])  ->  0.0
#   cosine_similarity([1, 1], [2, 2])  ->  1.0  (same direction)
#
# Hint: sum(x * y for x, y in zip(a, b)) and math.sqrt
def cosine_similarity(a: list[float], b: list[float]) -> float:
    raise NotImplementedError  # TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# Write a DECORATOR `count_calls(fn)` that returns a wrapper function which:
#   - calls fn with all the same arguments (*args, **kwargs) and returns its result
#   - counts how many times it was called, in `wrapper.calls` (starts at 0)
#
#   @count_calls
#   def add(a, b): return a + b
#   add(1, 2); add(3, 4)
#   add.calls  -> 2
#
# Hint: functions are objects, so you can set attributes on them: wrapper.calls = 0
# Bonus: decorate the wrapper with @functools.wraps(fn) so it keeps fn's name/docstring.
def count_calls(fn):
    raise NotImplementedError  # TODO


# Q5 ─────────────────────────────────────────────────────────────────────────────
# A GENERATOR that yields `text` in pieces of `size` characters (like a token stream).
#
#   list(stream_chunks("abcdefg", 3))  ->  ["abc", "def", "g"]
#
# It must use `yield` (the test checks it's a generator, not a list).
def stream_chunks(text: str, size: int):
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_render_prompt():
    eq(render_prompt("Translate {text} to {lang}", text="hi", lang="French"), "Translate hi to French")
    eq(render_prompt("No variables"), "No variables")


def test_q2_add_message():
    h1 = add_message("a")
    h2 = add_message("b")
    eq(h2, [{"role": "user", "content": "b"}])  # fails if the default list is shared
    eq(h1, [{"role": "user", "content": "a"}])
    returned = add_message("yo", role="assistant", history=h1)
    assert returned is h1, "should append to and return the history you passed in"
    eq(len(h1), 2)


def test_q3_cosine_similarity():
    eq(round(cosine_similarity([1, 0], [0, 1]), 6), 0.0)
    eq(round(cosine_similarity([1, 1], [2, 2]), 6), 1.0)
    eq(round(cosine_similarity([1, 2, 3], [-1, -2, -3]), 6), -1.0)
    eq(cosine_similarity([0, 0], [1, 1]), 0.0)
    raises(ValueError, cosine_similarity, [1, 2], [1])


def test_q4_count_calls():
    def add(a, b=0):
        return a + b

    wrapped = count_calls(add)
    eq(wrapped.calls, 0)
    eq(wrapped(1, b=2), 3)
    eq(wrapped(5), 5)
    eq(wrapped.calls, 2)


def test_q5_stream_chunks():
    gen = stream_chunks("abcdefg", 3)
    assert inspect.isgenerator(gen), "use `yield` so this is a generator"
    eq(list(gen), ["abc", "def", "g"])
    eq(list(stream_chunks("", 3)), [])


if __name__ == "__main__":
    run(globals())
