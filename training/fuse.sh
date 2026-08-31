#!/usr/bin/env bash
# Gộp adapter LoRA vào base model.
#   bash training/fuse.sh                  # fuse adapters.safetensors (checkpoint cuối)
#   bash training/fuse.sh 0000600          # fuse checkpoint iter 600 (val loss thấp nhất)
set -euo pipefail
cd "$(dirname "$0")/.."

PY=backend/.venv/bin/python
CONFIG=training/lora_config.yaml
ADAPTER="${ADAPTER:-./models/lora-adapter}"
SAVE_PATH="${SAVE_PATH:-./models/qwen-fused}"

# Base model PHẢI đúng model đã train. Bản cũ hardcode Qwen2.5-7B trong khi
# lora_config.yaml train trên Qwen2.5-3B -> fuse sai model.
MODEL="${MODEL:-$($PY -c "import yaml,sys; print(yaml.safe_load(open('$CONFIG'))['model'])")}"

FUSE_FROM="$ADAPTER"
CKPT="${1:-}"
if [ -n "$CKPT" ]; then
  SRC="$ADAPTER/${CKPT}_adapters.safetensors"
  [ -f "$SRC" ] || { echo "Không có $SRC"; ls "$ADAPTER"/*_adapters.safetensors; exit 1; }
  FUSE_FROM=$(mktemp -d)
  trap 'rm -rf "$FUSE_FROM"' EXIT
  cp "$ADAPTER/adapter_config.json" "$FUSE_FROM/"
  cp "$SRC" "$FUSE_FROM/adapters.safetensors"
  echo "==> Fuse checkpoint iter $CKPT"
fi

echo "==> base:    $MODEL"
echo "==> adapter: $FUSE_FROM"
echo "==> output:  $SAVE_PATH"

$PY -m mlx_lm fuse --model "$MODEL" --adapter-path "$FUSE_FROM" --save-path "$SAVE_PATH"

echo "==> Fused model ready at $SAVE_PATH"
