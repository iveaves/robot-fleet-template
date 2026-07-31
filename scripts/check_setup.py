"""Confirm everything works before the interview. Takes about five seconds.

    python3 scripts/check_setup.py

Checks your Python, your dependencies, the database, and that your API key
reaches the fleet. If all five pass you are ready and there is nothing else to
prepare.
"""

from __future__ import annotations

import os
import sqlite3
import sys

OK = "  ok   "
BAD = " FAIL  "
problems: list[str] = []


def check(label: str, fn) -> None:
    try:
        detail = fn()
        print(f"[{OK}] {label}" + (f" — {detail}" if detail else ""))
    except Exception as e:  # noqa: BLE001
        print(f"[{BAD}] {label} — {e}")
        problems.append(label)


def python_version() -> str:
    if sys.version_info < (3, 9):
        raise RuntimeError(
            f"Python {sys.version_info.major}.{sys.version_info.minor}; "
            "please use 3.9 or newer"
        )
    return f"Python {sys.version_info.major}.{sys.version_info.minor}"


def dependencies() -> str:
    import requests  # noqa: F401

    return "requests installed"


def database() -> str:
    path = os.environ.get("WAREHOUSE_DB", "warehouse.db")
    if not os.path.exists(path):
        raise RuntimeError(
            f"{path} not found — run this from the repo root, or "
            "`python3 scripts/seed.py` to rebuild it"
        )
    conn = sqlite3.connect(path)
    n = conn.execute("SELECT COUNT(*) FROM picks WHERE status='pending'").fetchone()[0]
    conn.close()
    if n == 0:
        raise RuntimeError("no pending picks — run `python3 scripts/seed.py`")
    return f"{n} pending picks"


def api_key() -> str:
    key = os.environ.get("FLEET_API_KEY", "")
    if not key:
        raise RuntimeError(
            "FLEET_API_KEY is not set. Your interviewer gives you this:\n"
            "           export FLEET_API_KEY=cand_..."
        )
    return f"{key[:9]}…"


def fleet_api() -> str:
    import requests

    from app.config import FLEET_API_BASE_URL

    key = os.environ.get("FLEET_API_KEY", "")
    if not key:
        raise RuntimeError("skipped — no API key set")
    r = requests.get(
        f"{FLEET_API_BASE_URL}/robots",
        headers={"Authorization": f"Bearer {key}"},
        timeout=15,
    )
    if r.status_code == 401:
        raise RuntimeError("the fleet rejected that key — check it with your interviewer")
    r.raise_for_status()
    return f"{len(r.json())} robots reachable"


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print()
    check("Python version", python_version)
    check("Dependencies", dependencies)
    check("Database", database)
    check("API key", api_key)
    check("Fleet API", fleet_api)
    print()
    if problems:
        print(f"{len(problems)} problem(s): {', '.join(problems)}")
        print("Tell your interviewer before the call — it takes a minute to sort out.\n")
        sys.exit(1)
    print("All good. Nothing else to prepare.\n")
