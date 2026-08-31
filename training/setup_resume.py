#!/usr/bin/env python3
"""
Tạo config resume từ checkpoint mới nhất trong models/lora-adapter/.

Sửa 2 lỗi của bản cũ:
- Glob sai tên file: mlx_lm lưu checkpoint là "0000100_adapters.safetensors",
  không phải "adapter_100.safetensors" => bản cũ không bao giờ tìm thấy
  checkpoint nên train.sh luôn train lại từ đầu.
- Config resume được viết tay lặp lại toàn bộ tham số, dễ lệch khỏi
  lora_config.yaml. Nay đọc trực tiếp config gốc rồi chỉ ghi đè phần cần thiết.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ADAPTER_DIR = ROOT / "models" / "lora-adapter"
CONFIG_BASE = ROOT / "training" / "lora_config.yaml"
CONFIG_RESUME = ROOT / "training" / "lora_config_resume.yaml"

CKPT_RE = re.compile(r"^(\d+)_adapters\.safetensors$")

# Resume chỉ hợp lệ khi checkpoint được train bằng đúng model + hình dạng LoRA.
COMPAT_KEYS = ("model", "fine_tune_type", "num_layers", "lora_parameters")


def find_latest() -> tuple[Path, int] | None:
    found = [
        (p, int(m.group(1)))
        for p in ADAPTER_DIR.glob("*_adapters.safetensors")
        if (m := CKPT_RE.match(p.name))
    ]
    return max(found, key=lambda t: t[1]) if found else None


def incompatible(config: dict) -> list[str]:
    """So sánh config hiện tại với config đã dùng lúc tạo checkpoint."""
    old_path = ADAPTER_DIR / "adapter_config.json"
    if not old_path.exists():
        return []
    old = json.loads(old_path.read_text("utf-8"))
    diffs = []
    for key in COMPAT_KEYS:
        if key in old and old[key] != config.get(key):
            diffs.append(f"{key}: checkpoint={old[key]!r} vs config={config.get(key)!r}")
    return diffs



def main() -> None:
    latest = find_latest()
    if latest is None:
        print(f"Không tìm thấy checkpoint nào trong {ADAPTER_DIR}/")
        print(f"   (mlx_lm lưu dạng 0000100_adapters.safetensors, mỗi save_every iters)")
        sys.exit(1)

    ckpt, last_iter = latest
    config = yaml.safe_load(CONFIG_BASE.read_text("utf-8"))

    diffs = incompatible(config)
    if diffs:
        print(f"Checkpoint {ckpt.name} KHÔNG khớp config hiện tại, không thể resume:")
        for d in diffs:
            print(f"   - {d}")
        print(f"\n   Checkpoint cũ thuộc một cấu hình khác. Hãy chuyển thư mục")
        print(f"   {ADAPTER_DIR}/ sang chỗ khác rồi train lại từ đầu:")
        print(f"      bash training/train.sh --fresh")
        CONFIG_RESUME.unlink(missing_ok=True)
        sys.exit(1)

    total_iters = int(config.get("iters", 1000))

    remaining = total_iters - last_iter

    print(f"Checkpoint mới nhất: {ckpt.name} (iter {last_iter})")
    print(f"Tổng iters: {total_iters} | đã train: {last_iter} | còn lại: {remaining}")

    if remaining <= 0:
        print("\nĐã train đủ iters. Không tạo config resume.")
        print(f"   Muốn train thêm: tăng 'iters' trong {CONFIG_BASE.name} rồi chạy lại.")
        CONFIG_RESUME.unlink(missing_ok=True)
        sys.exit(0)

    config["resume_adapter_file"] = str(ckpt.relative_to(ROOT))
    config["iters"] = remaining

    # Optimizer state không được lưu lại, nên vào lại bằng lr thấp + warmup ngắn
    # để không phá adapter đã học.
    schedule = config.get("lr_schedule")
    if isinstance(schedule, dict) and schedule.get("arguments"):
        peak, _, end = (list(schedule["arguments"]) + [1.0e-5])[:3]
        warmup = min(20, max(1, remaining // 10))
        schedule["warmup"] = warmup
        schedule["arguments"] = [peak / 2, max(remaining - warmup, 1), end]

    CONFIG_RESUME.write_text(
        "# TỰ SINH bởi training/setup_resume.py - đừng sửa tay, sửa lora_config.yaml.\n"
        + yaml.safe_dump(config, allow_unicode=True, sort_keys=False),
        "utf-8",
    )
    print(f"\nĐã tạo {CONFIG_RESUME.name} (iters={remaining}, resume từ {ckpt.name})")
    print("Chạy: bash training/train.sh")


if __name__ == "__main__":
    main()
