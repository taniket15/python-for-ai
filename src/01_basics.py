"""
01 — Data types, Lists, For loops
=================================

THEORY (read first)
-------------------
1. Python is dynamically typed but STRONGLY typed: it won't silently coerce.
       "1" + 1        # TypeError   (JS gives "11")
       "1" + str(1)   # "11"
       int("1") + 1   # 2
2. Numbers: `int` (unlimited size, no 2^53 limit) and `float` are separate types.
       7 / 2   -> 3.5   (always a float)
       7 // 2  -> 3     (floor division, JS: Math.floor(7 / 2))
       7 % 2   -> 1,    2 ** 10 -> 1024
3. Truthiness. Falsy values: None, False, 0, 0.0, "", [], {}, set()
   ⚠️ An EMPTY LIST IS FALSY in Python (in JS `[]` is truthy). `if items:` means "if not empty".
4. `None` replaces both `null` and `undefined`. Check for it with `is`:  `if x is None:`
   `==` compares VALUES:  [1, 2] == [1, 2]  -> True   (JS === would be false for arrays)
   `is` compares IDENTITY (same object in memory, like JS === on objects).
5. Mutable vs immutable: list / dict / set are mutable; int / float / str / tuple are not.
   Assigning a list does NOT copy it (same as JS): `b = a` -> both names point to one list.
   Copy with `a.copy()` or `a[:]`   (JS: [...a]).
6. Indexing & slicing: `xs[start:stop:step]`, stop is exclusive, negatives count from the end.
       xs[-1]    -> last item          (JS: xs.at(-1))
       xs[1:3]   -> items 1 and 2      (JS: xs.slice(1, 3))
       xs[::-1]  -> reversed copy
   Indexing past the end RAISES IndexError (JS returns undefined). Slicing never raises.
7. Loops: there is no C-style `for (;;)`. You loop over iterables.
       for x in xs:                 # for (const x of xs)
       for i in range(5):           # 0..4
       for i, x in enumerate(xs):   # xs.forEach((x, i) => ...)
       for a, b in zip(xs, ys):     # walk two lists side by side
   `while cond:` exists, plus `break` / `continue`. There is no `do...while`.
8. Naming: snake_case for variables and functions, PascalCase for classes,
   UPPER_CASE for constants. Blocks use a colon plus 4-space indentation, no braces.

TS / JS  ->  Python
-------------------
    const xs: number[] = [1, 2]      xs: list[int] = [1, 2]
    xs.push(3)                       xs.append(3)
    xs.length                        len(xs)
    xs.includes(2)                   2 in xs
    xs.map(x => x * 2)               [x * 2 for x in xs]
    xs.filter(x => x > 1)            [x for x in xs if x > 1]
    xs.sort((a, b) => a - b)         xs.sort()   /   sorted(xs)   (sorted returns a NEW list)
    Math.max(...xs)                  max(xs)
    xs.reduce((a, b) => a + b, 0)    sum(xs)
    s.trim() / s.toLowerCase()       s.strip() / s.lower()
    `Hi ${name}`                     f"Hi {name}"
    typeof x === "string"            isinstance(x, str)
    &&  ||  !                        and  or  not

WHY THIS MATTERS FOR AI
-----------------------
Before text reaches an LLM or an embedding model, you clean it, split it into chunks, and
rank the results. Chunking with overlap (Q2) is how RAG pipelines split documents, and
ranking by score (Q3) is how you pick the best search hits.

Run:  uv run python src/01_basics.py
"""
from _check import eq, raises, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Write `clean_tokens(text)`:
#   - lowercase the text
#   - split it into words on whitespace
#   - strip the characters  . , ! ? : ;  from the START and END of each word
#   - drop words that end up empty
#
#   clean_tokens("Hello, World!!  AI is fun.")  ->  ["hello", "world", "ai", "is", "fun"]
#
# Hint: str.strip() accepts the characters to remove:  "!!hi?".strip("!?")  ->  "hi"
def clean_tokens(text: str) -> list[str]:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# RAG-style chunking. Split a list of words into chunks of `size` words, where each
# chunk shares `overlap` words with the previous one. Stop once a chunk reaches the end.
# Raise ValueError if overlap >= size (that would never move forward).
#
#   chunk_words(list("abcdefg"), size=3, overlap=1)
#     -> [["a","b","c"], ["c","d","e"], ["e","f","g"]]
#
# Hint: range(start, stop, step). What is the step between the start of each chunk?
def chunk_words(words: list[str], size: int, overlap: int) -> list[list[str]]:
    raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# Given similarity scores for documents, return the INDICES of the k highest scores,
# best first.
#
#   top_k([0.1, 0.9, 0.4, 0.7], k=2)  ->  [1, 3]
#
# Hint: sorted(iterable, key=..., reverse=True). Unlike the JS .sort() comparator,
# `key` returns the value to sort BY:  key=lambda i: scores[i]
def top_k(scores: list[float], k: int) -> list[int]:
    raise NotImplementedError  # TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# Return the average length (in characters) of the texts, as a float.
# Return 0.0 for an empty list. (Use truthiness:  `if not texts:`)
#
#   average_length(["hi", "hello"])  ->  3.5
def average_length(texts: list[str]) -> float:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_clean_tokens():
    eq(clean_tokens("Hello, World!!  AI is fun."), ["hello", "world", "ai", "is", "fun"])
    eq(clean_tokens("  ...  "), [])
    eq(clean_tokens(""), [])


def test_q2_chunk_words():
    eq(chunk_words(list("abcdefg"), 3, 1), [list("abc"), list("cde"), list("efg")])
    eq(chunk_words(list("abcdef"), 3, 1), [list("abc"), list("cde"), list("ef")])
    eq(chunk_words(list("ab"), 5, 2), [list("ab")])
    eq(chunk_words([], 3, 1), [])
    raises(ValueError, chunk_words, list("abc"), 2, 2)


def test_q3_top_k():
    eq(top_k([0.1, 0.9, 0.4, 0.7], 2), [1, 3])
    eq(top_k([0.5], 3), [0])
    eq(top_k([], 2), [])


def test_q4_average_length():
    eq(average_length(["hi", "hello"]), 3.5)
    eq(average_length([]), 0.0)


if __name__ == "__main__":
    run(globals())
