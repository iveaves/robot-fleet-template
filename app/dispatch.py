"""Assign outstanding picks to robots.

Designed to be run on a schedule:

    python -m app.dispatch

It should be safe to run every 30 seconds.
"""

from __future__ import annotations

import logging

from app.db import query
from app.fleet_client import FleetClient
from app.models import PENDING

log = logging.getLogger(__name__)


def pending_picks() -> list[dict]:
    """Work we still owe, most urgent first."""
    return query(
        "SELECT * FROM picks WHERE status = ? ORDER BY priority, created_at",
        (PENDING,),
    )


def run() -> None:
    """One pass of the dispatcher.

    TODO: this is the job.
    """
    fleet = FleetClient()
    picks = pending_picks()
    robots = fleet.list_robots()
    log.info("%d pending picks, %d robots", len(picks), len(robots))
    raise NotImplementedError("this is the bit we'd like you to write")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    run()
