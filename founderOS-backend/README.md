# FounderOS Backend

FastAPI service for FounderOS: BI analysis, email, talent search, leads webhook, and CS bot routes. Deploy target: **Render** (see repo root `README.md` and `../founderOS/DEPLOY.md`).

**Live UI (Netlify):** [https://rococo-zabaione-7e5b62.netlify.app](https://rococo-zabaione-7e5b62.netlify.app)

---

## Requirements

- Python **3.12** (see `runtime.txt`)
- pip

---

## Setup

```powershell
cd founderOS-backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit **`.env`** (never commit real secrets). Copy `firebase-service-account.json` into this folder for local use, **or** set `FIREBASE_SERVICE_ACCOUNT_JSON` (recommended on Render).

---

## Run locally

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- Env probe (no secret values): [http://127.0.0.1:8000/env-check](http://127.0.0.1:8000/env-check)

---

## Environment variables

See **`.env.example`** for the full list. Commonly:

| Variable | Purpose |
|----------|---------|
| `FRONTEND_URL` | Browser origin for CORS (e.g. `http://localhost:3000` locally, your Netlify URL in prod) |
| `ANTHROPIC_API_KEY` | Claude / BI and agent routes |
| `APIFY_TOKEN` | News / research scrape |
| `RAPIDAPI_KEY` | Talent / LinkedIn-style search |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | **Preferred in production** — full service account JSON string |
| `FIREBASE_SERVICE_ACCOUNT_PATH` | Local path to JSON file if JSON env unset |
| `GMAIL_CLIENT_ID` / `GMAIL_CLIENT_SECRET` | Optional live Gmail |

Optional CORS tuning: `CORS_EXTRA_ORIGINS`, `CORS_ORIGIN_REGEX` (see `.env.example`).

---

## API route map (prefixes)

| Prefix | Examples |
|--------|----------|
| `/api/bi` | `POST /api/bi/analyze` |
| `/api/email` | `GET /api/email/inbox`, `POST /api/email/approve` |
| `/api/talent` | `POST /api/talent/search` |
| `/api/leads` | `POST /api/leads/webhook`, `GET /api/leads/all` |
| `/api/csbot` | `POST /api/csbot/message`, `GET /api/csbot/training-queue`, `POST /api/csbot/train` |

---

## Smoke tests

From this directory:

```powershell
python test_all.py
```

---

## Production (Render)

- **Root directory:** `founderOS-backend`
- **Build:** `pip install -r requirements.txt`
- **Start:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Health check path:** `/health`

Details: **`../founderOS/DEPLOY.md`**.
