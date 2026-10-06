"""
02 — Dicts, Tuples (and Sets)
=============================

THEORY (read first)
-------------------
1. dict is Python's object / Map, rolled into one.
   - Keys can be any HASHABLE value: str, int, tuple... but NOT a list.
   - Insertion order is preserved (guaranteed since Python 3.7).
   - d["k"] RAISES KeyError when the key is missing (no `undefined`).
     d.get("k") returns None; d.get("k", 0) returns a default.
   - "k" in d checks KEYS.     There is no dot access: d["name"], never d.name
   - Merge: {**a, **b} or a | b      (JS {...a, ...b})
   - Loop:  for k in d / for k, v in d.items()
   - Delete: del d["k"], or d.pop("k", None) if it might be missing
2. tuple: an immutable, fixed-length sequence:  point = (3, 4)
   - Similar to a TS tuple [number, number], but truly read-only at runtime.
   - A one-item tuple needs a trailing comma: (1,)
   - Tuples are hashable, so they can be dict keys:  cache[(model, prompt)] = answer
3. Unpacking (destructuring):
       x, y = point               # const [x, y] = point
       a, b = b, a                # swap without a temp variable
       first, *rest = items       # const [first, ...rest] = items
       for text, label in pairs:  # destructure inside a for loop
   Functions return several values by returning a tuple:  return low, high
4. set: unique values, {1, 2, 3}. Empty set is set() because {} is an empty dict!
   a | b union, a & b intersection, a - b difference.
5. Handy helpers in `collections`:
       Counter(["a", "b", "a"])  -> Counter({"a": 2, "b": 1});  .most_common(n)
       defaultdict(list)         -> a missing key auto-creates an empty list
6. Sorting with tuple keys: tuples compare item by item, so
       sorted(items, key=lambda x: (-x[1], x[0]))
   sorts by count descending, then by name ascending.

TS / JS  ->  Python
-------------------
    const o = { a: 1 }                    o = {"a": 1}
    o.a   /   o["a"]                      o["a"]
    o.a ?? 0                              o.get("a", 0)
    "a" in o   /   map.has("a")           "a" in o
    Object.keys / values / entries        o.keys() / o.values() / o.items()
    {...a, ...b}                          {**a, **b}    or    a | b
    delete o.a                            del o["a"]
    const [x, y] = pair                   x, y = pair
    new Set([1, 2])                       {1, 2}    or    set([1, 2])
    JSON from an API                      is just a dict / list in Python

WHY THIS MATTERS FOR AI
-----------------------
Every chat message is a dict: {"role": "user", "content": "..."}. API JSON responses parse
into dicts. Labelled datasets are lists of (text, label) tuples. Request options are dicts
merged from defaults and overrides.

Run:  uv run python src/02_dicts_tuples.py
"""
from _check import eq, raises, run

ALLOWED_ROLES = {"system", "user", "assistant"}  # a set


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Return a chat message dict. Strip whitespace from the content.
# Raise ValueError if `role` is not in ALLOWED_ROLES.
#
#   make_message("user", "  hi ")  ->  {"role": "user", "content": "hi"}
def make_message(role: str, content: str) -> dict[str, str]:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# Group example texts by their label.
#
#   group_by_label([("great!", "pos"), ("awful", "neg"), ("nice", "pos")])
#     -> {"pos": ["great!", "nice"], "neg": ["awful"]}
#
# Hint: `for text, label in examples:` and then d.setdefault(label, []).append(text)
#       (or use collections.defaultdict(list))
def group_by_label(examples: list[tuple[str, str]]) -> dict[str, list[str]]:
    raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# Merge request options. Return a NEW dict: `defaults` updated with `overrides`,
# but SKIP any override whose value is None. Don't modify either input dict.
#
#   merge_config({"model": "m1", "max_tokens": 1024}, {"max_tokens": 256, "user": None})
#     -> {"model": "m1", "max_tokens": 256}
#
# Hint: a dict comprehension {k: v for k, v in d.items() if ...} plus {**a, **b}
def merge_config(defaults: dict, overrides: dict) -> dict:
    raise NotImplementedError  # TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# Count how many examples each label has. Return a list of (label, count) TUPLES,
# sorted by count (highest first); break ties alphabetically by label.
#
#   label_counts([("a", "pos"), ("b", "neg"), ("c", "pos"), ("d", "neu"), ("e", "neg")])
#     -> [("neg", 2), ("pos", 2), ("neu", 1)]
#
# Hint: collections.Counter, then sorted(..., key=lambda pair: (-pair[1], pair[0]))
def label_counts(examples: list[tuple[str, str]]) -> list[tuple[str, int]]:
    raise NotImplementedError  # TODO


# Q5 ─────────────────────────────────────────────────────────────────────────────
# Return the (min, max) of a list of numbers as a tuple, in ONE pass with a for loop
# (don't use min()/max()). Raise ValueError for an empty list.
#
#   low, high = min_max([3, 1, 4, 1, 5])   ->  low == 1, high == 5
def min_max(nums: list[float]) -> tuple[float, float]:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_make_message():
    eq(make_message("user", "  hi "), {"role": "user", "content": "hi"})
    eq(make_message("assistant", "ok"), {"role": "assistant", "content": "ok"})
    raises(ValueError, make_message, "admin", "x")


def test_q2_group_by_label():
    eq(group_by_label([("great!", "pos"), ("awful", "neg"), ("nice", "pos")]),
       {"pos": ["great!", "nice"], "neg": ["awful"]})
    eq(group_by_label([]), {})


def test_q3_merge_config():
    defaults = {"model": "m1", "max_tokens": 1024}
    overrides = {"max_tokens": 256, "user": None, "stream": True}
    eq(merge_config(defaults, overrides), {"model": "m1", "max_tokens": 256, "stream": True})
    eq(defaults, {"model": "m1", "max_tokens": 1024})  # unchanged
    eq(overrides, {"max_tokens": 256, "user": None, "stream": True})  # unchanged
    eq(merge_config(defaults, {"model": None}), defaults)


def test_q4_label_counts():
    examples = [("a", "pos"), ("b", "neg"), ("c", "pos"), ("d", "neu"), ("e", "neg")]
    eq(label_counts(examples), [("neg", 2), ("pos", 2), ("neu", 1)])
    eq(label_counts([]), [])


def test_q5_min_max():
    low, high = min_max([3, 1, 4, 1, 5])
    eq((low, high), (1, 5))
    eq(min_max([7]), (7, 7))
    raises(ValueError, min_max, [])


if __name__ == "__main__":
    run(globals())
