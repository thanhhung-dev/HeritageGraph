#!/usr/bin/env python3
"""Sinh mẫu train cho CÂU KIỂM CHỨNG - "X ở Đà Nẵng đúng không?".

VẤN ĐỀ. Hỏi "Chùa Thiên Mụ ở Đà Nẵng đúng không", model trả lời "một địa điểm
nổi tiếng ở Đàng Trong... di sản văn hóa quý giá của địa phương" - né tiền đề
sai bằng cách nói vòng. Trong 305 mẫu của data/train_v3.jsonl KHÔNG có mẫu nào
dạng phản biện, model chưa từng thấy hình dạng "bác bỏ trước, kể sau".

SINH DETERMINISTIC, KHÔNG NHỜ LLM. Câu hỏi đúng/sai được suy từ metadata
(`region`, `category` trong locations_index.json) nên đáp án biết chắc. Nhờ
teacher đặt loại câu này là để nó bịa ground truth mà không có cách phát hiện.

BA RÀNG BUỘC, phá cái nào cũng đủ làm hỏng kết quả:

1. NGUỒN PHẢI CHỨA BẰNG CHỨNG. Mẫu nào có đáp án khẳng định "Huế" mà đoạn nguồn
   không chứa chữ "Huế" thì BỎ MẪU, không sửa đáp án. Để lại là dạy model trả
   lời bằng ký ức tham số - tức là dạy nó bịa, đúng bệnh đang cần chữa.
2. CÂN BẰNG ĐÚNG/SAI ~50/50. Lệch về "không đúng" thì model học phản đối mọi
   thứ, kể cả câu đúng. Script tự cân và in ra tỉ lệ.
3. ĐỊNH DẠNG GIỐNG HỆT 305 mẫu cũ: phán quyết -> đính chính -> [Nguồn: ...].
   Đổi hình dạng đáp án là làm loãng thứ adapter đã học tốt.

KHÔNG SAO NGUYÊN VĂN. Thân bài sinh 100% từ template + metadata, không lấy câu
nào từ nguồn. Bản đầu của script này có thêm 1-2 câu "kể tiếp" copy từ nguồn:
audit đo ra 130/130 mẫu vượt ngưỡng 14 từ, trung vị 57 từ liên tiếp trùng nguồn -
đúng lỗi mà bootstrap_v3.py được viết ra để chống. Phần verbatim duy nhất được
phép là trích dẫn trong [Nguồn: ...], như mọi mẫu khác.

Nguồn lấy qua ĐÚNG retrieval lúc serve (backend/core/rag.retrieve_context), không
tự chọn chunk: mẫu train phải có `Nguồn:` cùng hình dạng với lúc chạy thật.

  # sinh + xem báo cáo
  backend/.venv/bin/python training/bootstrap_verify.py

  # trộn vào data/train_v3.jsonl và data/valid_v3.jsonl
  backend/.venv/bin/python training/bootstrap_verify.py --merge
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend.core.corpus import load_docs  # noqa: E402
from backend.core.prompt import SYSTEM, user_msg  # noqa: E402
from backend.core.rag import retrieve_context  # noqa: E402
from backend.core.textutil import sentences, strip_accents  # noqa: E402
from training.bootstrap_deep_qa import SEED, split_docs  # noqa: E402
from training.bootstrap_v3 import (  # noqa: E402
    OUT_TRAIN,
    OUT_VALID,
    read_jsonl,
    write_jsonl,
)

OUT_VERIFY_TRAIN = ROOT / "data" / "verify_train.jsonl"
OUT_VERIFY_VALID = ROOT / "data" / "verify_valid.jsonl"

# Tỉ lệ tối đa mà mẫu kiểm chứng được chiếm trong tập train. Sinh hết cặp
# đúng/sai cho 45 bài ra 130 mẫu = 30% tập - quá nhiều cho MỘT khuôn câu trả lời
# rất cứng, model sẽ bắt đầu chào "Vâng, đúng vậy." cả với câu hỏi thường. 18%
# đủ để dạy hình dạng mà không lấn văn phong kể chuyện của 305 mẫu cũ.
MAX_SHARE = 0.18

REGIONS = ("Huế", "Đà Nẵng")

# Nhãn category -> cách gọi trong câu hỏi tiếng Việt tự nhiên.
CATEGORY_PHRASE = {
    "Ẩm thực": "một món ăn",
    "Di tích lịch sử": "một di tích lịch sử",
    "Danh thắng": "một danh thắng",
    "Lễ hội": "một lễ hội",
    "Nghệ thuật": "một loại hình nghệ thuật",
    "Làng nghề": "một làng nghề",
}

# --- Mẫu câu hỏi -------------------------------------------------------------
# Đa dạng cách hỏi nhưng KHÔNG đa dạng cách trả lời: hình dạng đáp án phải cố
# định để adapter học được một khuôn duy nhất.
REGION_QUESTIONS = (
    "{name} ở {region} đúng không?",
    "{name} có phải ở {region} không?",
    "{name} nằm ở {region} phải không?",
    "Nghe nói {name} ở {region}, đúng chứ?",
)
CATEGORY_QUESTIONS = (
    "{name} là {phrase} đúng không?",
    "{name} có phải là {phrase} không?",
)

# --- Mẫu đáp án --------------------------------------------------------------
# Phán quyết đứng ĐẦU: đó là thứ người hỏi cần, và là hình dạng model phải học.
# Toàn bộ thân bài ghép từ template + metadata, KHÔNG lấy câu nào từ nguồn -
# xem phần "KHÔNG SAO NGUYÊN VĂN" ở docstring module.
YES_LEAD = (
    "Vâng, đúng vậy.",
    "Đúng vậy.",
    "Chính xác.",
)
NO_LEAD = (
    "Thưa bạn, thông tin này chưa chính xác.",
    "Không phải vậy ạ.",
    "Xin phép được đính chính:",
)

REGION_YES = "{name} thuộc {region}."
REGION_NO = "{name} không thuộc {region} mà thuộc {truth}."
CATEGORY_YES = "{name} đúng là {phrase} của {region}."
CATEGORY_NO = "{name} không phải {wrong} mà là {truth} của {region}."

# Câu kết, cũng thuần template. Có mặt để đáp án không cụt lủn một dòng - văn
# phong "giàu tính kể chuyện" mà SYSTEM đòi - nhưng không thêm dữ kiện nào.
REGION_TAIL = (
    "Đây là một trong những di sản tiêu biểu của {truth}.",
    "Bạn có thể tìm đến {truth} nếu muốn tham quan.",
    "Xin bạn lưu ý điều này khi tìm hiểu về {truth}.",
)


def _evidence_sentence(source: str, needle: str) -> str:
    """Câu trong nguồn có chứa `needle` - dùng làm trích dẫn.

    Trả về "" nếu không có: khi đó mẫu bị BỎ. Đây là cổng thực thi ràng buộc 1.
    """
    plain_needle = strip_accents(needle)
    for sent in sentences(source):
        if plain_needle in strip_accents(sent):
            return sent
    return ""


def _make_sample(question: str, source: str, answer_body: str, quote: str,
                 url: str) -> dict:
    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_msg(source, question)},
        {"role": "assistant", "content": f"{answer_body} [Nguồn: {quote} — {url}]"},
    ]}


def _tail(rng: random.Random, truth: str) -> str:
    """Câu kết thuần template.

    Bản đầu lấy 1-2 câu từ nguồn ở đây và audit đo ra 130/130 mẫu copy nguyên
    văn (trung vị 57 từ liên tiếp). Câu kết không mang dữ kiện nên không cần
    nguồn - ghép từ template là đủ và không dạy model photocopy.
    """
    return rng.choice(REGION_TAIL).format(truth=truth)


def region_samples(doc: dict, rng: random.Random, stats: Counter) -> list[dict]:
    """Cặp (ĐÚNG, SAI) về vùng cho một bài. Bỏ cả cặp nếu thiếu bằng chứng."""
    truth = doc["region"]
    wrong = next(r for r in REGIONS if r != truth)
    out: list[dict] = []

    for region, is_true in ((truth, True), (wrong, False)):
        question = rng.choice(REGION_QUESTIONS).format(name=doc["name"], region=region)
        source, _hits = retrieve_context(question)
        if not source:
            stats["bỏ: retrieval không trả nguồn"] += 1
            continue
        # Bằng chứng luôn là VÙNG THẬT, kể cả với câu hỏi sai: muốn bác "ở Đà
        # Nẵng" thì nguồn phải chứng minh được "ở Huế".
        quote = _evidence_sentence(source, truth)
        if not quote:
            stats["bỏ: nguồn không có bằng chứng vùng"] += 1
            continue
        if is_true:
            body = f"{rng.choice(YES_LEAD)} {REGION_YES.format(name=doc['name'], region=truth)}"
        else:
            body = (f"{rng.choice(NO_LEAD)} "
                    f"{REGION_NO.format(name=doc['name'], region=region, truth=truth)}")
        body = f"{body} {_tail(rng, truth)}"
        out.append(_make_sample(question, source, body, quote, doc["url"]))
        stats["nhận: vùng ĐÚNG" if is_true else "nhận: vùng SAI"] += 1
    return out


def category_samples(doc: dict, rng: random.Random, stats: Counter) -> list[dict]:
    """Cặp (ĐÚNG, SAI) về loại. Bằng chứng là câu định nghĩa của wiki."""
    truth = doc["category"]
    if truth not in CATEGORY_PHRASE:
        return []
    wrong = next(c for c in CATEGORY_PHRASE if c != truth)
    out: list[dict] = []

    for category, is_true in ((truth, True), (wrong, False)):
        phrase = CATEGORY_PHRASE[category]
        question = rng.choice(CATEGORY_QUESTIONS).format(name=doc["name"], phrase=phrase)
        source, _hits = retrieve_context(question)
        if not source:
            stats["bỏ: retrieval không trả nguồn"] += 1
            continue
        # Bằng chứng loại: câu nào trong nguồn nhắc chính tên bài - câu định nghĩa
        # của wiki ("Mì Quảng là một loại mì ở Đà Nẵng...") gần như luôn là câu đó.
        quote = _evidence_sentence(source, doc["name"])
        if not quote:
            stats["bỏ: nguồn không có câu định nghĩa"] += 1
            continue
        if is_true:
            body = (f"{rng.choice(YES_LEAD)} "
                    f"{CATEGORY_YES.format(name=doc['name'], phrase=phrase, region=doc['region'])}")
        else:
            body = (f"{rng.choice(NO_LEAD)} "
                    f"{CATEGORY_NO.format(name=doc['name'], wrong=phrase, truth=CATEGORY_PHRASE[truth], region=doc['region'])}")
        body = f"{body} {_tail(rng, doc['region'])}"
        out.append(_make_sample(question, source, body, quote, doc["url"]))
        stats["nhận: loại ĐÚNG" if is_true else "nhận: loại SAI"] += 1
    return out


def build(docs: list[dict], rng: random.Random, stats: Counter) -> list[dict]:
    rows: list[dict] = []
    for doc in docs:
        rows.extend(region_samples(doc, rng, stats))
        rows.extend(category_samples(doc, rng, stats))
    return rows


# --- Kiểm tra sau khi sinh ---------------------------------------------------

def is_refutation(row: dict) -> bool:
    answer = row["messages"][-1]["content"]
    return any(answer.startswith(lead) for lead in NO_LEAD)


def source_of(row: dict) -> str:
    head = row["messages"][1]["content"].split("\n\nCâu hỏi:")[0]
    return head[len("Nguồn: "):] if head.startswith("Nguồn: ") else head


def check_evidence(rows: list[dict]) -> list[str]:
    """Mọi câu trích dẫn PHẢI là chuỗi có thật trong đoạn nguồn của cùng mẫu.

    Đây là ràng buộc 1, kiểm lại một lần nữa sau khi sinh: cổng lúc sinh có thể
    bị sửa hỏng về sau mà không ai biết, còn báo cáo này thì đọc được bằng mắt.
    """
    bad: list[str] = []
    for i, row in enumerate(rows):
        answer = row["messages"][-1]["content"]
        if "[Nguồn:" not in answer:
            bad.append(f"mẫu {i}: thiếu [Nguồn: ...]")
            continue
        quote = answer.split("[Nguồn:", 1)[1].rsplit("—", 1)[0].strip()
        if quote not in source_of(row):
            bad.append(f"mẫu {i}: trích dẫn không có trong nguồn: {quote[:50]!r}")
    return bad


def balance_report(rows: list[dict], label: str) -> None:
    n_no = sum(1 for r in rows if is_refutation(r))
    n_yes = len(rows) - n_no
    pct = f"{n_no / len(rows):.0%}" if rows else "0%"
    print(f"  {label}: {len(rows):>3} mẫu | {n_yes} khẳng định / {n_no} phản biện ({pct})")


def rebalance(rows: list[dict], rng: random.Random, cap: int | None = None) -> list[dict]:
    """Cân khẳng định/phản biện về ~50/50, đồng thời giới hạn tổng số mẫu.

    `cap` là số mẫu tối đa; cắt ĐỀU hai nhóm để tỉ lệ không lệch sau khi cắt.
    """
    yes = [r for r in rows if not is_refutation(r)]
    no = [r for r in rows if is_refutation(r)]
    keep = min(len(yes), len(no))
    if cap is not None:
        keep = min(keep, max(cap // 2, 1))
    rng.shuffle(yes)
    rng.shuffle(no)
    out = yes[:keep] + no[:keep]
    rng.shuffle(out)
    return out


def sync_system(rows: list[dict]) -> int:
    """Ghi lại SYSTEM hiện tại vào mọi mẫu. Trả về số mẫu bị đổi.

    Thêm quy tắc đính chính vào SYSTEM (backend/core/prompt.py) làm 305 mẫu cũ
    mang SYSTEM CŨ - model sẽ được train trên một prompt và serve bằng prompt
    khác, đúng loại lệch mà prompt.py được viết ra để chống. An toàn khi ghi đè:
    thân câu trả lời của mẫu cũ do template hoặc teacher (dùng TEACHER_SYSTEM
    riêng) sinh ra, không phụ thuộc SYSTEM.
    """
    changed = 0
    for row in rows:
        if row["messages"][0]["content"] != SYSTEM:
            row["messages"][0]["content"] = SYSTEM
            changed += 1
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--merge", action="store_true",
                    help=f"trộn vào {OUT_TRAIN.name} / {OUT_VALID.name}")
    args = ap.parse_args()

    rng = random.Random(SEED)
    docs, _skipped = load_docs()
    train_docs, valid_docs = split_docs(docs)

    stats: Counter = Counter()
    print(f"=== Sinh mẫu kiểm chứng từ {len(docs)} bài "
          f"({len(train_docs)} train / {len(valid_docs)} valid) ===")
    # Giới hạn theo MAX_SHARE của tập ĐANG CÓ: n_extra / (n_cũ + n_extra) <= share
    n_old_train, n_old_valid = len(read_jsonl(OUT_TRAIN)), len(read_jsonl(OUT_VALID))
    cap_train = int(n_old_train * MAX_SHARE / (1 - MAX_SHARE))
    cap_valid = int(n_old_valid * MAX_SHARE / (1 - MAX_SHARE))
    train_rows = rebalance(build(train_docs, rng, stats), rng, cap_train)
    valid_rows = rebalance(build(valid_docs, rng, stats), rng, cap_valid)

    print("\n=== Cổng ===")
    for reason, n in stats.most_common():
        print(f"  {reason:<44} {n}")

    bad = check_evidence(train_rows) + check_evidence(valid_rows)
    if bad:
        print(f"\nERROR: {len(bad)} mẫu có trích dẫn không nằm trong nguồn:")
        for line in bad[:10]:
            print(f"  {line}")
        return 1
    print("\n  OK: mọi trích dẫn đều là chuỗi có thật trong đoạn nguồn")

    print("\n=== Cân bằng ===")
    balance_report(train_rows, "Train")
    balance_report(valid_rows, "Valid")

    write_jsonl(OUT_VERIFY_TRAIN, train_rows)
    write_jsonl(OUT_VERIFY_VALID, valid_rows)
    print(f"\n  → {OUT_VERIFY_TRAIN.relative_to(ROOT)}")
    print(f"  → {OUT_VERIFY_VALID.relative_to(ROOT)}")

    if not args.merge:
        print("\n  Xem mẫu rồi chạy lại với --merge để trộn vào tập train.")
        print("\n--- ví dụ 2 mẫu ---")
        for row in train_rows[:2]:
            print(f"\nQ: {row['messages'][1]['content'].split('Câu hỏi: ')[-1]}")
            print(f"A: {row['messages'][-1]['content'][:300]}")
        return 0

    for base, extra in ((OUT_TRAIN, train_rows), (OUT_VALID, valid_rows)):
        old = read_jsonl(base)
        n_sync = sync_system(old)
        if n_sync:
            print(f"\n  {base.name}: đồng bộ SYSTEM cho {n_sync} mẫu cũ "
                  "(prompt.py có quy tắc đính chính mới)")
        merged = old + extra
        rng.shuffle(merged)
        write_jsonl(base, merged)
        share = f"{len(extra) / len(merged):.0%}"
        print(f"  {base.name}: {len(old)} + {len(extra)} = {len(merged)} mẫu "
              f"(kiểm chứng chiếm {share})")

    # NER nằm ở file riêng (ner_train_v3.jsonl) nhưng cũng mang SYSTEM - phải
    # đồng bộ, nếu không nửa tập dùng prompt cũ nửa tập dùng prompt mới.
    for ner_path in (ROOT / "data" / "ner_train_v3.jsonl",
                     ROOT / "data" / "ner_valid_v3.jsonl"):
        if not ner_path.exists():
            continue
        rows = read_jsonl(ner_path)
        n_sync = sync_system(rows)
        if n_sync:
            write_jsonl(ner_path, rows)
            print(f"  {ner_path.name}: đồng bộ SYSTEM cho {n_sync} mẫu")

    n_train = len(read_jsonl(OUT_TRAIN))
    print(f"\n  Gợi ý iters cho lora_config.yaml (batch_size 2, ~3 epoch): "
          f"{max(n_train * 3 // 2, 100)}")
    print("  Train --fresh, ĐỪNG resume trên adapter cũ.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
