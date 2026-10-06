# Solutions for ex3_comprehensions.py
# Test them with:  uv run python src/extra/ex3_comprehensions.py --solution


def squares_of_evens(nums: list[int]) -> list[int]:
    return [n * n for n in nums if n % 2 == 0]


def lengths(words: list[str]) -> dict[str, int]:
    return {word: len(word) for word in words}
