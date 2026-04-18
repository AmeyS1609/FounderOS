"""Agent 04 — LinkedIn talent scout (RapidAPI + Claude ranking)."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from services import claude, firebase, rapidapi

logger = logging.getLogger(__name__)

router = APIRouter()


class TalentSearchBody(BaseModel):
    role: str
    location: str
    experience_years: int = Field(default=3, ge=0, le=50)


def _profiles_text(profiles: list[dict[str, Any]], cap: int = 4000) -> str:
    lines: list[str] = []
    for p in profiles:
        lines.append(
            f"- {p.get('name')}: {p.get('headline')} | {p.get('location')} | {p.get('summary')} | {p.get('profile_url')}"
        )
    s = "\n".join(lines)
    return s if len(s) <= cap else s[:cap]


@router.post("/search")
async def search(body: TalentSearchBody) -> dict[str, Any]:
    profiles = await rapidapi.search_people(body.role, body.location, max_results=15)
    if not profiles:
        profiles = rapidapi.mock_candidates(body.role, body.location)

    profiles_text = _profiles_text(profiles)
    prompt = f"""You are a talent acquisition specialist.

Role needed: {body.role}
Location: {body.location}
Experience: {body.experience_years}+ years

Candidate data:
{profiles_text}

Return JSON with a single key "candidates" whose value is an array of exactly 5 objects, each with:
name, current_role, location, experience_summary (one sentence),
fit_score (number 1-10), fit_reason (one sentence),
outreach_line (personalised 1-line opener referencing something specific),
profile_url
"""

    try:
        parsed = claude.ask_claude_json(prompt)
    except Exception as e:  # noqa: BLE001
        logger.warning("Claude talent ranking failed: %s", e)
        candidates = []
        for p in profiles[:5]:
            candidates.append(
                {
                    "name": p.get("name"),
                    "current_role": p.get("headline"),
                    "location": p.get("location"),
                    "experience_summary": (p.get("summary") or "")[:200],
                    "fit_score": p.get("fit_score", 7),
                    "fit_reason": "Strong match for the stated role and location.",
                    "outreach_line": f"Loved your background in {p.get('headline') or body.role} — open to a quick chat?",
                    "profile_url": p.get("profile_url", ""),
                }
            )
        doc_id = "unsaved"
        try:
            db = firebase.get_db()
            _, ref = db.collection("candidates").add(
                {
                    "role": body.role,
                    "location": body.location,
                    "experience_years": body.experience_years,
                    "candidates": candidates,
                    "created_at": firebase.SERVER_TIMESTAMP,
                }
            )
            doc_id = ref.id
        except Exception as ex:  # noqa: BLE001
            logger.warning("Candidates Firestore write skipped: %s", ex)
        return {"success": True, "id": doc_id, "candidates": candidates, "warning": str(e)}

    raw_list = parsed.get("candidates")
    if not isinstance(raw_list, list):
        raw_list = parsed.get("items") if isinstance(parsed.get("items"), list) else []

    candidates = [c for c in raw_list if isinstance(c, dict)][:5]
    while len(candidates) < 5 and len(profiles) > len(candidates):
        p = profiles[len(candidates)]
        candidates.append(
            {
                "name": p.get("name"),
                "current_role": p.get("headline"),
                "location": p.get("location"),
                "experience_summary": (p.get("summary") or "")[:200],
                "fit_score": p.get("fit_score", 7),
                "fit_reason": "Fallback row from search results.",
                "outreach_line": f"Impressed by your work in {p.get('headline') or body.role} — worth a quick chat?",
                "profile_url": p.get("profile_url", ""),
            }
        )

    doc_id = "unsaved"
    try:
        db = firebase.get_db()
        doc = {
            "role": body.role,
            "location": body.location,
            "experience_years": body.experience_years,
            "candidates": candidates,
            "created_at": firebase.SERVER_TIMESTAMP,
        }
        _, ref = db.collection("candidates").add(doc)
        doc_id = ref.id
    except Exception as e:  # noqa: BLE001
        logger.warning("Candidates Firestore write skipped: %s", e)

    return {"success": True, "id": doc_id, "candidates": candidates}
