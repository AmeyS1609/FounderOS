/**
 * API base URL: Vite injects import.meta.env at build time.
 * Local: create frontend/.env with VITE_API_BASE_URL=http://127.0.0.1:8000
 * Netlify: Site settings → Environment variables → VITE_API_BASE_URL=https://your-service.onrender.com
 */
export function getApiBaseUrl(): string {
  const raw = import.meta.env.VITE_API_BASE_URL as string | undefined;
  const base = (raw && raw.trim()) || 'http://127.0.0.1:8000';
  return base.replace(/\/$/, '');
}

export function apiUrl(path: string): string {
  const base = getApiBaseUrl();
  const p = path.startsWith('/') ? path : `/${path}`;
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
