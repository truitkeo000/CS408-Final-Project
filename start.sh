#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Missing Python 3.10 or newer. Install Python 3.12."
    exit 1
fi

if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)'; then
    echo "Python 3.10 or newer is required. Install Python 3.12."
    exit 1
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "Missing Python venv. Install python3-venv."
    exit 1
fi

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate --noinput

echo "Open http://127.0.0.1:8000/"
exec .venv/bin/python manage.py runserver 127.0.0.1:8000 --noreload
