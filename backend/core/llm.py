"""Core LLM module - Qwen2.5 + LoRA generation.

Load model 1 lần khi backend start, cache trong memory.

Prompt KHÔNG định nghĩa ở đây: import từ backend/core/prompt.py, cùng file mà
training/bootstrap_deep_qa.py và training/score_gold.py dùng. Trước đây file này
giữ một bản COPY của SYSTEM và bản copy đã lệch (thiếu quy tắc trích nguồn kèm
url, thiếu quy tắc NER) - model được train một đằng, serve một nẻo.
"""
from __future__ import annotations

from functools import lru_cache

from backend.core.config import FUSED_MODEL_PATH
from backend.core.prompt import chat_messages

# Output của training/fuse.sh (một nguồn duy nhất: backend/core/config.py)
MODEL_PATH = FUSED_MODEL_PATH

# 512 token cắt ngang câu trả lời "sâu sắc, chi tiết" mà SYSTEM yêu cầu, và cắt
# mất luôn phần [Nguồn: ...] ở cuối - citation precision đo ra 0 dù model đúng.
MAX_TOKENS = 768


@lru_cache(maxsize=1)
def get_model():
    """Load model 1 lần, cache trong suốt session."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model chưa có tại {MODEL_PATH}. Chạy training/fuse.sh để tạo model."
        )
    from mlx_lm import load
    return load(str(MODEL_PATH))


def generate_response(question: str, context: str = "", max_tokens: int = MAX_TOKENS) -> str:
    """Sinh câu trả lời từ Qwen+LoRA. Greedy: cùng câu hỏi -> cùng câu trả lời."""
    model, tokenizer = get_model()

    # Dùng chat template của tokenizer, không tự ghép chuỗi <|im_start|> bằng tay:
    # training đi qua apply_chat_template, ghép tay dễ lệch một ký tự là model lạ prompt.
    prompt = tokenizer.apply_chat_template(
        chat_messages(context, question),
        add_generation_prompt=True,
        tokenize=False,
    )

    from mlx_lm import generate
    from mlx_lm.sample_utils import make_sampler

    # temp=0.0 -> argmax. Đây cũng là mặc định của mlx_lm hiện tại, viết rõ ra để
    # demo không đổi kết quả nếu mlx_lm sau này đổi mặc định sang sampling.
    return generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=max_tokens,
        sampler=make_sampler(temp=0.0),
        verbose=False,
    )
