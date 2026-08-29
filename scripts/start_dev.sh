#!/usr/bin/env bash
# Chạy cả backend + frontend đồng thời (mỗi cái 1 terminal tab)
set -e
cd "$(dirname "$0")/.."

if [ ! -d ".venv" ]; then
  echo "ERROR: chưa có .venv. Chạy: python3 -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt"
  exit 1
fi

source .venv/bin/activate

# Tab 1: backend
echo "Starting backend on :8000"
uvicorn backend.app:app --reload --port 8000 &
BACKEND_PID=$!

# Tab 2: frontend
echo "Starting frontend on :3000"
cd frontend
if [ ! -d "node_modules" ]; then
  echo "Installing frontend deps..."
  npm install
fi
npm run dev &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
