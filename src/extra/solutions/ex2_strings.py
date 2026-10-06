# Solutions for ex2_strings.py
# Test them with:  uv run python src/extra/ex2_strings.py --solution


def reverse_words(sentence: str) -> str:
    words = sentence.split()
    return " ".join(words[::-1])


def is_palindrome(text: str) -> bool:
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]
