#!/usr/bin/env python3
"""
KHÔNG DÙNG NỮA - dùng training/bootstrap_deep_qa.py.

Lý do: (1) đọc corpus/wiki_by_location/ - corpus giờ ở data/corpus/; (2) SYSTEM ở
đây là bản COPY cũ (không có url trong trích nguồn, không có mục NER); (3) cuối
file in ra lệnh `cp ... data/train.jsonl`, chạy theo là ghi đè data thật bằng data
sai định dạng.

Sinh training data tự nhiên từ thông tin các địa điểm Huế - Đà Nẵng.

Quy trình:
1. Đọc 80 địa điểm đã crawl
2. Với mỗi địa điểm: 6-8 câu hỏi khác nhau × Qwen sinh trả lời
3. Thêm 30 mẫu refusal
4. Lưu ra data/train_by_location.jsonl

Yêu cầu: phải có models/qwen-fused (chạy train.sh + fuse.sh trước)
"""
import json
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from locations_hue_danang import get_all_locations

random.seed(42)

CORPUS_DIR = Path("corpus/wiki_by_location")
INDEX_FILE = Path("corpus/locations_index.json")
OUT_TRAIN = Path("data/train_by_location.jsonl")
OUT_VALID = Path("data/valid_by_location.jsonl")
MODEL_PATH = Path("models/qwen-fused")

SYSTEM = """Bạn là trợ lý văn hóa dân gian Việt Nam, chuyên về Đà Nẵng và Huế.
Trả lời văn phong trang trọng, giàu tính kể chuyện, tự nhiên như người kể chuyện.
Luôn trích nguồn khi dùng thông tin (định dạng: [Nguồn: <trích đoạn ngắn>]).
Không bịa thông tin ngoài nguồn - nếu không có thì từ chối lịch sự."""


# 8 dạng câu hỏi cho mỗi địa điểm
QUESTION_TYPES = [
    ("kể", "Hãy kể về {name}"),
    ("là_gì", "{name} là gì?"),
    ("ở_đâu", "{name} nằm ở đâu?"),
    ("khi_nào", "{name} được xây dựng/khởi lập vào thời gian nào?"),
    ("ý_nghĩa", "{name} có ý nghĩa lịch sử và văn hóa như thế nào?"),
    ("đặc_điểm", "{name} có những đặc điểm gì nổi bật?"),
    ("lịch_sử", "Lịch sử hình thành và phát triển của {name}?"),
    ("giá_trị", "{name} có giá trị gì đối với văn hóa Việt Nam?"),
]


def call_qwen(prompt: str, max_tokens: int = 400) -> str | None:
    """Gọi Qwen local sinh câu trả lời."""
    if not MODEL_PATH.exists():
        print(f"  ERROR: {MODEL_PATH} chưa tồn tại. Chạy train.sh + fuse.sh trước.")
        return None
    try:
        result = subprocess.run(
            ["mlx_lm.generate", "--model", str(MODEL_PATH),
             "--prompt", prompt, "--max-tokens", str(max_tokens)],
            capture_output=True, text=True, timeout=180,
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"  [ERR] {e}")
        return None


