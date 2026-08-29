"""Config chung cho backend."""
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Paths
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
GRAPHRAG_DIR = PROJECT_ROOT / "graphrag"
EVAL_DIR = PROJECT_ROOT / "eval"

# Model
FUSED_MODEL_PATH = MODELS_DIR / "qwen-7b-fused"
LORA_ADAPTER_PATH = MODELS_DIR / "lora-adapter"

# Server
BACKEND_HOST = "0.0.0.0"
BACKEND_PORT = 8000
