# Solutions for 09_files.py
# Test them with:  uv run python src/09_files.py --solution
import json
from pathlib import Path


def save_jsonl(records: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_jsonl(path: Path) -> list[dict]:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_documents(folder: Path) -> dict[str, str]:
    documents = {}
    for file in sorted(folder.glob("*.txt")):
        documents[file.stem] = file.read_text(encoding="utf-8").strip()
    return documents


def append_log(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
