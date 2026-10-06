# Solutions for 02_dicts_tuples.py
# Test them with:  uv run python src/02_dicts_tuples.py --solution
from collections import Counter


def make_message(role: str, content: str) -> dict[str, str]:
    if role not in ALLOWED_ROLES:
        raise ValueError(f"unknown role: {role}")
    return {"role": role, "content": content.strip()}


def group_by_label(examples: list[tuple[str, str]]) -> dict[str, list[str]]:
    groups = {}
    for text, label in examples:
        if label not in groups:
            groups[label] = []
        groups[label].append(text)
    return groups


def merge_config(defaults: dict, overrides: dict) -> dict:
    merged = dict(defaults)  # a copy, so `defaults` is not changed
    for key, value in overrides.items():
        if value is not None:
            merged[key] = value
    return merged


def label_counts(examples: list[tuple[str, str]]) -> list[tuple[str, int]]:
    counts = Counter()
    for text, label in examples:
        counts[label] += 1
    pairs = list(counts.items())
    pairs.sort(key=lambda pair: (-pair[1], pair[0]))  # count high->low, then name A->Z
    return pairs


def min_max(nums: list[float]) -> tuple[float, float]:
    if not nums:
        raise ValueError("empty list")
    low = nums[0]
    high = nums[0]
    for n in nums:
        if n < low:
            low = n
        if n > high:
            high = n
    return low, high
