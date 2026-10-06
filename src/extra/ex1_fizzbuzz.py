"""
Extra 1 — FizzBuzz (loops, range, if/elif/else)
===============================================
An optional warm-up for complete Python beginners. Do these before src/01_basics.py.

TS / JS  ->  Python
-------------------
    for (let i = 1; i <= n; i++)     for i in range(1, n + 1):
    else if                          elif
    arr.push(x)                      lst.append(x)
    String(i)                        str(i)     (or an f-string: f"{i}")
    ===   &&   ||   !                ==   and   or   not
    { ... }  blocks                  a colon + 4 spaces of indentation

Run:  uv run python src/extra/ex1_fizzbuzz.py
"""
from _check import eq, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Return a LIST of strings for the numbers 1..n (inclusive):
#   "Fizz" if divisible by 3, "Buzz" if divisible by 5, "FizzBuzz" if divisible by both,
#   otherwise the number as a string, e.g. "7"
#
#   fizzbuzz(5)  ->  ["1", "2", "Fizz", "4", "Buzz"]
def fizzbuzz(n: int) -> list[str]:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_fizzbuzz():
    eq(fizzbuzz(5), ["1", "2", "Fizz", "4", "Buzz"])
    eq(fizzbuzz(15)[-1], "FizzBuzz")
    eq(fizzbuzz(0), [])


if __name__ == "__main__":
    run(globals())
