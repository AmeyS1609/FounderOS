"""
Write one sample row per collection using create_document() (auto ids + created_at).

Run from repository root:
  python backend/scripts/seed_firestore_samples.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from backend.services import firebase  # noqa: E402


def main() -> None:
    firebase.init_firebase()

    rows = [
        (
            "briefings",
            {
                "company": "Acme Demo Co",
                "market": "B2B SaaS",
                "analysis": {"note": "seed via create_document"},
                "_founderos_seed": True,
            },
        ),
        (
            "emails",
            {
                "gmail_message_id": "seed-gmail-demo-id",
                "subject": "Seed email",
                "sender": "seed@example.com",
                "date": "Mon, 1 Jan 2026 12:00:00 +0000",
                "draft_reply": "Thanks — seed row.",
                "is_meeting_request": False,
                "calendar_suggestion": "",
                "status": "pending",
                "_founderos_seed": True,
            },
        ),
        (
            "leads",
            {
                "transcript": "x" * 60 + " seed transcript.",
                "caller": {"name": "Seed Lead"},
                "duration_seconds": 120,
                "fit_score": 7,
                "lead_summary": "Seed lead document.",
                "status": "new",
                "bant": {},
                "_founderos_seed": True,
            },
        ),
        (
            "candidates",
            {
                "role": "Founding Engineer",
                "location": "Remote",
                "experience_years": 5,
                "candidates": [{"name": "Seed Candidate", "profile_url": ""}],
                "_founderos_seed": True,
            },
        ),
        (
            "conversations",
            {
                "question": "What is FounderOS?",
                "answer": "An AI operating system for solo entrepreneurs.",
                "confidence": "high",
                "needs_training": False,
                "_founderos_seed": True,
            },
        ),
    ]

    for coll, payload in rows:
        doc_id = firebase.create_document(coll, payload)
        print(f"seeded {coll}/{doc_id}")


if __name__ == "__main__":
    main()
