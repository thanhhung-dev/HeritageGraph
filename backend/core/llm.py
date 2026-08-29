"""Core LLM module - Qwen2.5 + LoRA generation.

Load model 1 lần khi backend start, cache trong memory.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

# Path tới model đã fuse
MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "qwen-7b-fused"

SYSTEM_PROMPT = """Bạn là trợ lý văn hóa dân gian Việt Nam, chuyên về Đà Nẵng và Huế.
Nguyên tắc:
- Trả lời văn phong trang trọng, giàu tính kể chuyện
- Trích xuất entity chính xác theo 4 loại: người, địa điểm, sự kiện, thời gian
- Luôn trích nguồn khi dùng thông tin (định dạng: [Nguồn: <trích đoạn>])
- Không bịa thông tin ngoài nguồn - nếu không có thì từ chối lịch sự"""


@lru_cache(maxsize=1)
def get_model():
    """Load model 1 lần, cache trong suốt session."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model chưa có tại {MODEL_PATH}. "
            f"Chạy training/fuse.sh để tạo model."
        )
    from mlx_lm import load
    return load(str(MODEL_PATH))


def generate_response(question: str, context: str = "", max_tokens: int = 512) -> str:
    """Sinh câu trả lời từ Qwen+LoRA."""
    model, tokenizer = get_model()

    if context:
        user_msg = f"Nguồn: {context}\n\nCâu hỏi: {question}\n\nTrả lời kèm [Nguồn: ...]"
    else:
        user_msg = question

    prompt = f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n<|im_start|>user\n{user_msg}<|im_end|>\n<|im_start|>assistant\n"

    from mlx_lm import generate
    return generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False)
