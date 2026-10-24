#!/bin/sh
# sync-hub.sh — kéo skill/tài liệu mới nhất từ hub về workspace OpenClaw của máy này.
# Chạy tay: bash sync-hub.sh | Chạy tự động: openclaw automations (xem README).
set -e
WS="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
HUB="$WS/opendclaw-training"

if [ -d "$HUB/.git" ]; then
  git -C "$HUB" pull --ff-only
else
  git clone https://github.com/hieu2211/opendclaw-training.git "$HUB"
fi

mkdir -p "$WS/skills"
cp -r "$HUB/workspace/skills/." "$WS/skills/"
cp "$HUB/workspace/TOOLS.md" "$HUB/workspace/TOKEN-OPTIMIZATION.md" "$WS/"

echo "✓ Hub synced $(date -u +%Y-%m-%dT%H:%M:%SZ)"
