# FounderOS — Render + Netlify

This repo keeps the backend in `founderOS-backend/` and the Vite app in `frontend/` (treat it as **founderOS-frontend** in Netlify by setting the site root to `frontend`).

## 1. Render (backend)

| Field | Value |
|--------|--------|
| **Root directory** | `founderOS-backend` |
| **Build command** | `pip install -r requirements.txt` |
| **Start command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Health check path** | `/health` |

**Environment variables (Render)**

| Variable | Required | Notes |
|----------|-----------|--------|
| `PORT` | Auto | Render injects this; do not set manually unless you know why. |
| `FRONTEND_URL` | Strongly recommended | Your Netlify URL, e.g. `https://your-site.netlify.app`. Comma-separated for multiple. |
| `ANTHROPIC_API_KEY` | For live BI / agents | |
| `APIFY_TOKEN` | For news scrape | |
| `RAPIDAPI_KEY` | For talent / LinkedIn | |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Recommended on Render | Full JSON string (secret). Safer than committing a file. |
| `FIREBASE_SERVICE_ACCOUNT_PATH` | Local / optional | Path to JSON file; used if JSON env is unset. |
| `GMAIL_CLIENT_ID` | Optional | Live Gmail |
| `GMAIL_CLIENT_SECRET` | Optional | Live Gmail |
| `CORS_EXTRA_ORIGINS` | Optional | Comma-separated extra allowed origins. |
| `CORS_ORIGIN_REGEX` | Optional | Default matches `https://*.netlify.app`. Set to empty to disable regex CORS. |

Optional: connect the repo and use the root **`render.yaml`** blueprint (same settings).

## 2. Netlify (frontend)

| Field | Value |
|--------|--------|
| **Base directory** | `frontend` |
| **Build command** | `npm run build` |
| **Publish directory** | `frontend/dist` (or `dist` if Netlify base is already `frontend`) |

`frontend/netlify.toml` sets `publish = "dist"` and SPA fallback to `index.html`.

**Environment variables (Netlify — build time)**

| Variable | Notes |
|----------|--------|
| `VITE_API_BASE_URL` | Your Render URL, e.g. `https://founderos-backend.onrender.com` — **no trailing slash**. |

Vite bakes `VITE_*` into the client at **build** time; change the var → trigger a new deploy.

## 3. Firebase on Render

- **Avoid** relying on a committed `firebase-service-account.json` on ephemeral disks.
- **Preferred:** create a Render **Secret** (or paste in Environment) as `FIREBASE_SERVICE_ACCOUNT_JSON` = full single-line JSON from Firebase Console → Service accounts → Generate new private key.
- **Alternative:** Render **Secret File** mounted to a path, then set `FIREBASE_SERVICE_ACCOUNT_PATH` to that path (not covered in code beyond normal file read).

## 4. Local development

1. **Backend:** from `founderOS-backend/`, copy `.env.example` → `.env`, fill keys, then:
   - `pip install -r requirements.txt`
   - `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
2. **Frontend:** from `frontend/`, copy `.env.example` → `.env`:
   - `VITE_API_BASE_URL=http://127.0.0.1:8000`
   - `npm install` && `npm run dev` (Vite default port 5173; already allowed in backend CORS).

## 5. Production flow

1. Deploy backend on Render; confirm `GET https://<render-host>/health` returns `"ok": true`.
2. Set Render `FRONTEND_URL` to your Netlify URL.
3. In Netlify, set `VITE_API_BASE_URL` to the Render URL, deploy site.
4. Smoke-test: open Intel → **Execute Analysis** (calls `POST /api/bi/analyze`).

## 6. Risks / follow-ups

- **Cold start:** Free Render tier sleeps; first request may be slow.
- **CORS:** Custom domains on Netlify must be listed in `FRONTEND_URL` or `CORS_EXTRA_ORIGINS` (the default regex only matches `*.netlify.app`).
- **Secrets in logs:** Never log API keys; `/env-check` only reports set/missing.

## 7. Files touched for this setup

- `founderOS-backend/main.py` — logging, CORS (origins + Netlify regex), lifespan, `/health`, `/env-check`
- `founderOS-backend/services/firebase.py` — `FIREBASE_SERVICE_ACCOUNT_JSON`, `is_configured()`
- `founderOS-backend/.env.example`, `Procfile`, `runtime.txt`
- `render.yaml` (repo root)
- `frontend/netlify.toml`, `frontend/.env.example`, `frontend/src/lib/api.ts`, `frontend/src/App.tsx` (Intel → live API)
