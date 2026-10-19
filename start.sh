
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Find Python 3.10 or newer
PYTHON=""

for candidate in python3.12 python3.13 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
        if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
            PYTHON="$(command -v "$candidate")"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Error: Python 3.10 or newer is required."
    exit 1
fi

echo "Using Python: $PYTHON"

# Create a virtual environment if needed
if [ -d ".venv" ]; then
    if ! .venv/bin/python -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
        echo "Error: Existing .venv uses an incompatible Python version."
        exit 1
    fi
else
    "$PYTHON" -m venv .venv
fi

# Install dependencies
.venv/bin/python -m pip install -r requirements.txt

# Set up the database
.venv/bin/python manage.py migrate --noinput

# Start the application
echo "Starting Campus Compass at http://127.0.0.1:8000/"
exec .venv/bin/python manage.py runserver 127.0.0.1:8000 --noreload
