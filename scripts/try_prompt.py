#!/usr/bin/env python3
"""Thử một prompt trên model đã train, KHÔNG cần fuse.

Dùng đúng SYSTEM + chat template của backend/core/prompt.py - cùng thứ mà
bootstrap_deep_qa.py sinh data và score_gold.py đo. Gõ `mlx_lm generate --prompt`
trực tiếp là thiếu SYSTEM: model lạ prompt, kết quả không nói lên điều gì.

  # Hỏi qua retrieval thật (giống lúc chạy app)
  backend/.venv/bin/python scripts/try_prompt.py "Hãy kể về Lăng Gia Long"

  # Tự đưa nguồn, bỏ qua retrieval
  backend/.venv/bin/python scripts/try_prompt.py "Đèo Hải Vân cao bao nhiêu?" --source "..."

  # Test từ chối: không nguồn -> phải từ chối
  backend/.venv/bin/python scripts/try_prompt.py "Chùa Một Cột xây năm nào?" --source ""

  # Test NER
  backend/.venv/bin/python scripts/try_prompt.py --ner "Điện Hòn Chén được vua Minh Mạng cho tu sửa vào tháng 3/1832."

  # So với base (không adapter) trên cùng prompt
  backend/.venv/bin/python scripts/try_prompt.py "..." --base
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend.core.config import LORA_ADAPTER_PATH  # noqa: E402
from backend.core.prompt import NER_QUESTION, chat_messages  # noqa: E402

BASE = "mlx-community/Qwen2.5-3B-Instruct-4bit"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("question")
    ap.add_argument("--source", default=None,
                    help='Nguồn đưa tay. Bỏ trống ("") để test từ chối. '
                         "Không truyền -> lấy bằng retrieval thật.")
    ap.add_argument("--ner", action="store_true",
                    help="Coi question là đoạn văn cần trích entity")
    ap.add_argument("--base", action="store_true", help="Chạy base, không gắn adapter")
    ap.add_argument("--adapter", default=str(LORA_ADAPTER_PATH))
    ap.add_argument("--checkpoint", default=None,
                    help="Iter cụ thể, ví dụ 0000800. Mặc định: adapters.safetensors")
    ap.add_argument("--max-tokens", type=int, default=768)
    args = ap.parse_args()

    if args.ner:
        source, question = "", NER_QUESTION.format(text=args.question)
    elif args.source is not None:
        source, question = args.source, args.question
    else:
        from backend.core.rag import retrieve_context
        question = args.question
        source, hits = retrieve_context(args.question)
        print(f"--- retrieval: {len(hits)} đoạn, {len(source)} ký tự", file=sys.stderr)
        for h in hits:
            print(f"      {h.get('doc') or h.get('name', '?')}", file=sys.stderr)
        if not source:
            print("--- retrieval không trả về nguồn -> model PHẢI từ chối", file=sys.stderr)

    adapter = None
    if not args.base:
        adapter = args.adapter
        if args.checkpoint:
            # mlx_lm chỉ đọc adapters.safetensors trong thư mục; trỏ vào một
            # checkpoint cụ thể phải dựng thư mục tạm.
            import shutil
            import tempfile
            src = Path(args.adapter) / f"{args.checkpoint}_adapters.safetensors"
            if not src.exists():
                print(f"Không có {src}", file=sys.stderr)
                return 1
            tmp = Path(tempfile.mkdtemp())
            shutil.copy(Path(args.adapter) / "adapter_config.json", tmp)
            shutil.copy(src, tmp / "adapters.safetensors")
            adapter = str(tmp)

    print(f"--- model: {BASE}  adapter: {adapter or '(không)'}", file=sys.stderr)

    from mlx_lm import generate, load
    from mlx_lm.sample_utils import make_sampler

    model, tokenizer = load(BASE, adapter_path=adapter)
    prompt = tokenizer.apply_chat_template(
        chat_messages(source, question), add_generation_prompt=True, tokenize=False)
    out = generate(model, tokenizer, prompt=prompt, max_tokens=args.max_tokens,
                   sampler=make_sampler(temp=0.0), verbose=False)
    print("\n" + out.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
