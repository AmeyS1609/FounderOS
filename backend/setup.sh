#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -m venv venv
# shellcheck source=/dev/null
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete — run: uvicorn main:app --reload --port 8000"
