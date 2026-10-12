#!/usr/bin/env bash
set -euo pipefail

HOST=""
KEY=""

while getopts "h:i:" opt; do
    case "$opt" in
        h) HOST="$OPTARG" ;;
        i) KEY="$OPTARG" ;;
        *) exit 1 ;;
    esac
done

if [ -z "$HOST" ] || [ -z "$KEY" ]; then
    echo "Usage: ./deploy/deploy.sh -h PUBLIC-IP -i KEY.pem"
    exit 1
fi

for tool in ssh rsync curl python3; do
    if ! command -v "$tool" >/dev/null; then
        echo "Missing required tool: $tool"
        exit 1
    fi
done

cd "$(dirname "$0")/.."

echo "Checking Python code..."
python3 -m compileall -q config manage.py

echo "Copying files to server..."
rsync -az \
    --exclude='.git/' \
    --exclude='.venv/' \
    --exclude='.env' \
    --exclude='*.pem' \
    --exclude='db.sqlite3' \
    --exclude='__pycache__/' \
    -e "ssh -i $KEY" \
    ./ "ubuntu@$HOST:/home/ubuntu/CS408-Final-Project/"

echo "Installing dependencies and restarting..."
ssh -i "$KEY" "ubuntu@$HOST" \
    'cd ~/CS408-Final-Project &&
     .venv/bin/python -m pip install -r requirements.txt &&
     .venv/bin/python manage.py migrate --noinput &&
     sudo systemctl restart canvas-tracker'

echo "Checking live website..."
curl -f --retry 5 --retry-delay 2 "http://$HOST/"

echo "Deployment successful!"
