"""Firebase Admin SDK and Firestore."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
from google.api_core.exceptions import PermissionDenied
from google.cloud.firestore import SERVER_TIMESTAMP, Query

_ROOT = Path(__file__).resolve().parent.parent
_REPO = _ROOT.parent
load_dotenv(_REPO / ".env", override=True)
load_dotenv(_ROOT / ".env", override=True)
load_dotenv(override=True)

logger = logging.getLogger(__name__)

db: firestore.Client | None = None


def _service_account_path() -> Path:
    """
    Resolve service account JSON path.
    Relative paths are resolved from the *backend* package directory so
    FIREBASE_SERVICE_ACCOUNT_PATH=../firebase-service-account.json works when
    uvicorn is started from the repo root.
    """
    raw = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "./firebase-service-account.json")
    p = Path(raw).expanduser()
    if p.is_absolute():
        return p.resolve()
    return (_ROOT / p).resolve()


def credentials_file_ready() -> bool:
    try:
        return _service_account_path().is_file()
    except Exception:  # noqa: BLE001
        return False


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


def create_document(collection: str, data: dict[str, Any]) -> str:
    """
    Insert a new document with an auto-generated id and ``created_at`` server time.

    Returns the new document id. Raises on Firestore failure (after logging).
    """
    payload = dict(data)
    if "created_at" not in payload:
        payload["created_at"] = SERVER_TIMESTAMP
    try:
        _, ref = get_db().collection(collection).add(payload)
        return ref.id
    except Exception as e:  # noqa: BLE001
        logger.exception("Firestore add failed collection=%s", collection)
        raise RuntimeError(f"Firestore write failed: {e}") from e


def merge_document(collection: str, doc_id: str, data: dict[str, Any]) -> None:
    """Merge fields into an existing document (updates / approvals)."""
    try:
        get_db().collection(collection).document(doc_id).set(data, merge=True)
    except Exception as e:  # noqa: BLE001
        logger.exception("Firestore merge failed collection=%s id=%s", collection, doc_id)
        raise RuntimeError(f"Firestore update failed: {e}") from e


def get_all_documents(
    collection: str,
    *,
    limit: int = 200,
    order_by: str | None = "created_at",
    descending: bool = True,
) -> list[dict[str, Any]]:
    """
    List documents (each dict includes ``id`` = Firestore document id).
    Falls back to unordered scan + client sort if ``order_by`` fails.
    """
    col = get_db().collection(collection)
    try:
        if order_by:
            direction = Query.DESCENDING if descending else Query.ASCENDING
            snaps = list(col.order_by(order_by, direction=direction).limit(limit).stream())
        else:
            snaps = list(col.limit(limit).stream())
    except Exception as e:  # noqa: BLE001
        logger.warning("get_all_documents order_by failed (%s), using fallback", e)
        snaps = list(col.limit(min(limit, 500)).stream())
        snaps.sort(key=lambda s: (s.to_dict() or {}).get("created_at") or "", reverse=descending)
        snaps = snaps[:limit]

    out: list[dict[str, Any]] = []
    for s in snaps:
        row = dict(s.to_dict() or {})
        row["id"] = s.id
        out.append(row)
    return out


def find_first_document_id(collection: str, field: str, value: Any) -> str | None:
    """Return first matching document id, or None."""
    try:
        q = get_db().collection(collection).where(field, "==", value).limit(1)
        for snap in q.stream():
            return snap.id
    except Exception as e:  # noqa: BLE001
        logger.warning("find_first_document_id failed: %s", e)
    return None


def probe_firestore() -> dict[str, Any]:
    """
    Check credential file + Firestore read/write (single probe doc, then delete).
    Safe to call at startup; does not replace normal route error handling.
    """
    out: dict[str, Any] = {
        "credentials_file": False,
        "credentials_path": "",
        "connected": False,
        "detail": "",
        "project_id": "",
    }
    try:
        path = _service_account_path()
        out["credentials_path"] = str(path)
    except Exception as e:  # noqa: BLE001
        out["detail"] = f"path_error: {e}"
        return out

    if not path.is_file():
        out["detail"] = "service_account_file_missing"
        return out

    out["credentials_file"] = True
    try:
        client = init_firebase()

        try:
            app = firebase_admin.get_app()
            opt = getattr(app, "project_id", None)
            if opt:
                out["project_id"] = str(opt)
        except Exception:  # noqa: BLE001
            pass
        if not out["project_id"] and path.is_file():
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                out["project_id"] = str(raw.get("project_id", ""))
            except Exception:  # noqa: BLE001
                pass

        ref = client.collection("_health_probe").document("startup")
        ref.set({"ok": True, "probe": True, "ts": SERVER_TIMESTAMP})
        snap = ref.get()
        ok = snap.exists and (snap.to_dict() or {}).get("ok") is True
        ref.delete()
        if ok:
            out["connected"] = True
            out["detail"] = "read_write_ok"
        else:
            out["detail"] = "probe_read_unexpected"
    except Exception as e:  # noqa: BLE001
        out["detail"] = f"firestore_error: {e!r}"[:800]
        logger.warning("Firestore probe failed: %s", e)

    return out


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
    "create_document",
    "merge_document",
    "get_all_documents",
    "find_first_document_id",
    "credentials_file_ready",
    "probe_firestore",
    "check_permissions",
    "test_connection",
]
