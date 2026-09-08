#!/usr/bin/env python3
"""Fuse LoRA without an intermediate requantization, then export Q8_0 GGUF.

Run on the source Apple-Silicon Mac with the backend virtualenv:
    backend/.venv/bin/python scripts/export_gguf.py

The script needs internet once to clone llama.cpp and install its converter
requirements. Temporary FP16 weights and converter files are removed afterwards.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "models"
ADAPTER_PATH = MODELS_DIR / "lora-serve"
OUTPUT_PATH = MODELS_DIR / "qwen-fused.gguf"
BASE_MODEL = "mlx-community/Qwen2.5-3B-Instruct-4bit"
TOKENIZER_FILES = (
    "added_tokens.json",
    "chat_template.jinja",
    "merges.txt",
    "special_tokens_map.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "vocab.json",
)


def run(*args: str, cwd: Path = ROOT) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def converter_requirements(llama_cpp: Path) -> Path:
    candidates = [
        llama_cpp / "requirements" / "requirements-convert_hf_to_gguf.txt",
        llama_cpp / "requirements.txt",
    ]
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError("Không tìm thấy requirements cho convert_hf_to_gguf.py")


def restore_huggingface_tokenizer(model_path: Path) -> None:
    """MLX save simplifies tokenizer_config in a way HF converter rejects."""
    from huggingface_hub import snapshot_download

    snapshot = Path(
        snapshot_download(repo_id=BASE_MODEL, allow_patterns=list(TOKENIZER_FILES))
    )
    for name in TOKENIZER_FILES:
        source = snapshot / name
        if source.is_file():
            shutil.copy2(source, model_path / name)


def export(output: Path, force: bool) -> None:
    if output.exists() and not force:
        print(f"Đã có {output}. Dùng --force nếu muốn tạo lại.")
        return
    if not (ADAPTER_PATH / "adapters.safetensors").is_file():
        raise FileNotFoundError(
            f"Thiếu adapter {ADAPTER_PATH / 'adapters.safetensors'}"
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    with tempfile.TemporaryDirectory(prefix="heritagegraph-gguf-") as directory:
        workspace = Path(directory)
        fp16_model = workspace / "qwen-fused-fp16"
        llama_cpp = workspace / "llama.cpp"
        converter_venv = workspace / "converter-venv"

        print("[1/4] Fuse base + LoRA và dequantize một lần sang FP16...")
        run(
            sys.executable,
            "-m",
            "mlx_lm",
            "fuse",
            "--model",
            BASE_MODEL,
            "--adapter-path",
            str(ADAPTER_PATH),
            "--save-path",
            str(fp16_model),
            "--dequantize",
        )
        restore_huggingface_tokenizer(fp16_model)

        print("[2/4] Tải llama.cpp converter...")
        run(
            "git",
            "clone",
            "--depth",
            "1",
            "https://github.com/ggml-org/llama.cpp.git",
            str(llama_cpp),
        )

        print("[3/4] Cài dependency converter trong môi trường tạm...")
        run(sys.executable, "-m", "venv", str(converter_venv))
        converter_python = converter_venv / "bin" / "python"
        if sys.platform == "win32":
            converter_python = converter_venv / "Scripts" / "python.exe"
        run(
            str(converter_python),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "-r",
            str(converter_requirements(llama_cpp)),
        )

        print("[4/4] Chuyển model sang GGUF Q8_0...")
        run(
            str(converter_python),
            str(llama_cpp / "convert_hf_to_gguf.py"),
            str(fp16_model),
            "--outfile",
            str(output),
            "--outtype",
            "q8_0",
        )

    size_gib = output.stat().st_size / (1024**3)
    print(f"Đã tạo {output} ({size_gib:.2f} GiB)")
    print("Tiếp theo: bash scripts/package_docker.sh")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    export(args.output.resolve(), args.force)


if __name__ == "__main__":
    main()
