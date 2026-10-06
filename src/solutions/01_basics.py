# Solutions for 01_basics.py
# Test them with:  uv run python src/01_basics.py --solution


def clean_tokens(text: str) -> list[str]:
    tokens = []
    for word in text.lower().split():
        word = word.strip(".,!?:;")
        if word:  # skip empty strings
            tokens.append(word)
    return tokens


def chunk_words(words: list[str], size: int, overlap: int) -> list[list[str]]:
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    step = size - overlap
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(words[start:start + size])
        if start + size >= len(words):  # this chunk reached the end
            break
    return chunks


def top_k(scores: list[float], k: int) -> list[int]:
    indices = list(range(len(scores)))
    indices.sort(key=lambda i: scores[i], reverse=True)
    return indices[:k]


def average_length(texts: list[str]) -> float:
    if not texts:
        return 0.0
    total = 0
    for text in texts:
        total += len(text)
    return total / len(texts)
