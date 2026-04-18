"""Firebase Admin SDK and Firestore."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
from google.api_core.exceptions import PermissionDenied
from google.cloud.firestore import SERVER_TIMESTAMP

_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env", override=True)
load_dotenv(override=True)

logger = logging.getLogger(__name__)

db: firestore.Client | None = None


def _service_account_path() -> Path:
    raw = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "./firebase-service-account.json")
    return Path(raw).expanduser().resolve()


def init_firebase() -> firestore.Client:
    """Initialize Firebase Admin once and set global db."""
    global db
    if db is not None:
        return db

    path = _service_account_path()
    if not path.is_file():
        msg = (
            f"Firebase service account file not found at {path}. "
            "Download it from Firebase Console → Project Settings → Service Accounts → Generate new private key"
        )
        raise RuntimeError(msg)

    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(str(path))
        except ValueError as e:
            raise RuntimeError(
                f"Invalid Firebase service account JSON at {path}: {e}. "
                'Use the full JSON key from Firebase Console (must include "type": "service_account").'
            ) from e
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db


def get_db() -> firestore.Client:
    if db is None:
        return init_firebase()
    return db


def check_permissions() -> bool:
    """
    Try a Firestore write. On PermissionDenied, print common causes and fixes, then re-raise.
    """
    try:
        init_firebase()
        c = get_db().collection("_permission_probe").document("probe")
        c.set({"ok": True}, merge=True)
        c.delete()
        return True
    except PermissionDenied:
        print(
            "CAUSE 1: Service account file is wrong or corrupted\n"
            "FIX: Re-download from Firebase Console → Project Settings → Service Accounts → Generate new private key\n"
            "\n"
            "CAUSE 2: Service account missing IAM roles\n"
            'FIX: Go to Google Cloud Console → IAM → find your service account email → add role "Cloud Datastore User"\n'
            "\n"
            "CAUSE 3: Wrong Firebase project\n"
            "FIX: Check that your service account JSON file is from the SAME project as your Firestore database\n"
        )
        raise


def test_connection() -> bool:
    """Write/read/delete a health document; return True if successful."""
    init_firebase()
    ref = get_db().collection("health").document("ping")
    ref.set({"test": True})
    snap = ref.get()
    data = snap.to_dict() or {}
    ok = snap.exists and data.get("test") is True
    ref.delete()
    return bool(ok)


__all__ = [
    "SERVER_TIMESTAMP",
    "db",
    "init_firebase",
    "get_db",
    "check_permissions",
    "test_connection",
]
