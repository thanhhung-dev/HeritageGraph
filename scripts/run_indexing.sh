#!/usr/bin/env bash
# Chạy index GraphRAG - đặt chạy qua đêm
set -e
cd "$(dirname "$0")/.."

source .venv/bin/activate

# Check Ollama
if ! curl -s http://localhost:11434 > /dev/null; then
  echo "ERROR: Ollama chưa chạy. Chạy: ollama serve &"
  exit 1
fi

# Init nếu chưa có settings.yaml
if [ ! -f "graphrag/settings.yaml" ]; then
  echo "Init GraphRAG..."
  python -m graphrag.index --init --root ./graphrag
  echo ""
  echo "TODO: sửa graphrag/settings.yaml để dùng Ollama + Qwen"
  echo "      xem README.md phần Setup"
  exit 1
fi

echo "Starting GraphRAG indexing (sẽ chạy 8-12 giờ)..."
python -m graphrag.index --root ./graphrag
echo "Done. Output ở graphrag/output/"
