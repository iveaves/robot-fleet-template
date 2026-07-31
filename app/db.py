"""A very small SQLite helper. Rows come back as dicts."""

from __future__ import annotations

import sqlite3
from typing import Any

from app.config import DB_PATH


def connect(path: str | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def query(sql: str, params: tuple = (), path: str | None = None) -> list[dict[str, Any]]:
    with connect(path) as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def execute(sql: str, params: tuple = (), path: str | None = None) -> int:
    with connect(path) as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.rowcount
