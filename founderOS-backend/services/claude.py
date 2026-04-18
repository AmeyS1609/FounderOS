"""Anthropic Claude client — FounderOS."""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any

from anthropic import Anthropic
from dotenv import load_dotenv

_APP_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_APP_ROOT / ".env", override=True)
load_dotenv(override=True)

logger = logging.getLogger(__name__)

_client: Anthropic | None = None
_DEFAULT_MODEL = "claude-sonnet-4-20250514"
_DEFAULT_SYSTEM = "You are an expert assistant for FounderOS, an AI operating system for solo entrepreneurs."


def _model() -> str:
    return (os.getenv("CLAUDE_MODEL") or _DEFAULT_MODEL).strip().strip('"').strip("'")


def _client_anthropic() -> Anthropic:
    global _client
    if _client is None:
        key = (os.getenv("ANTHROPIC_API_KEY") or "").strip().strip('"').strip("'")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        _client = Anthropic(api_key=key)
    return _client


def _call_messages(*, system: str, user: str, max_tokens: int = 4096) -> str:
    client = _client_anthropic()
    msg = client.messages.create(
        model=_model(),
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    parts: list[str] = []
    for block in msg.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    if parts:
        return "".join(parts)
    return str(msg.content[0])


def ask_claude(prompt: str) -> str:
    """Single-call text completion. Put role instructions inside *prompt* if needed."""
    return _call_messages(system=_DEFAULT_SYSTEM, user=prompt, max_tokens=2048)


def _strip_markdown_fences(text: str) -> str:
    s = text.strip()
    s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```\s*$", "", s, flags=re.IGNORECASE)
    return s.strip()


def ask_claude_json(prompt: str) -> dict[str, Any]:
    """
    Ask Claude for a JSON object. The *prompt* must describe the exact JSON shape.
    Root-level JSON arrays are wrapped as {"items": [...]} so return type is always dict.
    """
    sys = (
        _DEFAULT_SYSTEM
        + " Always respond with valid JSON only. No markdown fences, no commentary."
    )
    raw = _call_messages(system=sys, user=prompt, max_tokens=4096)
    cleaned = _strip_markdown_fences(raw)
    try:
        out = json.loads(cleaned)
    except json.JSONDecodeError:
        m_obj = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not m_obj:
            m_arr = re.search(r"\[.*\]", cleaned, re.DOTALL)
            if m_arr:
                try:
                    arr = json.loads(m_arr.group(0))
                    if isinstance(arr, list):
                        return {"items": arr}
                except json.JSONDecodeError:
                    pass
            logger.error("Claude JSON parse failure; raw (truncated): %s", raw[:500])
            raise ValueError("Claude did not return valid JSON: " + raw[:200]) from None
        try:
            out = json.loads(m_obj.group(0))
        except json.JSONDecodeError as e:
            logger.error("Claude JSON parse failure; raw (truncated): %s", raw[:500])
            raise ValueError("Claude did not return valid JSON: " + raw[:200]) from e

    if isinstance(out, list):
        return {"items": out}
    if isinstance(out, dict):
        return out
    raise ValueError("Claude JSON root must be object or array")
