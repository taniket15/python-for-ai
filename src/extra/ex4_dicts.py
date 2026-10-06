"""
Extra 4 — Dictionaries (Python's plain objects / Map)
=====================================================
An optional warm-up for complete Python beginners.

TS / JS  ->  Python
-------------------
    const counts: Record<string, number> = {}     counts = {}
    counts[w] = (counts[w] ?? 0) + 1              counts[w] = counts.get(w, 0) + 1
    for (const [k, v] of Object.entries(obj))     for k, v in d.items():
    obj.missing   -> undefined                    d["missing"]  -> raises KeyError!

Run:  uv run python src/extra/ex4_dicts.py
"""
from _check import eq, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Count how many times each word appears. Make it case-insensitive.
#
#   word_count("the cat and the hat")  ->  {"the": 2, "cat": 1, "and": 1, "hat": 1}
def word_count(text: str) -> dict[str, int]:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# Return the single most frequent word. Reuse word_count().
#
#   most_common("a b b c c c")  ->  "c"
#
# Hint: loop over counts.items() and remember the best word so far.
def most_common(text: str) -> str:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_word_count():
    eq(word_count("the cat and the hat"), {"the": 2, "cat": 1, "and": 1, "hat": 1})
    eq(word_count("Hi hi HI"), {"hi": 3})


def test_q2_most_common():
    eq(most_common("a b b c c c"), "c")
    eq(most_common("Python python java"), "python")


if __name__ == "__main__":
    run(globals())
