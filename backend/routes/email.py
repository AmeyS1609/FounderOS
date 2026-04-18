"""Agent 02 — Email triage (Gmail read + drafts; never auto-sends)."""

from __future__ import annotations

import logging
from typing import Any

import httpx
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from services import claude, firebase

logger = logging.getLogger(__name__)

router = APIRouter()

GMAIL_LIST = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
GMAIL_GET = "https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}"

MEETING_KEYWORDS = (
    "meeting",
    "call",
    "chat",
    "sync",
    "catch up",
    "schedule",
    "discuss",
    "connect",
)


def _header(headers: list[dict[str, str]], name: str) -> str:
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return str(h.get("value", ""))
    return ""


class ApproveBody(BaseModel):
    email_id: str
    final_reply: str = Field(..., min_length=1)


@router.get("/inbox")
async def inbox(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization required")
    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Authorization required")
    if "FAKE" in token.upper():
        raise HTTPException(status_code=401, detail="Gmail token expired — re-authenticate")

    params = {"maxResults": "10", "labelIds": "INBOX"}
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(timeout=httpx.Timeout(45.0)) as client:
        lr = await client.get(GMAIL_LIST, params=params, headers=headers)
        if lr.status_code == 401:
            raise HTTPException(status_code=401, detail="Gmail token expired — re-authenticate")
        if lr.status_code != 200:
            logger.error("Gmail list error %s: %s", lr.status_code, lr.text[:400])
            raise HTTPException(status_code=502, detail="Gmail API error")

        payload = lr.json()
        messages = payload.get("messages") or []
        emails_out: list[dict[str, Any]] = []

        for m in messages[:5]:
            mid = m.get("id")
            if not mid:
                continue
            gr = await client.get(
                GMAIL_GET.format(id=mid),
                params=[
                    ("format", "metadata"),
                    ("metadataHeaders", "Subject"),
                    ("metadataHeaders", "From"),
                    ("metadataHeaders", "Date"),
                ],
                headers=headers,
            )
            if gr.status_code != 200:
                continue
            detail = gr.json()
            pl = detail.get("payload") or {}
            hdrs = pl.get("headers") or []
            subject = _header(hdrs, "Subject")
            sender = _header(hdrs, "From")
            date = _header(hdrs, "Date")
            subj_l = subject.lower()
            is_meeting = any(k in subj_l for k in MEETING_KEYWORDS)

            draft = claude.ask_claude(
                f"Draft a 2-3 sentence reply.\nFrom: {sender}\nSubject: {subject}",
                "You are helping a solo startup founder reply to emails. Be warm and concise.",
            )
            cal_suggestion = ""
            if is_meeting:
                cal_suggestion = claude.ask_claude(
                    f"This is a meeting request from {sender}: '{subject}'. "
                    "Suggest: accept or decline, event title, and one reason. Be brief.",
                    "You are helping a solo startup founder manage their calendar.",
                )

            obj = {
                "id": mid,
                "subject": subject,
                "sender": sender,
                "date": date,
                "draft_reply": draft,
                "is_meeting_request": is_meeting,
                "calendar_suggestion": cal_suggestion,
                "status": "pending",
            }
            try:
                db = firebase.get_db()
                db.collection("emails").document(mid).set(obj, merge=True)
            except Exception as e:  # noqa: BLE001
                logger.warning("Emails Firestore write skipped: %s", e)
            emails_out.append(obj)

    return {"emails": emails_out}


@router.post("/approve")
async def approve(body: ApproveBody) -> dict[str, Any]:
    db = firebase.get_db()
    ref = db.collection("emails").document(body.email_id)
    ref.set(
        {
            "status": "approved",
            "final_reply": body.final_reply,
        },
        merge=True,
    )
    return {"success": True, "message": "Reply approved"}
