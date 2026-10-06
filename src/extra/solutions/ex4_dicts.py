# Solutions for ex4_dicts.py
# Test them with:  uv run python src/extra/ex4_dicts.py --solution


def word_count(text: str) -> dict[str, int]:
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def most_common(text: str) -> str:
    counts = word_count(text)
    best_word = ""
    best_count = 0
    for word, count in counts.items():
        if count > best_count:
            best_word = word
            best_count = count
    return best_word
