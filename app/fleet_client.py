"""HTTP wrapper for the Meridian fleet API.

`list_robots` is written as an example of the pattern. The rest is yours —
the endpoints and schemas are at:

    https://fleet-api-production-4bc7.up.railway.app/docs
"""

from __future__ import annotations

from typing import Any

import requests

from app.config import FLEET_API_BASE_URL, FLEET_API_KEY


class FleetError(RuntimeError):
    """The fleet API said no."""

    def __init__(self, status: int, message: str):
        super().__init__(f"fleet API {status}: {message}")
        self.status = status
        self.message = message


class FleetClient:
    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = (base_url or FLEET_API_BASE_URL).rstrip("/")
        self.api_key = api_key or FLEET_API_KEY
        if not self.api_key:
            raise RuntimeError(
                "No API key. Your interviewer will give you one:\n"
                "    export FLEET_API_KEY=cand_..."
            )
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {self.api_key}"

    def _request(self, method: str, path: str, **kwargs) -> Any:
        resp = self.session.request(
            method, f"{self.base_url}{path}", timeout=10, **kwargs
        )
        if not resp.ok:
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text
            raise FleetError(resp.status_code, str(detail))
        return resp.json() if resp.content else None

    # ------------------------------------------------------------------
    # Written for you, as an example of the shape.
    # ------------------------------------------------------------------

    def list_robots(self) -> list[dict]:
        """Every robot in your warehouse and what it's currently doing."""
        return self._request("GET", "/robots")

    # ------------------------------------------------------------------
    # Over to you. See /docs for the rest.
    # ------------------------------------------------------------------

    def create_task(self, pick_id: str, robot_id: str) -> dict:
        raise NotImplementedError

    def get_task(self, task_id: str) -> dict:
        raise NotImplementedError

    def reset(self) -> dict:
        """Wipe every task for your key. Handy while you're experimenting."""
        return self._request("POST", "/admin/reset")
