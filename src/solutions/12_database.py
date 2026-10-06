# Solutions for 12_database.py
# Test them with:  uv run python src/12_database.py --solution
import sqlite3


def create_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  TEXT NOT NULL,
            role        TEXT NOT NULL,
            content     TEXT NOT NULL,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)


def save_message(conn: sqlite3.Connection, session_id: str, role: str, content: str) -> int:
    with conn:  # commits automatically
        cursor = conn.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content),
        )
    return cursor.lastrowid


def get_history(conn: sqlite3.Connection, session_id: str, limit: int | None = None) -> list[dict]:
    rows = conn.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id",
        (session_id,),
    ).fetchall()
    if limit is not None:
        rows = rows[-limit:]
    history = []
    for role, content in rows:
        history.append({"role": role, "content": content})
    return history


def count_by_session(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute(
        "SELECT session_id, COUNT(*) FROM messages GROUP BY session_id"
    ).fetchall()
    counts = {}
    for session_id, count in rows:
        counts[session_id] = count
    return counts
