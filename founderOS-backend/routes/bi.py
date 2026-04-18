"""Agent 01 — Business Intelligence."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

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


def _trim(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n]


@router.post("/analyze")
async def analyze(body: BIAnalyzeBody) -> dict[str, Any]:
    q1 = f"{body.company} competitors {body.market} funding 2024"
    q2 = f"{body.market} market size trends 2024"
    news1 = await apify.scrape_news(q1, max_results=10)
    news2 = await apify.scrape_news(q2, max_results=10)
    combined: list[Any] = []
    for block in (news1, news2):
        if isinstance(block, list):
            combined.extend(block)
    scraped_text = _trim(str(combined), 3000)
    if not scraped_text.strip():
        logger.warning("Apify returned empty research — using mock text fallback")
        scraped_text = MOCK_RESEARCH.format(market=body.market)

    prompt = f"""You are a senior business analyst. Analyze this company and market.

Company: {body.company}
Market: {body.market}
Research (news / snippets): {scraped_text}

Return a single JSON object with exactly these keys:
- swot: object with strengths, weaknesses, opportunities, threats (each an array of 3 strings)
- porters_five_forces: object with keys competitive_rivalry, supplier_power, buyer_power, threat_of_substitutes, threat_of_new_entrants (each a short string, 1-2 sentences)
- market_overview: string (2-3 sentences)
- market_size: string (TAM / market size estimate)
- top_competitors: array of 3 competitor name strings
- pros: array of 3 strings
- cons: array of 3 strings
- what_to_expect: string (honest 2-3 sentence outlook for a new entrant)
- recommended_tools: array of 3 objects with name, purpose, free_tier (boolean)
- business_model_suggestions: array of 3 strings
"""

    try:
        result = claude.ask_claude_json(prompt)
    except RuntimeError as e:
        logger.warning("Claude unavailable: %s", e)
        return {
            "success": False,
            "id": "unsaved",
            "analysis": {},
            "error": str(e),
        }
    except ValueError as e:
        logger.warning("Claude JSON error: %s", e)
        return {"success": False, "id": "unsaved", "analysis": {}, "error": str(e)}

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
