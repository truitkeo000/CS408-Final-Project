#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

for tool in python3; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "Missing required tool: $tool"
        exit 1
    fi
done

if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "Missing Python venv. Install python3-venv."
    exit 1
fi

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate --noinput

echo "Starting Django at http://127.0.0.1:8000/"
exec .venv/bin/python manage.py runserver 127.0.0.1:8000 --noreload
