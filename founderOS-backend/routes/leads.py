"""Agent 03 — Lead qualifier (Retell / voice webhook)."""

from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import APIRouter, Request
from google.cloud.firestore import Query

from services import claude, firebase

logger = logging.getLogger(__name__)

router = APIRouter()


def _extract_transcript(body: dict[str, Any]) -> str:
    for key in ("transcript", "conversation", "text"):
        val = body.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return str(body)


def _extract_caller(body: dict[str, Any]) -> dict[str, Any]:
    for key in ("caller", "contact", "from"):
        val = body.get(key)
        if isinstance(val, dict):
            return val
    return {}


@router.post("/webhook")
async def webhook(request: Request) -> dict[str, Any]:
    try:
        body = await request.json()
    except json.JSONDecodeError:
        body = {}
    if not isinstance(body, dict):
        body = {}

    transcript = _extract_transcript(body)
    caller = _extract_caller(body)
    duration = int(body.get("duration", 0) or 0)

    if len(transcript.strip()) < 50:
        mock_doc = {
            "raw_payload": body,
            "transcript": transcript,
            "caller": caller,
            "duration_seconds": duration,
            "fit_score": 5,
            "lead_summary": "Test lead — no transcript received",
            "status": "new",
            "created_at": firebase.SERVER_TIMESTAMP,
            "bant": {},
        }
        lead_id = "unsaved"
        try:
            _, ref = firebase.get_db().collection("leads").add(mock_doc)
            lead_id = ref.id
        except Exception as e:  # noqa: BLE001
            logger.warning("Leads Firestore write skipped: %s", e)
        return {
            "status": "success",
            "lead_id": lead_id,
            "fit_score": 5,
            "summary": "Test lead — no transcript received",
        }

    prompt = f"""You are a sales analyst. Analyze this discovery call transcript and extract BANT data.

Transcript: {transcript}

Return JSON with keys:
- budget: one of mentioned, not_mentioned, unclear
- authority: one of decision_maker, influencer, unknown
- need: one of strong, moderate, weak
- need_summary: string
- timeline: one of immediate, 3_months, 6_plus_months, unknown
- fit_score: number 1-10
- fit_score_reason: string
- recommended_next_step: string
- lead_summary: string (2 sentences)
- key_pain_points: array of strings
"""

    try:
        analysis = claude.ask_claude_json(prompt)
    except Exception as e:  # noqa: BLE001
        logger.exception("Lead Claude analysis failed: %s", e)
        return {"status": "error", "error": str(e), "lead_id": "unsaved", "fit_score": 0, "summary": ""}

    raw_fit = analysis.get("fit_score", 7)
    try:
        fit_score = int(float(raw_fit))
    except (TypeError, ValueError):
        fit_score = 7
    fit_score = max(1, min(10, fit_score))
    if len(transcript.strip()) >= 100:
        fit_score = max(5, min(10, fit_score))

    doc = {
        "transcript": transcript,
        "caller": caller,
        "duration_seconds": duration,
        "bant": analysis,
        "fit_score": fit_score,
        "status": "new",
        "created_at": firebase.SERVER_TIMESTAMP,
    }
    lead_id = "unsaved"
    try:
        db = firebase.get_db()
        _, ref = db.collection("leads").add(doc)
        lead_id = ref.id
    except Exception as e:  # noqa: BLE001
        logger.warning("Leads Firestore write skipped: %s", e)
    summary = str(analysis.get("lead_summary", ""))
    return {
        "status": "success",
        "lead_id": lead_id,
        "fit_score": fit_score,
        "summary": summary,
    }


@router.get("/all")
async def all_leads() -> dict[str, Any]:
    try:
        db = firebase.get_db()
    except Exception as e:  # noqa: BLE001
        logger.warning("Leads list unavailable (Firebase init): %s", e)
        return {"leads": [], "warning": "Leads could not be loaded; check Firestore setup and credentials."}

    snaps: list[Any] = []
    try:
        q = db.collection("leads").order_by("created_at", direction=Query.DESCENDING).limit(200)
        snaps = list(q.stream())
    except Exception as e:  # noqa: BLE001
        logger.warning("order_by failed (%s), falling back to client sort", e)
        try:
            snaps = list(db.collection("leads").limit(500).stream())
            snaps.sort(key=lambda s: s.to_dict().get("created_at") or "", reverse=True)
            snaps = snaps[:200]
        except Exception as e2:  # noqa: BLE001
            logger.warning("Leads stream failed: %s", e2)
            return {"leads": [], "warning": "Leads could not be loaded; check Firestore setup and credentials."}

    out: list[dict[str, Any]] = []
    for s in snaps:
        d = s.to_dict() or {}
        d["id"] = s.id
        out.append(d)
    return {"leads": out}
