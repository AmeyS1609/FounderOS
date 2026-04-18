# FounderOS Frontend

React + TypeScript **Vite** app for the FounderOS dashboard. Deploy target: **Netlify** (base directory = `frontend`). Parent docs: [repo root README](../README.md).

---

## App URL (local)

When you run the dev server, the UI is served at:

**[http://localhost:3000](http://localhost:3000)**

(`package.json` sets Vite to `--port=3000`.)

---

## Requirements

- **Node.js** (LTS recommended)
- npm

---

## Setup

```powershell
cd frontend
npm install
```

Create **`.env`** in this folder (see `.env.example`):

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Use your **Render** (or other) API URL in production — **no trailing slash**. This value is baked in at **build** time on Netlify.

---

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Dev server (host `0.0.0.0`, port **3000**) |
| `npm run build` | Production build → `dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Typecheck (`tsc --noEmit`) |

---

## Netlify

- **Base directory:** `frontend`
- **Build command:** `npm run build`
- **Publish directory:** `dist`

`netlify.toml` configures the build and SPA fallback (`/*` → `index.html`).

Site env (build): **`VITE_API_BASE_URL`** = your backend public URL.

---

## API client

Shared helpers live in **`src/lib/api.ts`** (`getApiBaseUrl`, `apiUrl`, `apiFetch`). Point `VITE_API_BASE_URL` at the FounderOS backend so features like **Intel → Execute Analysis** call the live API.

---

## Stack

- React 19, TypeScript, Vite 6  
- Tailwind CSS v4 (`@tailwindcss/vite`)  
- Motion, Lucide React  

---

## CORS (backend)

Ensure `founderOS-backend` has `FRONTEND_URL=http://localhost:3000` for local dev (or your deployed Netlify URL in production). See `../founderOS-backend/README.md`.
