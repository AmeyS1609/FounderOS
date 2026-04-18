"""FounderOS Backend — FastAPI entrypoint."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

_APP_DIR = Path(__file__).resolve().parent
load_dotenv(_APP_DIR / ".env", override=True)
load_dotenv(override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("founderos")

from routes import bi, csbot, email, leads, talent  # noqa: E402


def _parse_origin_list(raw: str) -> list[str]:
    out: list[str] = []
    for part in raw.split(","):
        p = part.strip().rstrip("/")
        if p and p not in out:
            out.append(p)
    return out


def _cors_origins() -> list[str]:
    origins: list[str] = []
    origins.extend(_parse_origin_list(os.getenv("FRONTEND_URL", "")))
    origins.extend(_parse_origin_list(os.getenv("CORS_EXTRA_ORIGINS", "")))
    for o in (
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ):
        if o not in origins:
            origins.append(o)
    return origins


def _cors_origin_regex() -> str | None:
    """Netlify deploy + production URLs match by default; set CORS_ORIGIN_REGEX= to disable."""
    raw = os.getenv("CORS_ORIGIN_REGEX")
    if raw is None:
        return r"https://.*\.netlify\.app$"
    stripped = raw.strip()
    return stripped or None


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    try:
        from services import firebase as fb

        if fb.is_configured():
            fb.init_firebase()
            logger.info("Firestore client ready")
        else:
            logger.warning(
                "Firebase not configured (no JSON env and no service account file). "
                "Firestore-backed routes will error until credentials are set."
            )
    except Exception:  # noqa: BLE001
        logger.exception("Firestore initialization failed; continuing without DB")
    yield


app = FastAPI(title="FounderOS Backend", lifespan=_lifespan)

_cors_list = _cors_origins()
_cors_regex = _cors_origin_regex()
logger.info("CORS allow_origins count=%s regex=%s", len(_cors_list), _cors_regex or "off")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_list,
    allow_origin_regex=_cors_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bi.router, prefix="/api/bi", tags=["bi"])
app.include_router(email.router, prefix="/api/email", tags=["email"])
app.include_router(talent.router, prefix="/api/talent", tags=["talent"])
app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(csbot.router, prefix="/api/csbot", tags=["csbot"])


@app.options("/{full_path:path}")
async def options_preflight(full_path: str) -> Response:  # noqa: ARG001
    return Response(status_code=200)


@app.get("/")
async def root() -> dict[str, Any]:
    return {"status": "FounderOS backend running", "agents": 5}


@app.get("/health")
async def health() -> dict[str, Any]:
    from services import firebase as fb

    return {
        "ok": True,
        "service": "founderos-backend",
        "firestore": {
            "configured": fb.is_configured(),
            "initialized": fb.db is not None,
        },
    }


def _env_set(key: str) -> bool:
    val = os.getenv(key)
    return bool(val and str(val).strip())


@app.get("/env-check")
async def env_check() -> dict[str, Any]:
    """Report which critical env vars are set (never expose secret values)."""
    keys = (
        "PORT",
        "FRONTEND_URL",
        "ANTHROPIC_API_KEY",
        "APIFY_TOKEN",
        "RAPIDAPI_KEY",
        "FIREBASE_SERVICE_ACCOUNT_PATH",
        "FIREBASE_SERVICE_ACCOUNT_JSON",
        "GMAIL_CLIENT_ID",
        "GMAIL_CLIENT_SECRET",
        "CORS_EXTRA_ORIGINS",
        "CORS_ORIGIN_REGEX",
    )
    vars_report: dict[str, str] = {}
    for key in keys:
        if key == "FIREBASE_SERVICE_ACCOUNT_JSON":
            vars_report[key] = "set" if _env_set(key) else "missing"
        else:
            vars_report[key] = "set" if _env_set(key) else "missing"

    from services import firebase as fb

    firebase_ready = fb.is_configured() and fb.db is not None
    vars_report["firestore_runtime"] = "ready" if firebase_ready else "not_ready"

    live_apis = bool(_env_set("ANTHROPIC_API_KEY") and firebase_ready)

    return {
        "vars": vars_report,
        "all_required_for_live_apis": live_apis,
        "note": (
            "On Render, prefer FIREBASE_SERVICE_ACCOUNT_JSON (secret) over committing a key file. "
            "Gmail live inbox needs GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, and OAuth; "
            "otherwise /api/email/inbox may return mock data."
        ),
    }
