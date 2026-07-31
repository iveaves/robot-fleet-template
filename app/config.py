"""Settings, read from the environment."""

import os

FLEET_API_BASE_URL = os.environ.get(
    "FLEET_API_BASE_URL",
    "https://fleet-api-production-4bc7.up.railway.app",
)

# Your interviewer gives you this at the start:  export FLEET_API_KEY=cand_...
FLEET_API_KEY = os.environ.get("FLEET_API_KEY", "")

DB_PATH = os.environ.get("WAREHOUSE_DB", "warehouse.db")
