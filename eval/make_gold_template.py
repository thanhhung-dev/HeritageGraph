#!/usr/bin/env python3
"""
Tạo gold eval set cho 4 metric, lấy từ CHÍNH corpus đã crawl.

Bản cũ viết tay 5 mẫu về Bát Tràng / Đông Hồ / Đền Hùng - toàn bộ nằm NGOÀI corpus
(miền Bắc, không phải Huế - Đà Nẵng). Đo model bằng những mẫu đó thì cả ba metric
đều sai hướng: model bị trừ điểm vì không biết thứ mà hệ thống chưa từng có nguồn.

Nguyên tắc của file này:
- Chỉ dùng các tài liệu thuộc split VALID của training/bootstrap_deep_qa.py, tức
  là những bài model KHÔNG được train trên. Dùng bài train thì đo trí nhớ.
- Phần NER được ĐIỀN SẴN bằng backend/core/nerlabel.py (nhãn suy ra từ graph
  deterministic). Đây là điểm phải nói thật trong báo cáo: nhãn máy sinh đo
  "model có học được bộ luật trích entity hay không", chưa phải "trích entity có
  đúng hay không". Muốn thành gold thật thì phải MỞ FILE RA SOÁT TAY - thêm cái
  regex bỏ sót, bỏ cái nó nhận sai. Việc soát nhanh vì nhãn đã có sẵn 90%.
- Câu trích dẫn kỳ vọng là câu NGUYÊN VĂN trong nguồn, nên citation precision đo
  được bằng so khớp chuỗi, không cần chấm tay.

Chạy: backend/.venv/bin/python eval/make_gold_template.py
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend.core.corpus import load_docs  # noqa: E402
from backend.core.nerlabel import allowed_names, n_labels, ner_label  # noqa: E402
from backend.core.textutil import contains_name, sentences, strip_accents  # noqa: E402
from training.bootstrap_deep_qa import split_docs  # noqa: E402

EVAL = ROOT / "eval"
SEED = 1234
NER_PER_DOC = 4
QA_PER_DOC = 3
MIN_LABELS = 3
SENT_CHARS = (60, 400)

# Câu hỏi QA: dùng dạng người dùng thật sẽ gõ, không phải dạng template lúc train,
# để đo được model có bám nguồn khi câu hỏi lệch khỏi văn phong training.
QA_QUESTIONS = [
    "Hãy kể cho tôi về {name}.",
    "{name} có gì đặc biệt?",
    "Lịch sử của {name} như thế nào?",
    "Vì sao {name} nổi tiếng?",
]

# Câu hỏi ngoài phạm vi corpus -> phải từ chối. Đều là di sản THẬT nhưng chưa crawl,
# nên đây là phép thử đúng: model không được suy đoán từ kiến thức nền của nó.
OUT_OF_SCOPE = [
    "Chùa Một Cột được xây năm nào?",
    "Kể về nhã nhạc của triều Lý ở Thăng Long.",
    "Phố cổ Hội An có bao nhiêu di tích được xếp hạng?",
    "Thành nhà Hồ ở Thanh Hoá do ai xây?",
    "Lễ hội Đền Hùng diễn ra vào ngày nào?",
]


def ner_samples(docs: list[dict]) -> list[dict]:
    out: list[dict] = []
    for doc in docs:
        allowed = allowed_names(" ".join(c["heading"] + " " + c["text"] for c in doc["chunks"]))
        cands = []
        for chunk in doc["chunks"]:
            for sent in sentences(chunk["text"]):
                if not SENT_CHARS[0] <= len(sent) <= SENT_CHARS[1]:
                    continue
                label = ner_label(sent, allowed)
                if n_labels(label) >= MIN_LABELS:
                    cands.append((sum(1 for v in label.values() if v), sent, label))
        cands.sort(key=lambda t: -t[0])
        for k, (_, sent, label) in enumerate(cands[:NER_PER_DOC], 1):
            out.append({
                "id": f"ner-{doc['name']}-{k}",
                "task": "ner",
                "input": sent,
                "expected": label,
                "_prefilled": True,   # xoá cờ này sau khi đã soát tay
            })
    return out


def qa_samples(docs: list[dict], rng: random.Random) -> list[dict]:
    out: list[dict] = []
    for doc in docs:
        chunks = [c for c in doc["chunks"] if len(c["text"]) > 200][:QA_PER_DOC]
        for k, chunk in enumerate(chunks, 1):
            sents = [s for s in sentences(chunk["text"]) if 40 <= len(s) <= 300]
            if not sents:
                continue
            out.append({
                "id": f"qa-{doc['name']}-{k}",
                "task": "qa",
                "input": rng.choice(QA_QUESTIONS).format(name=doc["name"]),
                "source": chunk["text"],
                # Mọi câu trong nguồn đều là trích dẫn hợp lệ; score_gold.py chỉ
                # kiểm tra citation model đưa ra CÓ trong source hay không.
                "expected_citations": sents[:3],
            })
    return out


def refusal_samples(docs: list[dict], rng: random.Random) -> list[dict]:
    out: list[dict] = []
    for i, q in enumerate(OUT_OF_SCOPE, 1):
        out.append({"id": f"refusal-noSrc-{i}", "task": "refusal", "input": q,
                    "source": "", "expected_refusal": True})

    # Nguồn SAI BÀI: nguồn có thật nhưng nói về nơi khác. Đây là lỗi hay gặp nhất
    # lúc chạy thật (retrieval lấy sai đoạn) và là chỗ model dễ bịa nhất.
    for i, doc in enumerate(docs, 1):
        others = [d for d in docs if d["name"] != doc["name"]]
        if not others:
            continue
        other = rng.choice(others)
        chunk = rng.choice(other["chunks"])
        if contains_name(strip_accents(chunk["text"]), doc["name"]):
            continue
        out.append({"id": f"refusal-wrongDoc-{i}", "task": "refusal",
                    "input": f"Hãy kể chi tiết về {doc['name']}.",
                    "source": chunk["text"], "expected_refusal": True})

    # Nguồn ĐÚNG -> KHÔNG được từ chối. Không có nhóm này thì một model từ chối
    # mọi câu vẫn đạt refusal accuracy 100%.
    for i, doc in enumerate(docs, 1):
        chunk = max(doc["chunks"], key=lambda c: len(c["text"]))
        out.append({"id": f"refusal-ok-{i}", "task": "refusal",
                    "input": f"Hãy kể chi tiết về {doc['name']}.",
                    "source": chunk["text"], "expected_refusal": False})
    return out


def main() -> int:
    rng = random.Random(SEED)
    docs, _ = load_docs()
    _, valid_docs = split_docs(docs)
    print(f"Gold lấy từ {len(valid_docs)} bài KHÔNG có trong train: "
          f"{', '.join(d['name'] for d in valid_docs)}")

    gold = ner_samples(valid_docs) + qa_samples(valid_docs, rng) + refusal_samples(valid_docs, rng)

    out = EVAL / "gold.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for s in gold:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    by_task: dict[str, int] = {}
    for s in gold:
        by_task[s["task"]] = by_task.get(s["task"], 0) + 1
    print(f"wrote {len(gold)} mẫu → {out}   {by_task}")

    types: dict[str, int] = {}
    for s in gold:
        if s["task"] == "ner":
            for t, v in s["expected"].items():
                types[t] = types.get(t, 0) + len(v)
    print(f"  entity trong gold NER theo loại: {types}")
    print("\nBƯỚC BẮT BUỘC: mở eval/gold.jsonl soát lại phần \"expected\" của các mẫu ner-*")
    print("(nhãn do máy điền). Soát xong thì xoá \"_prefilled\": true để biết mẫu nào đã kiểm.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
