#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

MODEL="${MODEL:-mlx-community/Qwen2.5-7B-Instruct-4bit}"
ADAPTER="${ADAPTER:-./adapters}"
TEST_BATCHES="${TEST_BATCHES:-50}"

echo "==> Eval LoRA on validation set (test-only mode)"

mlx_lm.lora \
  --model "$MODEL" \
  --adapter-path "$ADAPTER" \
  --data ./data \
  --test \
  --test-batches "$TEST_BATCHES"

echo "==> Eval done. Use scripts/score_gold.py to compute NER/Citation/Refusal/Style metrics."
