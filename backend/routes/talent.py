"""Agent 04 — LinkedIn talent scout (RapidAPI + Claude ranking)."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services import claude, firebase
from backend.services import rapidapi

logger = logging.getLogger(__name__)

# Production note: Replace RapidAPI with LinkedIn Official Talent API
# Apply at: https://developer.linkedin.com/product-catalog/talent

router = APIRouter()


class TalentSearchBody(BaseModel):
    role: str
    location: str
    experience_years: int = Field(default=3, ge=0, le=50)
    use_mock: bool = Field(
        default=False,
        description="If true, skip external search and use local mock_candidates()",
    )


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
    if body.use_mock:
        profiles = rapidapi.mock_candidates(body.role, body.location)[:15]
    else:
        profiles = await rapidapi.search_people(body.role, body.location, max_results=15)
        if not profiles:
            logger.warning("search_people returned empty — using mock_candidates")
            profiles = rapidapi.mock_candidates(body.role, body.location)

    profiles_text = _profiles_text(profiles)
    system = "You are a talent acquisition specialist. Return only valid JSON."
    user = f"""Role needed: {body.role}
Location: {body.location}
Experience: {body.experience_years}+ years

Candidate data: {profiles_text}

Select the top 5 candidates. For each create:
{{
  "name": "string",
  "current_role": "string",
  "location": "string",
  "experience_summary": "string (one sentence)",
  "fit_score": "number 1-10",
  "fit_reason": "string (one sentence)",
  "outreach_line": "string (personalised 1-line opening message referencing something specific)",
  "profile_url": "string"
}}

Return a JSON array of 5 candidate objects."""

    parsed = claude.ask_claude_json(user, system)
    candidates: list[dict[str, Any]]
    if isinstance(parsed, list):
        candidates = [c for c in parsed if isinstance(c, dict)][:5]
    elif isinstance(parsed, dict) and isinstance(parsed.get("candidates"), list):
        candidates = [c for c in parsed["candidates"] if isinstance(c, dict)][:5]
    else:
        logger.warning("Unexpected Claude talent JSON shape — using first mock profiles")
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
        doc_id = firebase.create_document(
            "candidates",
            {
                "role": body.role,
                "location": body.location,
                "experience_years": body.experience_years,
                "candidates": candidates,
            },
        )
    except Exception as e:  # noqa: BLE001
        logger.warning("Candidates Firestore write skipped: %s", e)

    return {"success": True, "id": doc_id, "candidates": candidates}
