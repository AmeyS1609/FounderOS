"""FounderOS FastAPI backend."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

_ROOT = Path(__file__).resolve().parent
load_dotenv(_ROOT / ".env", override=True)
load_dotenv(override=True)

from backend.routes import bi, csbot, email, leads
from backend.routes import talent  # noqa: E402
from backend.services import rapidapi  # noqa: E402


def _debug() -> bool:
    return os.getenv("DEBUG", "").lower() in ("1", "true", "yes")


app = FastAPI(title="FounderOS API")

_cors_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
]
_extra_origin = os.getenv("FRONTEND_URL", "").strip()
if _extra_origin and _extra_origin not in _cors_origins:
    _cors_origins.append(_extra_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bi.router, prefix="/api/bi", tags=["bi"])
app.include_router(email.router, prefix="/api/email", tags=["email"])
app.include_router(talent.router, prefix="/api/talent", tags=["talent"])
app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(csbot.router, prefix="/api/csbot", tags=["csbot"])


@app.on_event("startup")
async def _startup_init_firebase() -> None:
    try:
        from pathlib import Path

        from backend.services.firebase import init_firebase

        raw = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "./firebase-service-account.json")
        if Path(raw).expanduser().resolve().is_file():
            init_firebase()
    except Exception:  # noqa: BLE001
        pass


@app.options("/{full_path:path}")
async def options_preflight(full_path: str) -> Response:  # noqa: ARG001
    return Response(status_code=200)


@app.get("/")
async def health() -> dict[str, Any]:
    return {"status": "FounderOS running", "agents": 5}


@app.get("/api/debug/mock-all")
async def mock_all() -> dict[str, Any]:
    """Demo-only: canned agent outputs without external APIs (requires DEBUG=true)."""
    if not _debug():
        raise HTTPException(status_code=404, detail="Not found")
    candidates = rapidapi.mock_candidates("founding engineer", "Remote")[:3]
    return {
        "bi": {
            "success": True,
            "id": "mock-bi",
            "analysis": {
                "swot": {
                    "strengths": ["Speed", "UX", "Distribution"],
                    "weaknesses": ["Burn", "Competition", "Hiring"],
                    "opportunities": ["AI", "SMB", "Global"],
                    "threats": ["Incumbents", "Pricing", "Regulation"],
                },
                "market_overview": "Mock market overview for dashboard testing.",
                "market_size": "$12B TAM (illustrative)",
                "top_competitors": ["A", "B", "C"],
                "pros": ["Fast iteration", "Clear ICP", "Strong retention"],
                "cons": ["Crowded space", "CAC pressure", "Feature parity risk"],
                "what_to_expect": "Mock outlook: focus on wedge and distribution.",
                "recommended_tools": [
                    {"name": "Notion", "purpose": "Docs", "free_tier": True},
                    {"name": "Linear", "purpose": "Delivery", "free_tier": True},
                    {"name": "PostHog", "purpose": "Analytics", "free_tier": True},
                ],
                "business_model_suggestions": ["PLG", "Usage-based", "Services-assisted onboarding"],
            },
        },
        "email": {
            "emails": [
                {
                    "id": "mock-email-1",
                    "subject": "Quick sync tomorrow?",
                    "sender": "partner@example.com",
                    "date": "Mon, 1 Jan 2026 09:00:00 +0000",
                    "draft_reply": "Thanks for reaching out — happy to sync. Does Tuesday 3pm work?",
                    "is_meeting_request": True,
                    "calendar_suggestion": "Accept — title: Partner sync — reason: relationship maintenance.",
                    "status": "pending",
                }
            ]
        },
        "leads": {
            "status": "success",
            "lead_id": "mock-lead",
            "fit_score": 8,
            "summary": "Mock summary: strong pain on outbound sales time.",
        },
        "talent": {"success": True, "id": "mock-talent", "candidates": candidates},
        "csbot": {
            "reply": "FounderOS has a 30-day free trial, then $49/month.\nPricing page has details.",
            "confidence": "high",
            "flagged_for_training": False,
            "conversation_id": "mock-conv",
        },
    }
