"""RapidAPI LinkedIn people search (LinkedIn Data Max or configurable host)."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any
import httpx
from dotenv import load_dotenv

_APP_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_APP_ROOT / ".env", override=True)
load_dotenv(override=True)

logger = logging.getLogger(__name__)

# Default: Fresh LinkedIn "search-employees" (widely used on RapidAPI).
# For **LinkedIn Data Max** (or another product), set in .env:
#   RAPIDAPI_LINKEDIN_HOST=…your-subscribed-host….p.rapidapi.com
#   RAPIDAPI_LINKEDIN_PATH=/your/search/path   (include leading slash)
_DEFAULT_HOST = "fresh-linkedin-profile-data.p.rapidapi.com"
_DEFAULT_PATH = "/search-employees"


def mock_candidates(role: str, location: str) -> list[dict[str, Any]]:
    """Demo candidates when RapidAPI is unavailable or returns empty."""
    base = [
        ("Jordan Kim", f"Staff engineer — {role}", location),
        ("Samira Patel", "Founding engineer | ex-FAANG", location),
        ("Chris Ortiz", "Full-stack contractor, open to FT", location),
        ("Alex Morgan", "Product-minded senior developer", location),
        ("Taylor Brooks", "Startup engineer; systems + web", location),
    ]
    out: list[dict[str, Any]] = []
    for name, headline, loc in base:
        slug = name.lower().replace(" ", "-")
        out.append(
            {
                "name": name,
                "headline": headline,
                "location": loc,
                "profile_url": f"https://www.linkedin.com/in/{slug}-demo",
                "summary": f"Experienced in {role}; based in {loc}. Demo profile for FounderOS.",
                "fit_score": 7,
            }
        )
    return out


def _normalize_profile(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": str(raw.get("name") or raw.get("fullName") or "Unknown"),
        "headline": str(raw.get("headline") or raw.get("title") or ""),
        "location": str(raw.get("location") or raw.get("geo") or ""),
        "profile_url": str(raw.get("profile_url") or raw.get("url") or ""),
        "summary": str(raw.get("summary") or raw.get("about") or ""),
    }


def _linkedin_host() -> str:
    return (os.getenv("RAPIDAPI_LINKEDIN_HOST") or _DEFAULT_HOST).strip().rstrip("/")


def _linkedin_path() -> str:
    p = (os.getenv("RAPIDAPI_LINKEDIN_PATH") or _DEFAULT_PATH).strip()
    return p if p.startswith("/") else f"/{p}"


async def search_people(role: str, location: str, max_results: int = 10) -> list[dict[str, Any]]:
    """
    Query RapidAPI LinkedIn search (host/path configurable for **LinkedIn Data Max**).
    Subscribes on RapidAPI must match RAPIDAPI_LINKEDIN_HOST / RAPIDAPI_LINKEDIN_PATH.
    """
    key = (os.getenv("RAPIDAPI_KEY") or "").strip()
    if not key:
        logger.warning("RAPIDAPI_KEY not set — using mock candidate data")
        return mock_candidates(role, location)

    host = _linkedin_host()
    path = _linkedin_path()
    url = f"https://{host}{path}"
    params: dict[str, str] = {
        "keywords": f"{role} {location}",
        "limit": str(max_results),
    }
    if "fresh-linkedin" in host and "search-employees" in path:
        params["company_domain"] = ""

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": host,
    }
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(45.0)) as client:
            r = await client.get(url, headers=headers, params=params)
            if r.status_code != 200:
                logger.warning("RapidAPI HTTP %s — using mock data", r.status_code)
                return mock_candidates(role, location)
            body = r.json()
            items = body if isinstance(body, list) else body.get("data") or body.get("employees") or []
            if not isinstance(items, list) or not items:
                logger.warning("RapidAPI empty response — using mock data")
                return mock_candidates(role, location)
            normalized: list[dict[str, Any]] = []
            for it in items[:max_results]:
                if isinstance(it, dict):
                    normalized.append(_normalize_profile(it))
            if not normalized:
                return mock_candidates(role, location)
            return normalized
    except Exception as e:  # noqa: BLE001
        logger.warning("RapidAPI error %s — using mock data", e)
        return mock_candidates(role, location)
