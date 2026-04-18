"""Apify actors via async HTTP."""

from __future__ import annotations

import asyncio
import logging
import os
import time
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

_APP_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_APP_ROOT / ".env", override=True)
load_dotenv(override=True)

logger = logging.getLogger(__name__)

APIFY_BASE = "https://api.apify.com/v2"


def _normalize_actor(actor: str) -> str:
    if "~" in actor:
        return actor
    if "/" in actor:
        return actor.replace("/", "~", 1)
    return actor


def _token() -> str | None:
    t = os.getenv("APIFY_TOKEN")
    return t.strip() if t else None


async def run_actor(
    actor_id: str,
    input_data: dict[str, Any],
    timeout_seconds: int = 90,
) -> list[Any]:
    """Start actor run, poll until success/fail/timeout."""
    token = _token()
    if not token:
        logger.warning("APIFY_TOKEN is not set — skipping Apify actor run (use empty list)")
        return []

    aid = _normalize_actor(actor_id)
    t0 = time.monotonic()
    backoff_schedule = [3, 5, 10, 15, 20]
    poll_index = 0

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            start = await client.post(
                f"{APIFY_BASE}/acts/{aid}/runs",
                params={"token": token},
                json=input_data,
            )
            if start.status_code not in (200, 201):
                logger.error("Apify start run failed HTTP %s: %s", start.status_code, start.text[:400])
                return []
            run = start.json().get("data") or {}
            run_id = run.get("id")
            if not run_id:
                return []

            while True:
                elapsed = time.monotonic() - t0
                if elapsed >= timeout_seconds:
                    logger.warning("Apify actor %s timed out after %.0fs", actor_id, elapsed)
                    return []

                st = await client.get(f"{APIFY_BASE}/actor-runs/{run_id}")
                if st.status_code != 200:
                    logger.error("Apify status HTTP %s", st.status_code)
                    return []
                data = st.json().get("data") or {}
                status = data.get("status")
                if status == "SUCCEEDED":
                    dataset_id = data.get("defaultDatasetId")
                    if not dataset_id:
                        return []
                    items_r = await client.get(
                        f"{APIFY_BASE}/datasets/{dataset_id}/items",
                        params={"clean": "true", "format": "json"},
                    )
                    if items_r.status_code != 200:
                        return []
                    items = items_r.json()
                    return items if isinstance(items, list) else []
                if status in ("FAILED", "ABORTED", "TIMED-OUT"):
                    logger.error("Apify actor %s failed: %s", actor_id, status)
                    return []

                sleep_s = (
                    backoff_schedule[poll_index]
                    if poll_index < len(backoff_schedule)
                    else 20
                )
                poll_index += 1
                remaining = timeout_seconds - (time.monotonic() - t0)
                if remaining <= 0:
                    return []
                await asyncio.sleep(min(sleep_s, max(0.1, remaining)))

    except Exception as e:  # noqa: BLE001
        logger.exception("Apify run_actor error: %s", e)
        return []


async def scrape_url(url: str, max_pages: int = 3) -> list[Any]:
    """Run Apify web-scraper on a single URL."""
    return await run_actor(
        "apify/web-scraper",
        {
            "startUrls": [{"url": url}],
            "maxPagesPerCrawl": max_pages,
            "maxConcurrency": 2,
        },
    )


async def scrape_news(query: str, max_results: int = 10) -> list[Any]:
    """Google search results via Apify (news / web context for BI)."""
    return await run_actor(
        "apify/google-search-scraper",
        {
            "queries": [query],
            "maxPagesPerQuery": 1,
            "resultsPerPage": max_results,
        },
    )
