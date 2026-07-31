# Warehouse dispatch

Our warehouse has picks that need collecting and a fleet of robots that can
collect them. The robots belong to a vendor — **Meridian** — and we talk to
them over an HTTP API.

Right now a human assigns the work. We want a script.

## The job

> **Read the outstanding picks from our database, assign them to robots via the
> Meridian API, and keep our records in step. It should be safe to run every 30
> seconds.**

That's it. `app/dispatch.py` is where it goes.

## Getting set up

**In a Codespace** — everything is installed already. Skip to *Credentials*.

**Locally**

```bash
pip install -r requirements.txt
```

The database is a SQLite file committed to the repo (`warehouse.db`), already
seeded. Nothing to migrate. If you want a clean slate:

```bash
python scripts/seed.py          # rebuilds warehouse.db from scratch
```

## Credentials

Your interviewer will give you an API key at the start. Then:

```bash
export FLEET_API_KEY=cand_...
```

The base URL is already set in `app/config.py`. Check it works:

```bash
python -c "from app.fleet_client import FleetClient; print(FleetClient().list_robots())"
```

## The API

Interactive docs, including every endpoint and schema:

**https://fleet-api-production-4bc7.up.railway.app/docs**

Your key is scoped to your own warehouse — your robots and tasks are yours
alone, so nothing you do affects anyone else.

`POST /admin/reset` wipes all tasks for your key and gives you a clean fleet.
Use it as much as you like. **Poking at the API is encouraged** — it's the
fastest way to understand it.

## What's in here

```
app/
  config.py         settings, read from the environment
  db.py             tiny SQLite helper — connect, query, execute
  models.py         Pick and Dispatch
  fleet_client.py   HTTP wrapper for the Meridian API (partly written)
  dispatch.py       ← your work goes here
tests/
  test_dispatch.py  two examples, so the harness is obvious
scripts/
  seed.py           rebuild warehouse.db
warehouse.db        seeded, committed
```

Run the tests with:

```bash
pytest
```

## How we'll work

Use AI, use Google, read the docs, and **think out loud** — we're more
interested in how you approach it than in how fast you type. Ask us anything;
some of what you need isn't written down anywhere, and asking is the right
move rather than a fallback.

There's no hidden trick and no single correct answer. Build something you'd be
comfortable running, and we'll talk about what happens when it meets reality.
