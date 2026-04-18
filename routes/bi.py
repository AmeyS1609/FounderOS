"""Agent 01 — Business Intelligence."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from services import apify, claude, firebase

logger = logging.getLogger(__name__)

router = APIRouter()

MOCK_RESEARCH = (
    "Company analysis shows strong product-market fit in the {market} space. "
    "Key competitors include established players and new entrants. "
    "Market growing at 15% annually. Main risks are competition and customer acquisition cost."
)


class BIAnalyzeBody(BaseModel):
    company: str
    market: str
    use_mock: bool = Field(default=False, description="Skip Apify and use canned research text")


def _trim(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n]


@router.post("/analyze")
async def analyze(body: BIAnalyzeBody) -> dict[str, Any]:
    if body.use_mock:
        scraped_text = MOCK_RESEARCH.format(market=body.market)
    else:
        q1 = f"{body.company} competitors {body.market} funding 2024"
        q2 = f"{body.market} market size trends 2024"
        news1 = await apify.scrape_news(q1, max_results=10)
        news2 = await apify.scrape_news(q2, max_results=10)
        combined = []
        for block in (news1, news2):
            if isinstance(block, list):
                combined.extend(block)
        scraped_text = _trim(str(combined), 3000)
        if not scraped_text.strip():
            logger.warning("Apify returned empty research — using mock text fallback")
            scraped_text = MOCK_RESEARCH.format(market=body.market)

    system = "You are a senior business analyst. Return only valid JSON."
    user = f"""Analyze this company and market.
Company: {body.company}
Market: {body.market}
Research: {scraped_text}

Return JSON with exactly these keys:
{{
  "swot": {{ "strengths": [3 items], "weaknesses": [3 items], "opportunities": [3 items], "threats": [3 items] }},
  "market_overview": "string (2-3 sentences)",
  "market_size": "string (TAM estimate)",
  "top_competitors": [3 names],
  "pros": [3 strings],
  "cons": [3 strings],
  "what_to_expect": "string (honest 2-3 sentence market outlook for a new entrant)",
  "recommended_tools": [{{ "name", "purpose", "free_tier": bool }}] (3 tools relevant to this market),
  "business_model_suggestions": [3 strings]
}}"""

    result = claude.ask_claude_json(user, system)
    if not isinstance(result, dict):
        raise ValueError("BI analysis must be a JSON object")

    doc_id = "unsaved"
    try:
        db = firebase.get_db()
        doc = {
            "company": body.company,
            "market": body.market,
            "analysis": result,
            "created_at": firebase.SERVER_TIMESTAMP,
        }
        _, ref = db.collection("briefings").add(doc)
        doc_id = ref.id
    except Exception as e:  # noqa: BLE001
        logger.warning("Briefings Firestore write skipped: %s", e)

    return {"success": True, "id": doc_id, "analysis": result}
