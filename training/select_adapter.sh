#!/usr/bin/env bash
# Chọn checkpoint LoRA để SERVE. Dựng models/lora-serve/ từ một checkpoint cụ thể.
#
#   bash training/select_adapter.sh 0000200   # checkpoint có val loss thấp nhất
#   bash training/select_adapter.sh           # checkpoint cuối (adapters.safetensors)
#
# VÌ SAO CẦN FILE NÀY. mlx_lm chỉ đọc `adapters.safetensors` trong thư mục adapter,
# và file đó LUÔN là checkpoint cuối. Nhưng val loss của lần train gần nhất chạm
# đáy ở iter 200 (0.414) rồi tăng lên 0.473 ở iter 720 - overfit từ ~iter 250. Đo
# trên 5 câu hỏi phủ định: iter 200 sai 1/5, iter 720 sai 2/5, iter 100 sai 5/5.
# Trỏ backend thẳng vào models/lora-adapter/ là mặc định lấy bản overfit nhất.
set -euo pipefail
cd "$(dirname "$0")/.."

ADAPTER=./models/lora-adapter
SERVE=./models/lora-serve
CKPT="${1:-}"

if [ -n "$CKPT" ]; then
  SRC="$ADAPTER/${CKPT}_adapters.safetensors"
  if [ ! -f "$SRC" ]; then
    echo "Không có $SRC. Các checkpoint hiện có:"
    ls "$ADAPTER"/*_adapters.safetensors
    exit 1
  fi
else
  SRC="$ADAPTER/adapters.safetensors"
  [ -f "$SRC" ] || { echo "Không có $SRC. Chạy training/train.sh trước."; exit 1; }
  CKPT="cuối"
fi

mkdir -p "$SERVE"
cp "$ADAPTER/adapter_config.json" "$SERVE/"
cp "$SRC" "$SERVE/adapters.safetensors"
# Ghi lại checkpoint nào đang serve. Không có file này thì sau một tháng không ai
# biết models/lora-serve/ là iter bao nhiêu.
echo "$CKPT" > "$SERVE/CHECKPOINT"

echo "==> models/lora-serve/ = checkpoint $CKPT"
echo "    val loss từng iter: grep 'Val loss' train_v4.log"
