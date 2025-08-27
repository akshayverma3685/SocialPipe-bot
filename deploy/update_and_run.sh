#!/usr/bin/env bash
set -e
APP_DIR="/home/${DEPLOY_USER}/socialpipe"
mkdir -p "$APP_DIR"
cd "$APP_DIR"
# assume repo already cloned once; otherwise clone
if [ ! -d ".git" ]; then
  git clone https://github.com/akshayverma3685/SocialPipe-bot.git .
else
  git fetch --all
  git reset --hard origin/main
fi

# pull latest image if using GHCR, or build locally from repo
docker-compose -f docker-compose.prod.yml pull || true
docker-compose -f docker-compose.prod.yml up -d --remove-orphans
