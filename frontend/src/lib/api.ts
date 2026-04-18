/**
 * API base URL (Vite injects `import.meta.env` at build time).
 *
 * Modes:
 * - **Local:** set `VITE_API_BASE_URL=http://127.0.0.1:8000` in `frontend/.env`
 * - **Production (direct):** Netlify env `VITE_API_BASE_URL=https://your-api.up.railway.app` (no trailing slash)
 * - **Production (proxy):** leave `VITE_API_BASE_URL` unset; set Netlify **build** env
 *   `BACKEND_PUBLIC_URL=https://your-api...` so `prebuild` writes `_redirects` to proxy `/api/*`
 *   → same-origin fetches use base `''`
 */
function stripTrailingSlash(s: string): string {
  return s.replace(/\/$/, '');
}

function isLocalApiUrl(u: string): boolean {
  try {
    const { hostname } = new URL(u);
    return hostname === 'localhost' || hostname === '127.0.0.1';
  } catch {
    return false;
  }
}

export function getApiBaseUrl(): string {
  const raw = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim();
  const prod = import.meta.env.PROD;

  if (raw && !(prod && isLocalApiUrl(raw))) {
    return stripTrailingSlash(raw);
  }

  if (prod) {
    if (raw && isLocalApiUrl(raw)) {
      console.error(
        '[FounderOS] VITE_API_BASE_URL points at localhost — browsers will not reach your machine. ' +
          'Set Netlify `VITE_API_BASE_URL` to your public Railway/Render URL, or use `BACKEND_PUBLIC_URL` + same-origin `/api` proxy (see README).',
      );
    }
    return '';
  }

  return 'http://127.0.0.1:8000';
}

export function apiUrl(path: string): string {
  const base = getApiBaseUrl();
  const p = path.startsWith('/') ? path : `/${path}`;
  if (!base) {
    return p;
  }
  return `${base}${p}`;
}

export async function apiFetch(
  path: string,
  init?: RequestInit,
): Promise<Response> {
  return fetch(apiUrl(path), {
    ...init,
    headers: {
      Accept: 'application/json',
      ...init?.headers,
    },
  });
}
