"""
Firestore collection schemas — FounderOS backend.

Every *new* row is created with ``collection.add({...})`` and includes
``created_at: SERVER_TIMESTAMP`` (injected by ``create_document`` if omitted).

--------------------------------------------------------------------
briefings
--------------------------------------------------------------------
  company          str     Company name analyzed
  market           str     Market segment
  analysis         dict    Full Claude JSON (SWOT, tools, etc.)
  created_at       TS      Server timestamp

--------------------------------------------------------------------
emails
--------------------------------------------------------------------
  gmail_message_id str|None Gmail API message id (for dedupe / lookup)
  subject          str
  sender           str
  date             str     RFC822-style date string from Gmail
  draft_reply      str
  is_meeting_request bool
  calendar_suggestion str  May be empty
  status           str     pending | approved
  final_reply      str|None Set when approved
  created_at       TS
  updated_at       TS|None Set on approval merge

  Primary key for API responses: Firestore auto id (field ``id`` in JSON).

--------------------------------------------------------------------
leads
--------------------------------------------------------------------
  transcript       str
  caller           dict    Arbitrary caller metadata
  duration_seconds int
  bant               dict    Claude BANT JSON (may be {})
  fit_score          int     1–10
  status             str     e.g. new
  lead_summary       str|None Short summary (short-transcript path)
  raw_payload        dict|None Original webhook body when applicable
  created_at         TS

--------------------------------------------------------------------
candidates
--------------------------------------------------------------------
  role               str
  location           str
  experience_years   int
  candidates         list    Ranked candidate dicts from Claude
  created_at         TS

--------------------------------------------------------------------
conversations
--------------------------------------------------------------------
  question           str
  answer             str
  confidence         str     high | low
  needs_training     bool
  created_at         TS
  correct_answer     str|None From POST /train
  trained            bool|None
  trained_at         datetime|TS|None
  updated_at         TS|None Set on training merge

  conversation_id in API = Firestore document id from ``add``.
"""

from __future__ import annotations

COLLECTION_BRIEFINGS = "briefings"
COLLECTION_EMAILS = "emails"
COLLECTION_LEADS = "leads"
COLLECTION_CANDIDATES = "candidates"
COLLECTION_CONVERSATIONS = "conversations"

__all__ = [
    "COLLECTION_BRIEFINGS",
    "COLLECTION_EMAILS",
    "COLLECTION_LEADS",
    "COLLECTION_CANDIDATES",
    "COLLECTION_CONVERSATIONS",
]
