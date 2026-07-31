"""Two examples, so the harness is obvious.

`tmp_db` gives each test its own freshly seeded database — the committed
warehouse.db is never touched by the suite.

The fleet API is stubbed here. You could also test against the real one using
your key and POST /admin/reset between runs; both are reasonable, and which
you choose (and why) is worth a conversation.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

from app.db import query
from app.models import PENDING

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    """A fresh, seeded warehouse.db for one test."""
    path = str(tmp_path / "warehouse.db")
    env = {**os.environ, "WAREHOUSE_DB": path}
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "seed.py")],
        env=env, cwd=str(tmp_path), check=True, capture_output=True,
    )
    monkeypatch.setattr("app.config.DB_PATH", path)
    monkeypatch.setattr("app.db.DB_PATH", path)
    return path


class FakeFleet:
    """Stand-in for the real client. Grow it as you need."""

    def __init__(self, robots=None):
        self._robots = robots or [
            {"id": "R-01", "zone": "A", "status": "idle", "battery_pct": 0.9,
             "current_task_id": None, "last_moved_at": 0.0},
        ]
        self.created: list[tuple[str, str]] = []

    def list_robots(self):
        return list(self._robots)

    def create_task(self, pick_id, robot_id):
        self.created.append((pick_id, robot_id))
        return {
            "id": f"T-{len(self.created):04d}",
            "pick_id": pick_id,
            "robot_id": robot_id,
            "status": "in_progress",
            "created_at": 0.0,
        }


def test_seeded_database_has_pending_work(tmp_db):
    picks = query("SELECT * FROM picks WHERE status = ?", (PENDING,), path=tmp_db)
    assert len(picks) == 40
    assert all(p["status"] == PENDING for p in picks)


def test_fake_fleet_records_what_was_created(tmp_db):
    """A shape you can build on: assert on what the dispatcher TOLD the fleet,
    not just on what ended up in our database."""
    fleet = FakeFleet()
    fleet.create_task("P-101", "R-01")
    assert fleet.created == [("P-101", "R-01")]
