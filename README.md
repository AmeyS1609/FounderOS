# FounderOS

Hackathon-ready **AI operating system** for founders: a **React + Vite** dashboard (`frontend/`) backed by a **FastAPI** service (`founderOS-backend/`) with agents for BI, email, talent, leads, and CS bot APIs.

**Live app (Netlify):** [https://rococo-zabaione-7e5b62.netlify.app](https://rococo-zabaione-7e5b62.netlify.app)

---

## App URLs

| Environment | App (UI) | API (backend) |
|-------------|----------|----------------|
| **Local (default)** | [http://localhost:3000](http://localhost:3000) | [http://127.0.0.1:8000](http://127.0.0.1:8000) |
| **Production** | [https://rococo-zabaione-7e5b62.netlify.app](https://rococo-zabaione-7e5b62.netlify.app) | Your Railway / Render public URL (see wiring above) |

For production wiring (pick **one** API strategy on Netlify):

**A — Direct API (simple)**  
1. Backend (Railway or Render): set **`FRONTEND_URL`** = `https://rococo-zabaione-7e5b62.netlify.app` (CORS).  
2. Netlify → **Environment variables** → add **`VITE_API_BASE_URL`** = your public API URL (e.g. `https://xxx.up.railway.app`), **no trailing slash** → **redeploy** (required so Vite bakes it in).

**B — Same-origin `/api` proxy (fewer CORS surprises)**  
1. Netlify → add **`BACKEND_PUBLIC_URL`** = your public API base (e.g. `https://xxx.up.railway.app`, no `/api` suffix).  
2. Leave **`VITE_API_BASE_URL` unset** (or delete it) so the app calls `/api/...` on the Netlify domain and Netlify proxies to the backend.  
3. Still set **`FRONTEND_URL`** on the backend if you call the API from other sites.

**If “UI loads but Intel / API does nothing”:** open DevTools → **Network** on `POST /api/bi/analyze`. Common causes: **`VITE_API_BASE_URL` missing** (build falls back to `localhost`), wrong backend URL, **CORS** (fix `FRONTEND_URL`), or **Firestore** not configured on the host (`/health` → `firestore.initialized: false` still allows BI, but briefing id stays `unsaved`).

Health check (local or prod): `GET /health` on the API base (e.g. [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)).

---

## Repository layout

| Path | Description |
|------|-------------|
| [`founderOS-backend/`](./founderOS-backend/) | FastAPI app — Render deployment target |
| [`frontend/`](./frontend/) | Vite + React UI — Netlify deployment target |
| [`founderOS/DEPLOY.md`](./founderOS/DEPLOY.md) | Render + Netlify env vars and checklist |
| [`render.yaml`](./render.yaml) | Optional Render blueprint (root → `founderOS-backend`) |

---

## Quick start (local)

**1. Backend**

```powershell
cd founderOS-backend
.\venv\Scripts\Activate.ps1   # if you use the project venv
pip install -r requirements.txt
copy .env.example .env        # then edit .env — see founderOS-backend/README.md
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**2. Frontend** (new terminal)

```powershell
cd frontend
npm install
# Create frontend/.env with: VITE_API_BASE_URL=http://127.0.0.1:8000
npm run dev
```

Open **[http://localhost:3000](http://localhost:3000)** (Vite is configured for port **3000**).  
Set `FRONTEND_URL=http://localhost:3000` in `founderOS-backend/.env` so CORS matches.

---

## Documentation

- **[founderOS-backend/README.md](./founderOS-backend/README.md)** — API, env vars, scripts, Firebase
- **[frontend/README.md](./frontend/README.md)** — UI stack, env vars, Netlify notes
- **[founderOS/DEPLOY.md](./founderOS/DEPLOY.md)** — production hosting (Render + Netlify)

---

## Tech stack (summary)

- **Frontend:** React 19, TypeScript, Vite 6, Tailwind CSS v4, Motion, Lucide
- **Backend:** FastAPI, Uvicorn, Anthropic, Apify, RapidAPI, Firebase Admin / Firestore, Gmail APIs (optional)

---

## License

See individual packages and SPDX headers in source files where noted.
