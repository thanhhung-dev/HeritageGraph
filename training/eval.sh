#!/usr/bin/env bash
# Tính loss/perplexity của adapter trên tập valid (không train).
#   bash training/eval.sh              # dùng adapters.safetensors
#   bash training/eval.sh 0000600      # dùng checkpoint iter 600
set -euo pipefail
cd "$(dirname "$0")/.."

PY=backend/.venv/bin/python
CONFIG=training/lora_config.yaml
ADAPTER="${ADAPTER:-./models/lora-adapter}"

MODEL="${MODEL:-$($PY -c "import yaml,sys; print(yaml.safe_load(open('$CONFIG'))['model'])")}"

# mlx_lm --test đọc data/test.jsonl. Repo chưa có tập test riêng (corpus quá nhỏ),
# nên dựng thư mục tạm với test.jsonl = valid.jsonl và nói rõ đang đo trên valid.
ADAPTER_TMP=""
TMP=$(mktemp -d)
trap 'rm -rf "$TMP" ${ADAPTER_TMP:+"$ADAPTER_TMP"}' EXIT
cp data/train.jsonl data/valid.jsonl "$TMP/"
cp data/valid.jsonl "$TMP/test.jsonl"

CKPT="${1:-}"
if [ -n "$CKPT" ]; then
  SRC="$ADAPTER/${CKPT}_adapters.safetensors"
  [ -f "$SRC" ] || { echo "Không có $SRC"; exit 1; }
  ADAPTER_TMP=$(mktemp -d)
  cp "$ADAPTER/adapter_config.json" "$ADAPTER_TMP/"
  cp "$SRC" "$ADAPTER_TMP/adapters.safetensors"
  ADAPTER="$ADAPTER_TMP"
  echo "==> Checkpoint iter $CKPT"
fi

echo "==> Eval trên tập VALID (${MODEL})"
# --mask-prompt để loss chỉ tính trên câu trả lời, khớp với lúc train
# (không có cờ này thì loss gồm cả đoạn nguồn -> số liệu không so sánh được).
$PY -m mlx_lm lora \
  --model "$MODEL" \
  --adapter-path "$ADAPTER" \
  --data "$TMP" \
  --test \
  --test-batches -1 \
  --batch-size 2 \
  --max-seq-length 1536 \
  --mask-prompt

echo ""
echo "==> Loss/ppl chỉ đo khả năng khớp văn bản. Đánh giá NER/Citation/Refusal/Style:"
echo "    $PY training/score_gold.py"
