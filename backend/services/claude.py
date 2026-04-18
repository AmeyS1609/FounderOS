"""Anthropic Claude client."""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any

from anthropic import Anthropic
from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env", override=True)
load_dotenv(override=True)

logger = logging.getLogger(__name__)

_client: Anthropic | None = None

_DEFAULT_FALLBACK = "claude-sonnet-4-20250514"


def _model() -> str:
    return (os.getenv("CLAUDE_MODEL") or _DEFAULT_FALLBACK).strip().strip('"').strip("'")


def _client_anthropic() -> Anthropic:
    global _client
    if _client is None:
        key = (os.getenv("ANTHROPIC_API_KEY") or "").strip().strip('"').strip("'")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        _client = Anthropic(api_key=key)
    return _client


def ask_claude(prompt: str, system: str) -> str:
    """Call Claude with system + user prompt; return assistant text."""
    client = _client_anthropic()
    msg = client.messages.create(
        model=_model(),
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    parts: list[str] = []
    for block in msg.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    if parts:
        return "".join(parts)
    return str(msg.content[0])


def _strip_markdown_fences(text: str) -> str:
    s = text.strip()
    s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```\s*$", "", s, flags=re.IGNORECASE)
    return s.strip()


def ask_claude_json(prompt: str, system: str) -> dict[str, Any] | list[Any]:
    """
    Ask for JSON: extend system prompt, strip fences, try json.loads, then regex object/array.
    """
    sys_full = (
        system.strip()
        + " Respond with valid JSON only. No markdown. No backticks."
    )
    raw = ask_claude(prompt, sys_full)
    cleaned = _strip_markdown_fences(raw)
    try:
        out = json.loads(cleaned)
        if isinstance(out, (dict, list)):
            return out
    except json.JSONDecodeError:
        pass
    m_obj = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if m_obj:
        try:
            out = json.loads(m_obj.group(0))
            if isinstance(out, dict):
                return out
        except json.JSONDecodeError:
            pass
    m_arr = re.search(r"\[.*\]", cleaned, re.DOTALL)
    if m_arr:
        try:
            out = json.loads(m_arr.group(0))
            if isinstance(out, list):
                return out
        except json.JSONDecodeError:
            pass
    logger.error("Claude JSON parse failure; raw (truncated): %s", raw[:500])
    raise ValueError("Claude did not return valid JSON: " + raw[:200])
