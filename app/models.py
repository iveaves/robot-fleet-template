"""What our warehouse knows about.

The fleet vendor knows about robots and tasks. We know about the work that
needs doing and what we've told them to do about it.
"""

from __future__ import annotations

from dataclasses import dataclass

# picks.status
PENDING = "pending"
ASSIGNED = "assigned"
DONE = "done"


@dataclass
class Pick:
    id: str
    sku: str
    aisle: int
    zone: str
    quantity: int
    priority: int  # 1 is most urgent
    status: str
    created_at: float


@dataclass
class Dispatch:
    """Our record of a task we asked the fleet to run."""

    id: int
    pick_id: str
    task_id: str
    robot_id: str
    dispatched_at: float
    status: str
