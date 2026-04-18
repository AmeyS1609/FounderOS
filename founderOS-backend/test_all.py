"""FounderOS backend smoke + integration checks (no secret values printed)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

os.chdir(_ROOT)

from dotenv import load_dotenv

load_dotenv(_ROOT / ".env", override=True)
load_dotenv(override=True)


def _check(name: str, cond: bool, detail: str = "") -> bool:
    status = "OK" if cond else "FAIL"
    extra = f" — {detail}" if detail else ""
    print(f"[{status}] {name}{extra}")
    return cond


def main() -> int:
    ok_all = True

    keys = (
        "ANTHROPIC_API_KEY",
        "APIFY_TOKEN",
        "RAPIDAPI_KEY",
        "FIREBASE_SERVICE_ACCOUNT_PATH",
        "FIREBASE_SERVICE_ACCOUNT_JSON",
        "GMAIL_CLIENT_ID",
        "GMAIL_CLIENT_SECRET",
        "FRONTEND_URL",
        "PORT",
    )
    optional = {
        "GMAIL_CLIENT_ID",
        "GMAIL_CLIENT_SECRET",
        "FRONTEND_URL",
        "PORT",
        "APIFY_TOKEN",
        "RAPIDAPI_KEY",
        "FIREBASE_SERVICE_ACCOUNT_PATH",
        "FIREBASE_SERVICE_ACCOUNT_JSON",
    }
    for k in keys:
        present = bool((os.getenv(k) or "").strip())
        if k in optional:
            _check(f"env {k} (optional)", True, "present" if present else "ok without (mock / skip)")
        elif k == "ANTHROPIC_API_KEY":
            _check(f"env {k}", present, "required for Claude routes" if present else "missing — BI/talent/leads/csbot live calls will fail")
            # do not fail whole suite on missing key in CI without secrets
        else:
            ok_all &= _check(f"env {k}", present)

    raw = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "./firebase-service-account.json")
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = (_ROOT / p).resolve()
    json_creds = bool((os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON") or "").strip())
    firebase_ok = json_creds or p.is_file()
    ok_all &= _check(
        "firebase credentials (file or FIREBASE_SERVICE_ACCOUNT_JSON)",
        firebase_ok,
        "JSON env set" if json_creds else str(p),
    )

    try:
        import main as app_main  # noqa: PLC0415

        app = app_main.app
        ok_all &= _check("import main:app", app.title == "FounderOS Backend", f"title={app.title!r}")
    except Exception as e:  # noqa: BLE001
        _check("import main:app", False, str(e))
        return 1

    paths = {getattr(r, "path", "") for r in app.router.routes}
    need = {
        "/",
        "/health",
        "/env-check",
        "/api/bi/analyze",
        "/api/email/inbox",
        "/api/email/approve",
        "/api/leads/webhook",
        "/api/leads/all",
        "/api/talent/search",
        "/api/csbot/message",
        "/api/csbot/training-queue",
        "/api/csbot/train",
    }
    missing = need - paths
    ok_all &= _check("routes registered", not missing, f"missing={missing}" if missing else "")

    try:
        from services import firebase  # noqa: PLC0415

        if firebase_ok:
            firebase.init_firebase()
            ok_all &= _check("firebase init_firebase", True)
        else:
            _check("firebase init_firebase", False, "skipped — no credentials")
    except Exception as e:  # noqa: BLE001
        ok_all &= _check("firebase init_firebase", False, str(e))

    from fastapi.testclient import TestClient  # noqa: PLC0415

    client = TestClient(app)

    r = client.get("/")
    ok_all &= _check("TestClient GET /", r.status_code == 200 and r.json().get("agents") == 5, str(r.status_code))

    r = client.get("/health")
    ok_all &= _check("TestClient GET /health", r.status_code == 200, str(r.status_code))

    r = client.get("/env-check")
    ok_all &= _check(
        "TestClient GET /env-check",
        r.status_code == 200 and "vars" in r.json(),
        str(r.status_code),
    )

    r = client.get("/openapi.json")
    ok_all &= _check("TestClient GET /openapi.json", r.status_code == 200, str(r.status_code))

    r = client.get("/docs")
    ok_all &= _check("TestClient GET /docs", r.status_code == 200, str(r.status_code))

    r = client.post("/api/leads/webhook", json={"transcript": "short"})
    ok_all &= _check(
        "POST /api/leads/webhook (short transcript)",
        r.status_code == 200 and r.json().get("status") == "success",
        str(r.status_code),
    )

    r = client.get("/api/leads/all")
    ok_all &= _check("GET /api/leads/all", r.status_code == 200 and "leads" in r.json(), str(r.status_code))

    r = client.get("/api/email/inbox")
    ok_all &= _check("GET /api/email/inbox (no auth)", r.status_code == 401, str(r.status_code))

    print("\nSummary:", "PASS" if ok_all else "SOME CHECKS FAILED (see above)")
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