def chunk_text(text: str, max_chunk_size: int = 1200) -> list[str]:
    """Chia text thành các chunks ~1200 chars."""
    text = text.replace("\n\n", "\n").strip()
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chunk_size, len(text))
        if end < len(text):
            for sep in [". ", ".\n", "; "]:
                cut = text.rfind(sep, start + max_chunk_size // 2, end)
                if cut > 0:
                    end = cut + len(sep)
                    break
        chunk = text[start:end].strip()
        if len(chunk) > 200:
            chunks.append(chunk)
        start = end
    return chunks


def generate_for_location(location_info: dict) -> list[dict]:
    """Sinh 6-8 mẫu cho 1 địa điểm."""
    samples = []
    file_path = CORPUS_DIR / location_info["file"]
    if not file_path.exists():
        return samples

    text = file_path.read_text("utf-8")
    chunks = chunk_text(text)
    if not chunks:
        return samples

    name = location_info["name"]
    used_chunks = set()

    for q_type, q_template in random.sample(QUESTION_TYPES, k=min(6, len(QUESTION_TYPES))):
        # Tìm chunk chưa dùng
        available = [c for i, c in enumerate(chunks) if i not in used_chunks]
        if not available:
            break
        chunk = random.choice(available)
        used_chunks.add(chunks.index(chunk))

        question = q_template.format(name=name)
        prompt = f"{SYSTEM}\n\nNguồn: {chunk}\n\nCâu hỏi: {question}"

        answer = call_qwen(prompt)
        if not answer or "không tìm thấy" in answer.lower():
            continue

        samples.append({
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"Nguồn: {chunk}\n\nCâu hỏi: {question}"},
                {"role": "assistant", "content": answer},
            ]
        })

    return samples


def add_refusal_samples(n: int = 30) -> list[dict]:
    """Tạo mẫu refusal (model từ chối khi nguồn trống)."""
    refusal_qs = [
        "Lễ hội Đền Hùng có từ bao giờ?",
        "Hát chầu văn là gì?",
        "Ca trù có ở Huế không?",
        "Múa rối nước phổ biến ở đâu?",
        "Quan họ là di sản của vùng nào?",
        "Lễ hội Lim diễn ra khi nào?",
        "Ca dao Việt Nam có bao nhiêu bài?",
        "Nghệ thuật cải lương từ thời nào?",
    ]
    samples = []
    for i in range(n):
        q = refusal_qs[i % len(refusal_qs)]
        samples.append({
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"Nguồn: (không có)\n\nCâu hỏi: {q}"},
                {"role": "assistant", "content": "Không tìm thấy thông tin này trong nguồn được cung cấp. Vui lòng cung cấp thêm tài liệu tham khảo để tôi trả lời chính xác hơn."},
            ]
        })
    return samples


def main():
    if not INDEX_FILE.exists():
        print(f"ERROR: chạy ingestion/crawl_by_location.py trước")
        sys.exit(1)

    if not MODEL_PATH.exists():
        print(f"ERROR: {MODEL_PATH} chưa có.")
        print("Chạy: bash training/train.sh && bash training/fuse.sh")
        sys.exit(1)

    data = json.loads(INDEX_FILE.read_text("utf-8"))
    locations = data["success"]
    print(f"=== Sinh training data cho {len(locations)} địa điểm ===\n")

    all_samples = []
    for i, loc in enumerate(locations, 1):
        print(f"[{i}/{len(locations)}] {loc['name']} ({loc['region']})")
        samples = generate_for_location(loc)
        all_samples.extend(samples)
        print(f"   → {len(samples)} mẫu (tổng: {len(all_samples)})")

    # Thêm refusal
    refusals = add_refusal_samples(30)
    all_samples.extend(refusals)
    print(f"\n+ {len(refusals)} mẫu refusal")

    # Shuffle
    random.shuffle(all_samples)

    # Lưu
    OUT_TRAIN.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TRAIN.open("w", encoding="utf-8") as f:
        for s in all_samples[:-30]:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with OUT_VALID.open("w", encoding="utf-8") as f:
        for s in all_samples[-30:]:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"\n=== Done ===")
    print(f"  Train: {len(all_samples) - 30}")
    print(f"  Valid: 30")
    print(f"  Trung bình: {(len(all_samples) - 30) // len(locations)} mẫu/địa điểm")
    print(f"\n  File: {OUT_TRAIN}")
    print(f"\n  Bước tiếp:")
    print(f"    1. Review tay ~30% mẫu (nano {OUT_TRAIN})")
    print(f"    2. cp {OUT_TRAIN} data/train.jsonl")
    print(f"    3. cp {OUT_VALID} data/valid.jsonl")
    print(f"    4. bash training/train.sh && bash training/fuse.sh")


if __name__ == "__main__":
    main()
