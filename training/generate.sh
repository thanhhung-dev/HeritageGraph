#!/usr/bin/env bash
# Sinh thử câu trả lời để xem model đã học đúng định dạng chưa.
#   bash training/generate.sh
#   MODEL=./models/qwen-fused PROMPT_FILE=./prompts/test_quick.txt bash training/generate.sh
set -euo pipefail
cd "$(dirname "$0")/.."

PY=backend/.venv/bin/python
MODEL="${MODEL:-./models/qwen-fused}"
PROMPT_FILE="${PROMPT_FILE:-./prompts/test_quick.txt}"
MAX_TOKENS="${MAX_TOKENS:-400}"

[ -f "$PROMPT_FILE" ] || { echo "Không có $PROMPT_FILE"; exit 1; }

# mlx_lm generate KHÔNG có cờ --prompt-file (bản cũ dùng cờ này nên luôn lỗi
# argparse), và cả file bị coi là 1 prompt. Ở đây tách theo dòng "---".
# System prompt lấy trực tiếp từ bootstrap_deep_qa.py để không lệch với data train.
SYSTEM=$($PY -c "import sys; sys.path.insert(0, 'training'); from bootstrap_deep_qa import SYSTEM; print(SYSTEM)")

i=0
while IFS= read -r -d '' block; do
  i=$((i + 1))
  echo "======================== PROMPT $i ========================"
  printf '%s\n\n' "$block"
  $PY -m mlx_lm generate \
    --model "$MODEL" \
    --system-prompt "$SYSTEM" \
    --prompt "$block" \
    --max-tokens "$MAX_TOKENS"
  echo ""
done < <($PY -c '
import sys
text = open(sys.argv[1], encoding="utf-8").read()
for block in text.split("\n---\n"):
    block = block.strip()
    if block:
        sys.stdout.write(block + "\0")
' "$PROMPT_FILE")

