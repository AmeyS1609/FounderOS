"""Firebase Admin SDK and Firestore."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
from google.api_core.exceptions import PermissionDenied
from google.cloud.firestore import SERVER_TIMESTAMP

_APP_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_APP_ROOT / ".env", override=True)
load_dotenv(override=True)

logger = logging.getLogger(__name__)

db: firestore.Client | None = None


def _service_account_path() -> Path:
    raw = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "./firebase-service-account.json")
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = (_APP_ROOT / p).resolve()
    return p.resolve()


def is_configured() -> bool:
    """True if either inline JSON or a service account file path is available."""
    if os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip():
        return True
    return _service_account_path().is_file()


def _init_app_from_credentials() -> None:
    if firebase_admin._apps:
        return

    json_raw = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
    if json_raw:
        try:
            info = json.loads(json_raw)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                "FIREBASE_SERVICE_ACCOUNT_JSON is set but is not valid JSON. "
                "Paste the full service account JSON from Firebase Console as one line, "
                "or use a Render secret / shell-escaped string."
            ) from e
        if not isinstance(info, dict) or info.get("type") != "service_account":
            raise RuntimeError(
                'FIREBASE_SERVICE_ACCOUNT_JSON must decode to a JSON object with "type": "service_account".'
            )
        try:
            cred = credentials.Certificate(info)
        except ValueError as e:
            raise RuntimeError(f"Invalid Firebase service account fields: {e}") from e
        firebase_admin.initialize_app(cred)
        logger.info("Firebase initialized from FIREBASE_SERVICE_ACCOUNT_JSON")
        return

    path = _service_account_path()
    if not path.is_file():
        msg = (
            f"Firebase service account file not found at {path}. "
            "Set FIREBASE_SERVICE_ACCOUNT_JSON (recommended on Render) or "
            "FIREBASE_SERVICE_ACCOUNT_PATH in .env, or place firebase-service-account.json in founderOS-backend/."
        )
        raise RuntimeError(msg)

    try:
        cred = credentials.Certificate(str(path))
    except ValueError as e:
        raise RuntimeError(
            f"Invalid Firebase service account JSON at {path}: {e}. "
            'Use the full JSON key from Firebase Console (must include "type": "service_account").'
        ) from e
    firebase_admin.initialize_app(cred)
    logger.info("Firebase initialized from file %s", path)


def init_firebase() -> firestore.Client:
    """Initialize Firebase Admin once and set global db."""
    global db
    if db is not None:
        return db

    _init_app_from_credentials()
    db = firestore.client()
    return db


def get_db() -> firestore.Client:
    if db is None:
        return init_firebase()
    return db


def check_permissions() -> bool:
    try:
        init_firebase()
        c = get_db().collection("_permission_probe").document("probe")
        c.set({"ok": True}, merge=True)
        c.delete()
        return True
    except PermissionDenied:
        logger.exception("Firestore permission denied during probe")
        raise


def test_connection() -> bool:
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
    "is_configured",
]
