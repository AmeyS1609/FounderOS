/**
 * Writes Netlify `public/_redirects` before Vite build.
 * Set BACKEND_PUBLIC_URL on Netlify (e.g. https://xxx.onrender.com) so the browser
 * can use same-origin paths: /api/*, /health, /env-check → backend.
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
  lines.push(`/health  ${backend}/health  200`);
  lines.push(`/env-check  ${backend}/env-check  200`);
}
lines.push('/*  /index.html  200');

const out = path.join(pub, '_redirects');
fs.writeFileSync(out, `${lines.join('\n')}\n`);
// eslint-disable-next-line no-console
console.log(
  `[write-redirects] wrote ${out}`,
  backend ? `(proxy /api,/health,/env-check → ${backend})` : '(SPA only — set BACKEND_PUBLIC_URL on Netlify for API proxy)',
);
