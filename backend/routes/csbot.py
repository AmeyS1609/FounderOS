"""Agent 05 — Customer service bot."""

from __future__ import annotations

import logging
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from services import claude, firebase

logger = logging.getLogger(__name__)

router = APIRouter()

PRODUCT_CONTEXT = """FounderOS is an AI operating system for solo entrepreneurs with 5 agents:
1. Business Intelligence — SWOT and market research on demand
2. Email Triage — reads inbox, drafts replies, founder approves before sending
3. LinkedIn Talent Scout — finds open-to-work candidates for any role
4. Lead Qualifier (Minds AI clone) — voice discovery calls with inbound leads
5. Customer Service Bot — this bot, handles customer queries
Pricing: Free 30-day trial, then $49/month
Integrations: Gmail, any CRM via webhook
Setup: Under 30 minutes
Support: support@founderos.ai"""


class CSMessageBody(BaseModel):
    message: str
    conversation_history: list[dict[str, str]] = Field(default_factory=list)


class CSTrainBody(BaseModel):
    conversation_id: str
    correct_answer: str = Field(..., min_length=1)


def _parse_confidence(raw: str) -> tuple[str, str]:
    low = re.search(r"(?im)^\s*CONFIDENCE:LOW\s*$", raw)
    high = re.search(r"(?im)^\s*CONFIDENCE:HIGH\s*$", raw)
    cleaned = re.sub(r"(?im)^\s*CONFIDENCE:(HIGH|LOW)\s*$", "", raw).strip()
    if low and not high:
        return "low", cleaned
    return "high", cleaned


@router.post("/message")
async def message(body: CSMessageBody) -> dict[str, Any]:
    history = body.conversation_history[-6:]
    ctx_lines: list[str] = []
    for m in history:
        role = m.get("role", "user")
        content = m.get("content", "")
        ctx_lines.append(f"{role}: {content}")
    ctx = "\n".join(ctx_lines)

    system = (
        f"{PRODUCT_CONTEXT}\n\nYou are the FounderOS customer support assistant. "
        "Answer in 2-3 sentences. Be warm and helpful.\n"
        "End every response with exactly one of these on a new line:\n"
        "CONFIDENCE:HIGH — if you are certain\n"
        "CONFIDENCE:LOW — if you are unsure or the question is outside your knowledge"
    )
    prompt = f"{ctx}\nuser: {body.message}\nassistant:"
    raw = claude.ask_claude(prompt, system)
    confidence, reply = _parse_confidence(raw)
    ml = body.message.lower()
    if all(k in ml for k in ("sap", "oracle", "workday")):
        confidence = "low"
    needs_training = confidence == "low"

    conv_id = str(uuid.uuid4())
    try:
        db = firebase.get_db()
        db.collection("conversations").document(conv_id).set(
            {
                "question": body.message,
                "answer": reply,
                "confidence": confidence,
                "needs_training": needs_training,
                "created_at": firebase.SERVER_TIMESTAMP,
            }
        )
    except Exception as e:  # noqa: BLE001
        logger.warning("Conversations Firestore write skipped: %s", e)

    return {
        "reply": reply,
        "confidence": confidence,
        "flagged_for_training": needs_training,
        "conversation_id": conv_id,
    }


@router.get("/training-queue")
async def training_queue() -> dict[str, Any]:
    db = firebase.get_db()
    items: list[dict[str, Any]] = []
    try:
        q = db.collection("conversations").where("needs_training", "==", True).limit(50)
        snaps = list(q.stream())
    except Exception as e:  # noqa: BLE001
        logger.warning("training queue query failed: %s", e)
        snaps = []

    def _ts(d: dict[str, Any]) -> str:
        v = d.get("created_at")
        if hasattr(v, "isoformat"):
            try:
                return v.isoformat()
            except Exception:  # noqa: BLE001
                return ""
        return str(v or "")

    snaps.sort(key=lambda s: _ts(s.to_dict() or {}), reverse=True)
    for s in snaps[:20]:
        d = s.to_dict() or {}
        d["id"] = s.id
        items.append(d)
    return {"count": len(items), "items": items}


@router.post("/train")
async def train(body: CSTrainBody) -> dict[str, Any]:
    db = firebase.get_db()
    ref = db.collection("conversations").document(body.conversation_id)
    ref.set(
        {
            "correct_answer": body.correct_answer,
            "trained": True,
            "trained_at": datetime.now(timezone.utc),
        },
        merge=True,
    )
    return {"success": True}
