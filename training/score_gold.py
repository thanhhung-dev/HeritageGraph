#!/usr/bin/env python3
"""
Đánh giá 4 metric chính trên gold set:
  1. NER F1 (theo 4 loại: người, địa điểm, sự kiện, thời gian)
  2. Citation Precision: trong các citation model đưa ra, bao nhiêu % có trong nguồn
  3. Refusal Accuracy: câu hỏi ngoài nguồn → model có từ chối đúng không
  4. Style Score: đánh giá tay 1-5 cho văn phong kể chuyện

Gold set format (JSONL):
  {"id": "001", "task": "ner", "input": "...", "expected": {...}}
  {"id": "002", "task": "qa", "input": "...", "source": "...", "expected_citations": ["..."]}
  {"id": "003", "task": "refusal", "input": "...", "expected_refusal": true}

Usage:
  python scripts/score_gold.py --model ./qwen-7b-lora-fused --gold ./eval/gold.jsonl --out ./eval/report.json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


# ---------- 1. NER F1 ----------

def parse_ner_output(text: str) -> dict[str, list[str]]:
    """Parse JSON từ model output; fallback regex nếu model lỡ thêm text thừa."""
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return {"người": [], "địa điểm": [], "sự kiện": [], "thời gian": []}
    try:
        obj = json.loads(m.group(0))
        return {
            "người": list(obj.get("người", [])),
            "địa điểm": list(obj.get("địa điểm", [])),
            "sự kiện": list(obj.get("sự kiện", [])),
            "thời gian": list(obj.get("thời gian", [])),
        }
    except json.JSONDecodeError:
        return {"người": [], "địa điểm": [], "sự kiện": [], "thời gian": []}


def ner_f1(pred: list[str], gold: list[str]) -> tuple[float, float, float]:
    pset = {x.strip().lower() for x in pred}
    gset = {x.strip().lower() for x in gold}
    if not pset and not gset:
        return 1.0, 1.0, 1.0
    if not pset or not gset:
        return 0.0, 0.0, 0.0
    tp = len(pset & gset)
    p = tp / len(pset)
    r = tp / len(gset)
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f1


# ---------- 2. Citation Precision ----------

def extract_citations(text: str) -> list[str]:
    """Tìm các marker trích dẫn: [Nguồn: ...], (Nguồn ...), v.v."""
    patterns = [
        r"\[Nguồn:\s*([^\]]+)\]",
        r"\(Nguồn:\s*([^)]+)\)",
        r"Nguồn:\s*([^\n\.]+)",
    ]
    out: list[str] = []
    for pat in patterns:
        out.extend(m.strip() for m in re.findall(pat, text))
    return out


def citation_precision(pred_cites: list[str], source: str) -> float:
    """% citation có thật sự xuất hiện trong source (substring match, case-insensitive)."""
    if not pred_cites:
        return 1.0  # không cite = không sai
    src_lower = source.lower()
    hit = sum(1 for c in pred_cites if c.lower() in src_lower)
    return hit / len(pred_cites)


# ---------- 3. Refusal Accuracy ----------

REFUSAL_MARKERS = [
    "không tìm thấy",
    "không có thông tin",
    "ngoài phạm vi",
    "không được cung cấp",
    "không đủ thông tin",
]


def is_refusal(text: str) -> bool:
    t = text.lower()
    return any(m in t for m in REFUSAL_MARKERS)


# ---------- 4. Style Score (đánh tay) ----------

def style_template() -> dict[str, Any]:
    """Trả về template trống để con người tự chấm sau."""
    return {"scores": {}, "notes": "Chấm tay 1-5 theo: tính kể chuyện, trang trọng, tự nhiên"}


# ---------- Driver ----------

def run_mlx_generate(model: str, prompt: str, max_tokens: int = 512) -> str:
    """Gọi mlx_lm.generate qua CLI; đơn giản nhưng chậm — chuyển sang mlx_lm API nếu cần tốc độ."""
    cmd = [
        "mlx_lm.generate",
        "--model", model,
        "--prompt", prompt,
        "--max-tokens", str(max_tokens),
        "--quiet",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=180)
        return out.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"[ERROR] {e.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "[ERROR] timeout"


SYSTEM = (
    "Bạn là trợ lý văn hóa dân gian Việt Nam. "
    "Trích xuất entity chính xác theo 4 loại: người, địa điểm, sự kiện, thời gian. "
    "Trả lời văn phong trang trọng, giàu tính kể chuyện. "
    "Luôn trích nguồn khi dùng thông tin. Không bịa thông tin ngoài nguồn."
)


def build_prompt(sample: dict[str, Any]) -> str:
    task = sample["task"]
    if task == "ner":
        return f"{SYSTEM}\n\nTrích entity (người, địa điểm, sự kiện, thời gian) từ:\n\n{sample['input']}"
    if task == "qa":
        return (
            f"{SYSTEM}\n\nNguồn: {sample.get('source','')}\n\n"
            f"Câu hỏi: {sample['input']}\n\n"
            f"Trả lời kèm [Nguồn: ...]"
        )
    if task == "refusal":
        return f"{SYSTEM}\n\nNguồn: {sample.get('source','(không có)')}\n\nCâu hỏi: {sample['input']}"
    return sample["input"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--gold", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--max-tokens", type=int, default=512)
    args = ap.parse_args()

    samples = [json.loads(l) for l in args.gold.read_text("utf-8").splitlines() if l.strip()]

    ner_scores: dict[str, list[float]] = {"người": [], "địa điểm": [], "sự kiện": [], "thời gian": []}
    cite_scores: list[float] = []
    refusal_correct = 0
    refusal_total = 0
    style_samples: list[dict[str, Any]] = []

    for i, s in enumerate(samples, 1):
        prompt = build_prompt(s)
        print(f"[{i}/{len(samples)}] task={s['task']} id={s.get('id','')}", file=sys.stderr)
        out = run_mlx_generate(args.model, prompt, args.max_tokens)

        if s["task"] == "ner":
            pred = parse_ner_output(out)
            gold = s["expected"]
            for cat in ner_scores:
                _, _, f1 = ner_f1(pred[cat], gold.get(cat, []))
                ner_scores[cat].append(f1)

        elif s["task"] == "qa":
            pred_cites = extract_citations(out)
            src = s.get("source", "")
            cite_scores.append(citation_precision(pred_cites, src))
            style_samples.append({"id": s.get("id"), "input": s["input"], "output": out})

        elif s["task"] == "refusal":
            refusal_total += 1
            if bool(s.get("expected_refusal", False)) == is_refusal(out):
                refusal_correct += 1

    report = {
        "n_samples": len(samples),
        "ner_macro_f1_by_type": {k: (sum(v) / len(v) if v else 0.0) for k, v in ner_scores.items()},
        "ner_overall_f1": (
            sum(sum(v) for v in ner_scores.values()) / sum(len(v) for v in ner_scores.values())
            if any(ner_scores.values()) else 0.0
        ),
        "citation_precision": (sum(cite_scores) / len(cite_scores)) if cite_scores else None,
        "refusal_accuracy": (refusal_correct / refusal_total) if refusal_total else None,
        "style_samples_pending_manual": style_samples,
    }
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2), "utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
