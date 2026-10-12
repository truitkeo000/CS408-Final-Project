#!/usr/bin/env bash
set -euo pipefail

APP_DIR=/home/ubuntu/CS408-Final-Project
SERVICE=canvas-tracker

if [ "$EUID" -ne 0 ]; then
    echo "Run with sudo: sudo bash deploy/setup-ec2.sh"
    exit 1
fi

echo "Installing server dependencies..."
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 python3-venv python3-pip nginx rsync

echo "Preparing application..."
mkdir -p "$APP_DIR"
chown ubuntu:ubuntu "$APP_DIR"

if [ ! -f "$APP_DIR/.env" ]; then
    echo "Missing private .env file."
    exit 1
fi

chmod 600 "$APP_DIR/.env"

echo "Installing Python dependencies..."
cd "$APP_DIR"
runuser -u ubuntu -- python3 -m venv .venv
runuser -u ubuntu -- .venv/bin/python -m pip install -r requirements.txt
runuser -u ubuntu -- .venv/bin/python manage.py migrate --noinput

echo "Installing systemd service..."
cp deploy/${SERVICE}.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable "$SERVICE"
systemctl restart "$SERVICE"

echo "Configuring nginx..."
cat > /etc/nginx/sites-available/canvas-tracker <<'NGINX'
server {
    listen 80 default_server;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX

rm -f /etc/nginx/sites-enabled/default
ln -sfn /etc/nginx/sites-available/canvas-tracker \
    /etc/nginx/sites-enabled/canvas-tracker

nginx -t
systemctl enable nginx
systemctl restart nginx

echo "EC2 setup completed."
echo "Visit http://54.185.198.226/"
