"""
09 — File Handling
==================

THEORY (read first)
-------------------
1. open(path, mode, encoding="utf-8")
       "r" read (default)   "w" write (OVERWRITES)   "a" append   "x" create, fail if exists
       add "b" for bytes:   "rb", "wb"  (images, PDFs, audio)
   ⚠️ Always pass encoding="utf-8" for text. The default depends on the OS.
2. `with open(...) as f:` closes the file automatically, even if an error happens.
   That's a "context manager", the same idea as try/finally (or `using` in TS 5.2).
3. Reading:  f.read() -> the whole file as one str
             for line in f:  -> lazily, line by line (memory-friendly for huge datasets)
   Each line keeps its trailing "\n", so use line.strip() / line.rstrip("\n").
4. Python file I/O is synchronous (like Node's fs.readFileSync), with no promises.
5. pathlib.Path is the modern API (Node's `path` and `fs` rolled into one):
       p = Path("data") / "notes.txt"         # join paths with `/`!
       p.read_text(encoding="utf-8")          p.write_text(text, encoding="utf-8")
       p.exists()   p.name   p.stem   p.suffix   p.parent
       p.glob("*.txt")                        # files matching a pattern
       p.mkdir(parents=True, exist_ok=True)   # mkdir -p
6. json:  json.loads(s) / json.dumps(obj)    ≈ JSON.parse / JSON.stringify
          json.load(f) / json.dump(obj, f)   (read from / write to a file object)
          json.dumps(obj, ensure_ascii=False, indent=2)  keeps "café" readable, pretty-printed
7. JSONL (one JSON object per line) is THE format for AI datasets: fine-tuning data,
   eval results and batch-API inputs. You can append to it and stream it line by line.
8. Relative paths resolve against the CURRENT WORKING DIRECTORY, not the script's folder.
   For script-relative paths use Path(__file__).parent (Node's __dirname).
9. Also good to know: the `csv` module (csv.DictReader), and pandas for tables.

TS / JS  ->  Python
-------------------
    fs.readFileSync(p, "utf8")          Path(p).read_text(encoding="utf-8")
    fs.writeFileSync(p, s)              Path(p).write_text(s, encoding="utf-8")
    fs.appendFileSync(p, s)             with open(p, "a", encoding="utf-8") as f: f.write(s)
    path.join(a, b)                     Path(a) / b
    path.basename(p, ".txt")            Path(p).stem
    fs.existsSync(p)                    Path(p).exists()
    fs.mkdirSync(p, { recursive: true })    Path(p).mkdir(parents=True, exist_ok=True)
    __dirname                           Path(__file__).parent

Run:  uv run python src/09_files.py
"""
import tempfile
from pathlib import Path

from _check import eq, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Write `records` to `path` as JSONL: one json.dumps(record, ensure_ascii=False) per line.
# Create the parent folder if it doesn't exist.
def save_jsonl(records: list[dict], path: Path) -> None:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# Read a JSONL file back into a list of dicts. Skip blank lines.
# Read it line by line with `for line in f:` (don't load the whole file at once).
def load_jsonl(path: Path) -> list[dict]:
    raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# Load every .txt file in `folder` (not other extensions) into a dict of
#   {file stem: stripped text}
# This is the first step of any "chat with your documents" app.
#
#   folder/a.txt ("  Alpha \n"), folder/b.txt ("Beta"), folder/notes.md
#     -> {"a": "Alpha", "b": "Beta"}
def load_documents(folder: Path) -> dict[str, str]:
    raise NotImplementedError  # TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# Append `line` + "\n" to a log file, creating the parent folders if needed.
# Calling it twice must keep both lines (hint: mode "a").
def append_log(path: Path, line: str) -> None:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
RECORDS = [{"prompt": "Hi", "label": "greeting"}, {"prompt": "Un café, s'il vous plaît", "label": "order"}]


def test_q1_save_jsonl():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "sub" / "data.jsonl"
        save_jsonl(RECORDS, path)
        text = path.read_text(encoding="utf-8")
        eq(len(text.strip().splitlines()), 2)  # one line per record
        assert "café" in text, "use ensure_ascii=False"


def test_q2_load_jsonl():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "data.jsonl"
        path.write_text('{"a": 1}\n\n{"a": 2}\n', encoding="utf-8")
        eq(load_jsonl(path), [{"a": 1}, {"a": 2}])
        save_jsonl(RECORDS, path)
        eq(load_jsonl(path), RECORDS)  # round trip


def test_q3_load_documents():
    with tempfile.TemporaryDirectory() as d:
        folder = Path(d)
        (folder / "a.txt").write_text("  Alpha \n", encoding="utf-8")
        (folder / "b.txt").write_text("Beta", encoding="utf-8")
        (folder / "notes.md").write_text("ignore me", encoding="utf-8")
        eq(load_documents(folder), {"a": "Alpha", "b": "Beta"})


def test_q4_append_log():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "logs" / "app.log"
        append_log(path, "first")
        append_log(path, "second")
        eq(path.read_text(encoding="utf-8"), "first\nsecond\n")


if __name__ == "__main__":
    run(globals())
