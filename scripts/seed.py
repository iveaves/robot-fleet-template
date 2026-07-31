"""Rebuild warehouse.db from scratch.

The committed database is the output of this script, so the repo needs no
setup step. Re-run it any time you want a clean slate.
"""

from __future__ import annotations

import os
import sqlite3
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB = os.environ.get("WAREHOUSE_DB", "warehouse.db")

ZONES = {"A": (1, 10), "B": (11, 20), "C": (21, 30), "D": (31, 40)}
SCHEMA = """
DROP TABLE IF EXISTS picks;
DROP TABLE IF EXISTS dispatches;

CREATE TABLE picks (
    id          TEXT PRIMARY KEY,
    sku         TEXT NOT NULL,
    aisle       INTEGER NOT NULL,
    zone        TEXT NOT NULL,
    quantity    INTEGER NOT NULL,
    priority    INTEGER NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending',
    created_at  REAL NOT NULL
);

CREATE TABLE dispatches (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    pick_id        TEXT NOT NULL,
    task_id        TEXT NOT NULL,
    robot_id       TEXT NOT NULL,
    dispatched_at  REAL NOT NULL,
    status         TEXT NOT NULL DEFAULT 'in_progress'
);
CREATE INDEX dispatches_pick ON dispatches(pick_id);
"""


def main() -> None:
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)

    now = time.time()
    rows = []
    for n in range(1, 41):
        aisle = ((n - 1) % 40) + 1
        zone = next(z for z, (lo, hi) in ZONES.items() if lo <= aisle <= hi)
        rows.append(
            (
                f"P-{100 + n}",
                f"SKU-{4000 + n * 7}",
                aisle,
                zone,
                1 + (n % 4),
                1 + (n % 3),
                "pending",
                now - (40 - n) * 60,
            )
        )
    conn.executemany(
        "INSERT INTO picks (id, sku, aisle, zone, quantity, priority, status, created_at)"
        " VALUES (?,?,?,?,?,?,?,?)",
        rows,
    )
    conn.commit()
    conn.close()
    print(f"seeded {DB} with {len(rows)} pending picks")


if __name__ == "__main__":
    main()
