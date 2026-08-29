#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

MODEL="${MODEL:-./models/qwen-7b-fused}"
PROMPT_FILE="${PROMPT_FILE:-./prompts/samples.txt}"
MAX_TOKENS="${MAX_TOKENS:-512}"

echo "==> Generating with $MODEL"
echo "    prompts: $PROMPT_FILE"

mlx_lm.generate \
  --model "$MODEL" \
  --prompt-file "$PROMPT_FILE" \
  --max-tokens "$MAX_TOKENS" \
  --verbose
