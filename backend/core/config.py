"""Config chung cho backend."""
import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Paths
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
GRAPHRAG_DIR = PROJECT_ROOT / "graphrag"
EVAL_DIR = PROJECT_ROOT / "eval"

# Model
# Tên thư mục phải khớp SAVE_PATH trong training/fuse.sh. Không dùng lại tên
# "qwen-7b-fused": lora_config.yaml train trên Qwen2.5-3B, không phải 7B.
FUSED_MODEL_PATH = MODELS_DIR / "qwen-fused"
LORA_ADAPTER_PATH = MODELS_DIR / "lora-adapter"

# SERVE BẰNG BASE + ADAPTER, KHÔNG BẰNG MODEL ĐÃ FUSE.
#
# Base là model 4-bit (group_size 64, bits 4), nên `mlx_lm fuse` phải dequantize ->
# cộng LoRA -> REQUANTIZE lại. Vòng requantize đó làm mất độ chính xác đủ để đổi
# câu trả lời. Đo trên 5 câu hỏi phủ định, cùng temp=0.0, cùng đoạn nguồn:
#     base + adapter (iter 200) : sai 1/5
#     models/qwen-fused          : sai 3/5
# Cùng một trọng số. Ví dụ cụ thể:
#     adapter: "Không phải vậy ạ. Chùa Thiên Mụ thật sự ở Huế."          (đúng)
#     fused  : "Không phải vậy đâu. Chùa Thiên Mụ không ở Huế mà ở Đà Nẵng."  (sai)
# `scripts/try_prompt.py` luôn load base + adapter, nên nó cho kết quả tốt hơn
# backend - lệch đó từng làm mọi phép đo bằng try_prompt.py không đại diện cho
# thứ người dùng thật nhận được.
#
# fuse.sh vẫn giữ: model fuse gọn hơn (1.6G, một thư mục) và vẫn dùng cho
# training/bootstrap_by_location.py, training/generate.sh. Chỉ đường SERVE đổi.
BASE_MODEL = "mlx-community/Qwen2.5-3B-Instruct-4bit"

# Thư mục adapter DÙNG ĐỂ SERVE. Không trỏ thẳng vào models/lora-adapter:
# `adapters.safetensors` ở đó luôn là checkpoint CUỐI, mà val loss của lần train
# gần nhất chạm đáy ở iter 200 (0.414) rồi tăng đến 0.473 ở iter 720 - overfit từ
# ~iter 250. Chọn checkpoint bằng `bash training/select_adapter.sh 0000200`.
LORA_SERVE_PATH = MODELS_DIR / "lora-serve"

# GGUF model cho Docker/llama.cpp. Sinh ra bằng scripts/export_gguf.py.
GGUF_MODEL_PATH = MODELS_DIR / "qwen-fused.gguf"

# INFERENCE_BACKEND: "mlx" (macOS Apple Silicon) hoặc "llama_cpp" (Docker/Linux/Windows).
# MLX nhanh hơn trên Mac nhưng KHÔNG chạy trong Docker trên máy khác.
# llama_cpp chạy được everywhere (CPU hoặc CUDA).
INFERENCE_BACKEND = os.environ.get("INFERENCE_BACKEND", "mlx")

# Server
BACKEND_HOST = "0.0.0.0"
BACKEND_PORT = 8000
