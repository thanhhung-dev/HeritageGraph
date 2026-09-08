#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL="$ROOT/models/qwen-fused.gguf"
OUTPUT="${1:-$ROOT/heritagegraph-docker.tar.gz}"

if [[ ! -f "$MODEL" ]]; then
  echo "Thiếu $MODEL" >&2
  echo "Tạo trước bằng: backend/.venv/bin/python scripts/export_gguf.py" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
rm -f "$OUTPUT"

COPYFILE_DISABLE=1 tar -czf "$OUTPUT" \
  -s ',^,HeritageGraph/,' \
  --exclude='backend/.venv' \
  --exclude='backend/venv' \
  --exclude='backend/models' \
  --exclude='backend/**/__pycache__' \
  --exclude='frontend/node_modules' \
  --exclude='frontend/.next' \
  --exclude='**/.DS_Store' \
  -C "$ROOT" \
  README.md \
  docker-compose.yml \
  .dockerignore \
  .env.docker.example \
  backend \
  corpus \
  frontend \
  models/qwen-fused.gguf \
  docs/docker-local.md

echo "Đã tạo: $OUTPUT"
du -h "$OUTPUT"
