"""L2 Memory — SQLite Session, one Patient, max_turns=6. Not AI."""

from __future__ import annotations

import json
import sqlite3
from typing import Any

from agent.config import MAX_TURNS, session_db_path
from agent.redact import redact_obj, redact_text


def _connect() -> sqlite3.Connection:
    path = session_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            member_id TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS turns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT,
            prompt TEXT,
            response TEXT,
            status TEXT
        )
        """
    )
    return conn


def load(session_id: str) -> dict[str, Any]:
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT member_id FROM sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        turns = conn.execute(
            """
            SELECT role, prompt, response, status
            FROM turns WHERE session_id = ?
            ORDER BY id DESC LIMIT ?
            """,
            (session_id, MAX_TURNS),
        ).fetchall()
        history = [
            {"role": t[0], "prompt": t[1], "response": t[2], "status": t[3]}
            for t in reversed(turns)
        ]
        return {"session_id": session_id, "member_id": row[0] if row else None, "turns": history}
    finally:
        conn.close()


def store(
    session_id: str,
    *,
    member_id: str | None,
    role: str,
    prompt: str,
    response: dict[str, Any],
    status: str,
) -> None:
    conn = _connect()
    try:
        existing = conn.execute(
            "SELECT member_id FROM sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if existing is None:
            conn.execute(
                "INSERT INTO sessions (session_id, member_id) VALUES (?, ?)",
                (session_id, member_id),
            )
        elif not existing[0] and member_id:
            conn.execute(
                "UPDATE sessions SET member_id = ? WHERE session_id = ?",
                (member_id, session_id),
            )
        conn.execute(
            """
            INSERT INTO turns (session_id, role, prompt, response, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session_id,
                role,
                redact_text(prompt),
                json.dumps(redact_obj(response), default=str),
                status,
            ),
        )
        ids = conn.execute(
            "SELECT id FROM turns WHERE session_id = ? ORDER BY id DESC",
            (session_id,),
        ).fetchall()
        extra = ids[MAX_TURNS:]
        if extra:
            conn.executemany(
                "DELETE FROM turns WHERE id = ?",
                [(row[0],) for row in extra],
            )
        conn.commit()
    finally:
        conn.close()
