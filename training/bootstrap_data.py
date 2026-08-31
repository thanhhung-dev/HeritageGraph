#!/usr/bin/env python3
"""
KHÔNG DÙNG NỮA - dùng training/bootstrap_deep_qa.py.

Lý do giữ lại chỉ để tham khảo: (1) đọc từ graphrag/input/ - đường dẫn không còn
tồn tại, corpus giờ nằm ở data/corpus/; (2) SYSTEM ở đây là bản COPY cũ, định
dạng trích nguồn không có url, khác backend/core/prompt.py - train bằng file này
sẽ lệch với lúc serve.

Bootstrap training data tự nhiên từ corpus Huế-Đà Nẵng.
Dùng chính Qwen local (qua mlx-lm) làm "teacher" sinh mẫu.

Input:  graphrag/input/*.txt (chunks Wikipedia)
Output: data/train_natural.jsonl (mẫu tự nhiên, không JSON)

Chạy: python training/bootstrap_data.py
"""
import json
import random
import subprocess
import sys
from pathlib import Path

random.seed(42)

CHUNKS_DIR = Path("graphrag/input")
OUT_TRAIN = Path("data/train_natural.jsonl")
OUT_VALID = Path("data/valid_natural.jsonl")

SYSTEM = """Bạn là trợ lý văn hóa dân gian Việt Nam, chuyên về Đà Nẵng và Huế.
Trả lời văn phong trang trọng, giàu tính kể chuyện, tự nhiên như người kể chuyện.
Luôn trích nguồn khi dùng thông tin (định dạng: [Nguồn: <trích đoạn ngắn>]).
Không bịa thông tin ngoài nguồn - nếu không có thì từ chối lịch sự."""


def load_chunks():
    """Đọc tất cả chunks từ graphrag/input/."""
    chunks = []
    for f in CHUNKS_DIR.glob("*.txt"):
        for c in f.read_text("utf-8").split("\n\n---\n\n"):
            if 200 < len(c) < 1500:
                chunks.append(c)
    print(f"loaded {len(chunks)} chunks")
    return chunks


def call_qwen(prompt: str, max_tokens: int = 400) -> str | None:
    """Gọi Qwen local qua mlx_lm.generate CLI.

    Returns None nếu lỗi.
    """
    try:
        result = subprocess.run(
            ["mlx_lm.generate", "--model", "./models/qwen-fused",
             "--prompt", prompt, "--max-tokens", str(max_tokens), "--quiet"],
            capture_output=True, text=True, timeout=120,
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"  [ERR] {e}")
        return None


# Các dạng prompt sinh câu hỏi đa dạng
QUESTION_TEMPLATES = [
    "Hãy kể về {topic} dựa trên nguồn sau.",
    "{topic} có ý nghĩa gì?",
    "Giới thiệu về {topic}.",
    "Kể câu chuyện về {topic}.",
    "{topic} có gì đặc biệt?",
]


def generate_sample(chunk: str, idx: int) -> dict | None:
    """Sinh 1 mẫu tự nhiên từ chunk."""
    # Lấy topic từ câu đầu của chunk (heuristic đơn giản)
    first_sentence = chunk.split(".")[0][:80]
    topic = first_sentence.strip()

    # Random chọn template câu hỏi
    template = random.choice(QUESTION_TEMPLATES)
    question = template.format(topic=topic)

    # Sinh câu trả lời từ Qwen
    prompt = f"{SYSTEM}\n\nNguồn: {chunk}\n\nCâu hỏi: {question}"
    answer = call_qwen(prompt)
    if not answer or "không tìm thấy" in answer.lower():
        return None

    return {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Nguồn: {chunk}\n\nCâu hỏi: {question}"},
            {"role": "assistant", "content": answer},
        ]
    }


def generate_refusal_sample() -> dict:
    """Sinh mẫu refusal (model từ chối khi không có nguồn)."""
    questions = [
        "Lễ hội Đền Hùng có nguồn gốc từ thời nào?",
        "Bài chòi phổ biến ở những tỉnh nào?",
        "Nghệ thuật cải lương có từ bao giờ?",
        "Ca trù có ở Huế không?",
        "Hát chầu văn là gì?",
    ]
    q = random.choice(questions)
    return {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Nguồn: (không có)\n\nCâu hỏi: {q}"},
            {"role": "assistant", "content": "Không tìm thấy thông tin này trong nguồn được cung cấp. Vui lòng cung cấp thêm tài liệu tham khảo để tôi trả lời chính xác hơn."},
        ]
    }


def main():
    if not CHUNKS_DIR.exists():
        print(f"ERROR: {CHUNKS_DIR} không tồn tại.")
        print("Chạy: python ingestion/chunk_corpus_mt.py trước")
        sys.exit(1)

    chunks = load_chunks()
    if not chunks:
        print("ERROR: không có chunk nào.")
        sys.exit(1)

    # Sinh N mẫu từ chunks
    n_target = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    n_refusal = max(n_target // 10, 20)  # 10% là refusal

    samples = []
    print(f"\nSinh {n_target} mẫu tự nhiên từ chunks...")
    for i, chunk in enumerate(random.sample(chunks, min(n_target, len(chunks)))):
        if (i + 1) % 20 == 0:
            print(f"  [{i+1}/{n_target}] generated {len(samples)} mẫu OK")
        s = generate_sample(chunk, i)
        if s:
            samples.append(s)

    # Thêm mẫu refusal
    print(f"\nThêm {n_refusal} mẫu refusal...")
    for _ in range(n_refusal):
        samples.append(generate_refusal_sample())

    # Lưu
    OUT_TRAIN.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TRAIN.open("w", encoding="utf-8") as f:
        for s in samples[:-20]:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with OUT_VALID.open("w", encoding="utf-8") as f:
        for s in samples[-20:]:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"\n✅ wrote {len(samples) - 20} train, 20 valid → {OUT_TRAIN.parent}")
    print("\nĐặc điểm:")
    print(f"  - Tất cả output là văn xuôi tự nhiên")
    print(f"  - {n_refusal} mẫu refusal (~{n_refusal * 100 // len(samples)}%)")
    print(f"  - Có [Nguồn: ...] trong mỗi mẫu")
    print(f"\nReview tay trước khi train! Mở: {OUT_TRAIN}")


if __name__ == "__main__":
    main()
