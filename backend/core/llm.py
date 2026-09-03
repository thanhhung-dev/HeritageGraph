"""Core LLM module - Qwen2.5 + LoRA generation.

Load model 1 lần khi backend start, cache trong memory.

Prompt KHÔNG định nghĩa ở đây: import từ backend/core/prompt.py, cùng file mà
training/bootstrap_deep_qa.py và training/score_gold.py dùng. Trước đây file này
giữ một bản COPY của SYSTEM và bản copy đã lệch (thiếu quy tắc trích nguồn kèm
url, thiếu quy tắc NER) - model được train một đằng, serve một nẻo.

Serve BASE + ADAPTER, không serve model đã fuse: xem BASE_MODEL trong
backend/core/config.py cho số đo. Adapter nào được dùng thì do
training/select_adapter.sh quyết định, không mặc định lấy checkpoint cuối.
"""
from __future__ import annotations

from functools import lru_cache

from backend.core.config import BASE_MODEL, LORA_SERVE_PATH
from backend.core.prompt import chat_messages

# 512 token cắt ngang câu trả lời "sâu sắc, chi tiết" mà SYSTEM yêu cầu, và cắt
# mất luôn phần [Nguồn: ...] ở cuối - citation precision đo ra 0 dù model đúng.
MAX_TOKENS = 768


@lru_cache(maxsize=1)
def get_model():
    """Load base + adapter 1 lần, cache trong suốt session."""
    if not (LORA_SERVE_PATH / "adapters.safetensors").exists():
        raise FileNotFoundError(
            f"Chưa có adapter tại {LORA_SERVE_PATH}. Chạy:\n"
            f"    bash training/select_adapter.sh 0000200"
        )
    from mlx_lm import load
    return load(BASE_MODEL, adapter_path=str(LORA_SERVE_PATH))


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
