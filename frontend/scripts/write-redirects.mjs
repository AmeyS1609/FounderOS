/**
 * Writes Netlify `public/_redirects` before Vite build.
 * Set BACKEND_PUBLIC_URL on Netlify (e.g. https://your-service.up.railway.app) to proxy
 * browser calls from /api/* → backend (same-origin, no CORS headaches).
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, '..');
const pub = path.join(root, 'public');
fs.mkdirSync(pub, { recursive: true });

const backend = (process.env.BACKEND_PUBLIC_URL || '').trim().replace(/\/$/, '');
const lines = [];
if (backend) {
  lines.push(`/api/*  ${backend}/api/:splat  200`);
}
lines.push('/*  /index.html  200');

const out = path.join(pub, '_redirects');
fs.writeFileSync(out, `${lines.join('\n')}\n`);
// eslint-disable-next-line no-console
console.log(
  `[write-redirects] wrote ${out}`,
  backend ? `(API proxy /api → ${backend})` : '(SPA only — set BACKEND_PUBLIC_URL on Netlify to enable /api proxy)',
);
