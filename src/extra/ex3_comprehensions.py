"""
Extra 3 — List & dict comprehensions (Python's map/filter)
==========================================================
An optional warm-up for complete Python beginners.

A list comprehension builds a list in one line:
    [<expression> for <item> in <iterable> if <condition>]

TS / JS  ->  Python
-------------------
    nums.filter(n => n % 2 === 0)          [n for n in nums if n % 2 == 0]
        .map(n => n * n)                   [n * n for n in nums if n % 2 == 0]
    Object.fromEntries(words.map(          {w: len(w) for w in words}
      w => [w, w.length]))
    s.length                               len(s)

Run:  uv run python src/extra/ex3_comprehensions.py
"""
from _check import eq, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Return the squares of only the even numbers, in their original order.
# Try to do it in ONE line with a list comprehension.
#
#   squares_of_evens([1, 2, 3, 4, 5, 6])  ->  [4, 16, 36]
def squares_of_evens(nums: list[int]) -> list[int]:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# Return a dict of word -> length, using a dict comprehension.
#
#   lengths(["hi", "hello"])  ->  {"hi": 2, "hello": 5}
def lengths(words: list[str]) -> dict[str, int]:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_squares_of_evens():
    eq(squares_of_evens([1, 2, 3, 4, 5, 6]), [4, 16, 36])
    eq(squares_of_evens([1, 3, 5]), [])


def test_q2_lengths():
    eq(lengths(["hi", "hello"]), {"hi": 2, "hello": 5})
    eq(lengths([]), {})


if __name__ == "__main__":
    run(globals())
