"""
Insert one sample row per collection via create_document(), read each back, print results.

Run from repo root:
  python backend/scripts/firestore_roundtrip_test.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from backend.services import firebase  # noqa: E402


def main() -> int:
    firebase.init_firebase()
    db = firebase.get_db()

    samples: list[tuple[str, dict]] = [
        (
            "briefings",
            {"company": "Roundtrip Co", "market": "Test", "analysis": {"ok": True}},
        ),
        (
            "emails",
            {
                "gmail_message_id": "roundtrip-seed-gmail-id",
                "subject": "Roundtrip",
                "sender": "t@example.com",
                "date": "Mon, 1 Jan 2026 00:00:00 +0000",
                "draft_reply": "hi",
                "is_meeting_request": False,
                "calendar_suggestion": "",
                "status": "pending",
            },
        ),
        (
            "leads",
            {
                "transcript": "x" * 55,
                "caller": {},
                "duration_seconds": 0,
                "bant": {},
                "fit_score": 5,
                "status": "new",
                "lead_summary": "roundtrip",
            },
        ),
        (
            "candidates",
            {
                "role": "Eng",
                "location": "Remote",
                "experience_years": 3,
                "candidates": [{"name": "A", "profile_url": ""}],
            },
        ),
        (
            "conversations",
            {
                "question": "ping?",
                "answer": "pong",
                "confidence": "high",
                "needs_training": False,
            },
        ),
    ]

    ids: dict[str, str] = {}
    for coll, payload in samples:
        try:
            doc_id = firebase.create_document(coll, payload)
            ids[coll] = doc_id
            snap = db.collection(coll).document(doc_id).get()
            data = snap.to_dict() or {}
            print(f"{coll}: id={doc_id} exists={snap.exists} sample_keys={list(data.keys())[:6]}")
        except Exception as e:  # noqa: BLE001
            print(f"{coll}: FAIL {e}")
            return 1

    print("Roundtrip OK for:", ", ".join(f"{k}={v}" for k, v in ids.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
