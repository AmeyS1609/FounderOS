/**
 * Single source for backend API base URL + fetch helpers.
 *
 * **Local:** `frontend/.env` → `VITE_API_BASE_URL=http://localhost:8000` (or leave unset + use Vite proxy, see vite.config.ts)
 * **Netlify production:** set `VITE_API_BASE_URL=https://YOUR-SERVICE.onrender.com` (no trailing slash), **or**
 *   set build env `BACKEND_PUBLIC_URL` and use same-origin `/api` proxy (`scripts/write-redirects.mjs`).
 *
 * Alias env: `VITE_API_URL` (same meaning as `VITE_API_BASE_URL`).
 */

const DEBUG =
  import.meta.env.DEV || String(import.meta.env.VITE_API_DEBUG || '').toLowerCase() === 'true';

function stripTrailingSlash(s: string): string {
  return s.replace(/\/$/, '');
}

function firstEnv(...keys: (keyof ImportMetaEnv)[]): string | undefined {
  for (const k of keys) {
    const raw = import.meta.env[k];
    const v = typeof raw === 'string' ? raw.trim() : '';
    if (v) return v;
  }
  return undefined;
}

function isLocalApiUrl(u: string): boolean {
  try {
    const { hostname } = new URL(u);
    return hostname === 'localhost' || hostname === '127.0.0.1';
  } catch {
    return false;
  }
}

/**
 * Resolved API origin (empty string = same-origin relative URLs; use with Netlify/Vite proxy).
 */
export function getApiBaseUrl(): string {
  const raw = firstEnv('VITE_API_BASE_URL', 'VITE_API_URL');
  const prod = import.meta.env.PROD;

  if (raw && !(prod && isLocalApiUrl(raw))) {
    return stripTrailingSlash(raw);
  }

  if (prod && raw && isLocalApiUrl(raw)) {
    console.error(
      '[FounderOS] VITE_API_BASE_URL / VITE_API_URL points at localhost in production. ' +
        'Set Netlify to your Render HTTPS URL, or use BACKEND_PUBLIC_URL proxy (see README).',
    );
  }

  if (prod) {
    return '';
  }

  // Dev: explicit URL wins; otherwise same-origin + Vite proxy (see vite.config.ts)
  return '';
}

/** Short label for UI (never contains secrets). */
export function getApiOriginLabel(): string {
  const b = getApiBaseUrl();
  if (b) return b;
  return import.meta.env.PROD ? 'same-origin (/api proxy)' : 'same-origin (Vite dev proxy)';
}

export function apiUrl(path: string): string {
  const base = getApiBaseUrl();
  const p = path.startsWith('/') ? path : `/${path}`;
  if (!base) return p;
  return `${base}${p}`;
}

function mergeHeaders(init?: RequestInit): Headers {
  const h = new Headers();
  h.set('Accept', 'application/json');
  if (init?.headers) {
    const extra = new Headers(init.headers as HeadersInit);
    extra.forEach((v, k) => h.set(k, v));
  }
  return h;
}

function logApi(direction: 'request' | 'response', url: string, info: Record<string, unknown>) {
  if (!DEBUG) return;
  // eslint-disable-next-line no-console
  console.info(`[FounderOS API] ${direction}`, url, info);
}

/**
 * Low-level fetch to the API (relative when base is empty).
 */
export async function apiFetch(path: string, init?: RequestInit): Promise<Response> {
  const url = apiUrl(path);
  const method = (init?.method || 'GET').toUpperCase();
  const headers = mergeHeaders(init);
  const body = init?.body;
  if (
    body &&
    typeof body === 'string' &&
    body.trimStart().startsWith('{') &&
    !headers.has('Content-Type')
  ) {
    headers.set('Content-Type', 'application/json');
  }

  logApi('request', url, { method, hasBody: Boolean(body) });
  if (DEBUG && typeof body === 'string' && body.length < 2000) {
    // eslint-disable-next-line no-console
    console.info('[FounderOS API] body', body);
  }

  let res: Response;
  try {
    res = await fetch(url, { ...init, headers });
  } catch (e) {
    // eslint-disable-next-line no-console
    console.error('[FounderOS API] network error', url, e);
    throw e instanceof Error ? e : new Error('Network request failed');
  }

  const ct = res.headers.get('content-type') || '';
  logApi('response', url, { status: res.status, contentType: ct });

  if (!res.ok && ct.includes('text/html')) {
    const snippet = (await res.clone().text()).slice(0, 200);
    throw new Error(
      `Got HTML instead of JSON (${res.status}) for ${url}. ` +
        'Usually means the SPA served index.html — set Netlify VITE_API_BASE_URL to your Render URL, ' +
        `or set BACKEND_PUBLIC_URL so /api proxies correctly. Snippet: ${snippet.replace(/\s+/g, ' ').slice(0, 120)}…`,
    );
  }

  return res;
}

/**
 * Parse JSON response; throws with body preview on non-JSON or HTTP errors.
 */
export async function apiJson<T = unknown>(path: string, init?: RequestInit): Promise<T> {
  const res = await apiFetch(path, init);
  const text = await res.text();
  const ct = res.headers.get('content-type') || '';

  if (!ct.includes('application/json')) {
    if (text.trimStart().startsWith('<!') || text.trimStart().startsWith('<html')) {
      throw new Error(
        `Non-JSON response from ${path} (${res.status}). Likely Netlify returned HTML — check VITE_API_BASE_URL / BACKEND_PUBLIC_URL.`,
      );
    }
    throw new Error(`Expected JSON from ${path} (${res.status}), got: ${ct || 'unknown type'}. Body: ${text.slice(0, 240)}`);
  }

  let data: T;
  try {
    data = JSON.parse(text) as T;
  } catch {
    throw new Error(`Invalid JSON from ${path} (${res.status}): ${text.slice(0, 240)}`);
  }

  if (!res.ok) {
    const err = data as { detail?: unknown };
    const detail =
      typeof err.detail === 'string'
        ? err.detail
        : Array.isArray(err.detail)
          ? JSON.stringify(err.detail)
          : text.slice(0, 300);
    throw new Error(detail || `HTTP ${res.status}`);
  }

  return data;
}

export async function fetchBackendHealth(): Promise<{ ok?: boolean } | null> {
  try {
    return await apiJson<Record<string, unknown>>('/health');
  } catch (e) {
    if (DEBUG) {
      // eslint-disable-next-line no-console
      console.warn('[FounderOS API] /health failed', e);
    }
    return null;
  }
}
