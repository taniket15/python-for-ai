"""
12 — Database Interactions (SQLite)
===================================

THEORY (read first)
-------------------
1. `sqlite3` is BUILT IN: no install, no server. The database is a single file (or
   ":memory:"). It's great for prototypes, local chat memory and storing eval results.
   In production you'd use Postgres (psycopg), often with pgvector for embeddings.
2. Basics:
       conn = sqlite3.connect("app.db")
       cur = conn.execute("SELECT ...", params)    # returns a cursor
       conn.commit()                               # save changes
       conn.close()
3. ⚠️ ALWAYS use placeholders, NEVER f-strings, for values:
       conn.execute("SELECT * FROM messages WHERE id = ?", (msg_id,))
   Note the 1-tuple (msg_id,), the trailing comma makes it a tuple!
   An f-string here is a SQL injection hole.
4. `with conn:` is a TRANSACTION: it commits on success and rolls back if an exception
   happens. (It does NOT close the connection.)
5. cur.fetchone() -> one row or None;  cur.fetchall() -> a list of rows.
   Rows are tuples by default. Set conn.row_factory = sqlite3.Row to read them by
   column name: row["content"].
6. cur.lastrowid -> the id of the row you just inserted.
7. ORMs: SQLAlchemy, or SQLModel (by FastAPI's author, built on Pydantic)
   ≈ Prisma / TypeORM / Drizzle.
8. Vector databases (pgvector, Chroma, Qdrant, Pinecone) store embeddings for semantic
   search. Same ideas (insert, query), except you query by SIMILARITY instead of equality.

TS / JS (better-sqlite3)  ->  Python (sqlite3)
----------------------------------------------
    const db = new Database("app.db")              conn = sqlite3.connect("app.db")
    db.prepare("... WHERE id = ?").get(id)         conn.execute("... WHERE id = ?", (id,)).fetchone()
    db.prepare("...").all()                        conn.execute("...").fetchall()
    db.transaction(() => { ... })()                with conn: ...
    info.lastInsertRowid                           cur.lastrowid

Run:  uv run python src/12_database.py
"""
import sqlite3

from _check import eq, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Create a `messages` table (only if it doesn't already exist) with these columns:
#   id          INTEGER PRIMARY KEY AUTOINCREMENT
#   session_id  TEXT NOT NULL
#   role        TEXT NOT NULL
#   content     TEXT NOT NULL
#   created_at  TEXT DEFAULT CURRENT_TIMESTAMP
# Calling it twice must not fail (CREATE TABLE IF NOT EXISTS).
def create_schema(conn: sqlite3.Connection) -> None:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# Insert a message using ? placeholders, commit (use `with conn:`), and return the new id.
def save_message(conn: sqlite3.Connection, session_id: str, role: str, content: str) -> int:
    raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# Return a session's messages as [{"role": ..., "content": ...}] in the order they were
# saved (ORDER BY id). If `limit` is given, return only the LAST `limit` messages,
# still in chronological order. This is exactly what you'd send back to the LLM.
#
# Hint: the simplest way is to fetch them all and slice in Python (rows[-limit:]).
#       Bonus: do it in SQL with ORDER BY id DESC LIMIT ? inside a subquery.
def get_history(conn: sqlite3.Connection, session_id: str, limit: int | None = None) -> list[dict]:
    raise NotImplementedError  # TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# Return {session_id: number_of_messages} for every session.
# Hint: SELECT session_id, COUNT(*) FROM messages GROUP BY session_id
def count_by_session(conn: sqlite3.Connection) -> dict[str, int]:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def fresh_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    return conn


def test_q1_create_schema():
    conn = fresh_db()
    create_schema(conn)  # second call must not fail
    columns = [row[1] for row in conn.execute("PRAGMA table_info(messages)")]
    eq(columns, ["id", "session_id", "role", "content", "created_at"])


def test_q2_save_message():
    conn = fresh_db()
    eq(save_message(conn, "s1", "user", "hi"), 1)
    eq(save_message(conn, "s1", "assistant", "hello"), 2)
    evil = "x'); DROP TABLE messages; --"
    save_message(conn, "s1", "user", evil)
    row = conn.execute("SELECT content FROM messages WHERE id = 3").fetchone()
    eq(row[0], evil)  # stored as plain text, table still exists


def test_q3_get_history():
    conn = fresh_db()
    for i, role in enumerate(["user", "assistant", "user", "assistant"]):
        save_message(conn, "s1", role, f"m{i}")
    save_message(conn, "other", "user", "not mine")
    eq(get_history(conn, "s1"), [
        {"role": "user", "content": "m0"},
        {"role": "assistant", "content": "m1"},
        {"role": "user", "content": "m2"},
        {"role": "assistant", "content": "m3"},
    ])
    eq(get_history(conn, "s1", limit=2), [{"role": "user", "content": "m2"}, {"role": "assistant", "content": "m3"}])
    eq(get_history(conn, "nobody"), [])


def test_q4_count_by_session():
    conn = fresh_db()
    for sid in ["a", "a", "b", "a", "c"]:
        save_message(conn, sid, "user", "x")
    eq(count_by_session(conn), {"a": 3, "b": 1, "c": 1})


if __name__ == "__main__":
    run(globals())
