#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PORT="${1:-8080}"
echo "本地预览：http://127.0.0.1:${PORT}"
echo "总览页：  http://127.0.0.1:${PORT}/index.html"
exec python3 -m http.server "$PORT"
