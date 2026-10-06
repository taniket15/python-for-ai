"""
Extra 2 — Strings (slicing, split/join, methods)
================================================
An optional warm-up for complete Python beginners.

TS / JS  ->  Python
-------------------
    s.split(" ")                  s.split()     (no argument = split on any whitespace)
    arr.join(" ")                 " ".join(lst)  (join is called on the SEPARATOR)
    [...arr].reverse()            lst[::-1]      (a reversed copy, works on strings too!)
    s.toLowerCase()               s.lower()
    s.replaceAll(" ", "")         s.replace(" ", "")
    true / false                  True / False   (capitalized)

Run:  uv run python src/extra/ex2_strings.py
"""
from _check import eq, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Reverse the order of the words in a sentence.
#
#   reverse_words("hello world python")  ->  "python world hello"
def reverse_words(sentence: str) -> str:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# Return True if the text reads the same backwards. Ignore upper/lower case and spaces.
#
#   is_palindrome("Race car")  ->  True
def is_palindrome(text: str) -> bool:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_reverse_words():
    eq(reverse_words("hello world python"), "python world hello")
    eq(reverse_words("one"), "one")


def test_q2_is_palindrome():
    eq(is_palindrome("Race car"), True)
    eq(is_palindrome("hello"), False)


if __name__ == "__main__":
    run(globals())
