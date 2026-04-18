"""
Verify at least one seeded row exists per collection (``_founderos_seed`` == true).

Run from repository root:
  python backend/scripts/verify_firestore_reads.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from backend.services.firebase import get_db, init_firebase  # noqa: E402

COLLECTIONS = ("briefings", "emails", "leads", "candidates", "conversations")


def main() -> int:
    init_firebase()
    db = get_db()
    ok = True
    for name in COLLECTIONS:
        try:
            q = db.collection(name).where("_founderos_seed", "==", True).limit(1)
            docs = list(q.stream())
        except Exception as e:  # noqa: BLE001
            print(f"{name}: query FAIL {e}")
            ok = False
            continue
        exists = len(docs) > 0
        print(f"{name}: seeded_row_exists={exists}")
        if not exists:
            ok = False
    print("VERIFY:", "PASS" if ok else "FAIL (run seed_firestore_samples.py)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
