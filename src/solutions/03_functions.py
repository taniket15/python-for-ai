# Solutions for 03_functions.py
# Test them with:  uv run python src/03_functions.py --solution
import math


def render_prompt(template: str, **variables: str) -> str:
    return template.format(**variables)


def add_message(content: str, role: str = "user", history: list[dict] | None = None) -> list[dict]:
    if history is None:
        history = []  # a fresh list on every call
    history.append({"role": role, "content": content})
    return history


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    dot = 0
    for x, y in zip(a, b):
        dot += x * y
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    if length_a == 0 or length_b == 0:
        return 0.0
    return dot / (length_a * length_b)


def count_calls(fn):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return fn(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def stream_chunks(text: str, size: int):
    for start in range(0, len(text), size):
        yield text[start:start + size]
