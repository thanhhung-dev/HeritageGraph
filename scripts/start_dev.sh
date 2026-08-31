#!/usr/bin/env bash
# Chạy cả backend + frontend đồng thời
set -e
cd "$(dirname "$0")/.."

# venv thật của repo là backend/.venv (bản cũ trỏ vào .venv ở gốc, không tồn tại)
VENV=backend/.venv
if [ ! -d "$VENV" ]; then
  echo "ERROR: chưa có $VENV. Chạy:"
  echo "  python3 -m venv $VENV && $VENV/bin/pip install -r backend/requirements.txt"
  exit 1
fi

# Tab 1: backend
echo "Starting backend on :8000"
"$VENV/bin/uvicorn" backend.app:app --reload --port 8000 &
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
