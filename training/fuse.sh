#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

MODEL="${MODEL:-mlx-community/Qwen2.5-7B-Instruct-4bit}"
ADAPTER="${ADAPTER:-./models/lora-adapter}"
SAVE_PATH="${SAVE_PATH:-./models/qwen-7b-fused}"

echo "==> Fusing adapter into base model"
echo "    base:   $MODEL"
echo "    adapter: $ADAPTER"
echo "    output: $SAVE_PATH"

mlx_lm.fuse \
  --model "$MODEL" \
  --adapter-path "$ADAPTER" \
  --save-path "$SAVE_PATH"

echo "==> Fused model ready at $SAVE_PATH"
