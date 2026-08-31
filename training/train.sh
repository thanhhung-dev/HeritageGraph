#!/usr/bin/env bash
# Train LoRA. Mặc định: tiếp tục từ checkpoint mới nhất nếu có.
#   bash training/train.sh          # resume nếu có checkpoint
#   bash training/train.sh --fresh  # bỏ checkpoint cũ, train lại từ đầu
set -euo pipefail
cd "$(dirname "$0")/.."

PY=backend/.venv/bin/python
BASE_CONFIG=training/lora_config.yaml
RESUME_CONFIG=training/lora_config_resume.yaml

for f in data/train.jsonl data/valid.jsonl; do
  if [ ! -s "$f" ]; then
    echo "Thiếu $f. Chạy: $PY training/bootstrap_deep_qa.py"
    exit 1
  fi
done

# Config resume cũ luôn bị xóa trước: nó gắn với một checkpoint cụ thể,
# giữ lại là train sai iters/checkpoint ở lần chạy sau.
rm -f "$RESUME_CONFIG"

CONFIG="$BASE_CONFIG"
if [ "${1:-}" = "--fresh" ]; then
  echo "==> --fresh: train từ đầu (checkpoint cũ trong models/lora-adapter/ sẽ bị ghi đè)"
# mlx_lm lưu checkpoint dạng 0000100_adapters.safetensors
elif compgen -G "models/lora-adapter/*_adapters.safetensors" > /dev/null; then
  echo "==> Tìm thấy checkpoint, tạo config resume..."
  if $PY training/setup_resume.py && [ -f "$RESUME_CONFIG" ]; then
    CONFIG="$RESUME_CONFIG"
  else
    echo "==> Không resume được, dùng config gốc"
  fi
else
  echo "==> Chưa có checkpoint, train từ đầu"
fi

echo "==> Config: $CONFIG"
echo ""
$PY -m mlx_lm lora --config "$CONFIG"

echo ""
echo "==> Done. Adapter: models/lora-adapter/adapters.safetensors"
echo "    Chọn checkpoint có val loss thấp nhất trong log, đừng mặc định lấy cái cuối."
