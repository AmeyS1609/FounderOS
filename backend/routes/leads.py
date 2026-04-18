"""Agent 03 — Minds AI lead webhook."""

from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import APIRouter, Request
from google.cloud.firestore import Query

from backend.services import claude
from backend.services import firebase

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
    body: dict[str, Any]
    try:
        body = await request.json()
    except json.JSONDecodeError:
        body = {}

    transcript = _extract_transcript(body)
    caller = _extract_caller(body)
    duration = int(body.get("duration", 0) or 0)

    db = firebase.get_db()

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

    system = "You are a sales analyst. Return only valid JSON."
    user = f"""Analyze this discovery call transcript and extract BANT data.

Transcript: {transcript}

Return JSON:
{{
  "budget": "mentioned" | "not_mentioned" | "unclear",
  "authority": "decision_maker" | "influencer" | "unknown",
  "need": "strong" | "moderate" | "weak",
  "need_summary": "string",
  "timeline": "immediate" | "3_months" | "6_plus_months" | "unknown",
  "fit_score": "number 1-10",
  "fit_score_reason": "string",
  "recommended_next_step": "string",
  "lead_summary": "string (2 sentences)",
  "key_pain_points": ["list of strings"]
}}"""

    analysis = claude.ask_claude_json(user, system)
    if not isinstance(analysis, dict):
        raise ValueError("Lead analysis must be a JSON object")

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
    db = firebase.get_db()
    try:
        q = db.collection("leads").order_by("created_at", direction=Query.DESCENDING).limit(20)
        snaps = list(q.stream())
    except Exception as e:  # noqa: BLE001
        logger.warning("order_by failed (%s), falling back to client sort", e)
        snaps = list(db.collection("leads").limit(50).stream())
        snaps.sort(key=lambda s: s.to_dict().get("created_at") or "", reverse=True)
        snaps = snaps[:20]

    out = []
    for s in snaps:
        d = s.to_dict() or {}
        d["id"] = s.id
        out.append(d)
    return {"leads": out}
