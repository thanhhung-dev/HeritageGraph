#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Activate venv nếu có
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

echo "==> Training LoRA on $(uname -m) | model=Qwen2.5-7B-Instruct-4bit"

mlx_lm.lora \
  --config training/lora_config.yaml

echo "==> Done. Adapter saved to ./models/lora-adapter"
