#!/usr/bin/env python3
"""Đo chất lượng retrieval - chạy được offline, không cần model, không cần mạng.

Đo hai thứ TÁCH BIỆT nhau, vì chúng hỏng theo hai cách khác nhau:
  1. recall  - câu hỏi TRONG phạm vi có lấy đúng bài không (retrieval)
  2. refusal - câu hỏi NGOÀI phạm vi có trả context rỗng không (cổng từ chối)

Đây là nửa dưới của công thức độ chính xác:
    P(đúng) = P(lấy đúng đoạn) x P(model trung thực với đoạn đó)
Nửa trên đo ở đây; nửa dưới do LoRA lo. Sửa retrieval mà không đo lại chỗ này
thì rất dễ nâng recall bằng cách phá cổng từ chối (và ngược lại).

Chạy: backend/.venv/bin/python eval/eval_retrieval.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.core.rag import retrieve_context          # noqa: E402
from backend.core.retriever import get_retriever       # noqa: E402

# (câu hỏi, tên bài ĐÚNG). Có cả câu KHÔNG DẤU vì người chat gõ không dấu rất
# thường xuyên - và đó là trường hợp mọi retrieval chỉ-có-dấu đều trả về rỗng.
IN_DOMAIN: list[tuple[str, str]] = [
    ("Lăng Minh Mạng được xây dựng năm nào?", "Lăng Minh Mạng"),
    ("lang minh mang o dau", "Lăng Minh Mạng"),
    ("Kiến trúc lăng Khải Định có gì đặc biệt?", "Lăng Khải Định"),
    ("Lăng Tự Đức còn có tên gọi khác là gì?", "Lăng Tự Đức"),
    ("Lăng Gia Long nằm ở đâu?", "Lăng Gia Long"),
    ("Hoàng thành Huế có mấy cửa?", "Hoàng thành Huế"),
    ("Nhã nhạc cung đình Huế được UNESCO công nhận năm nào?", "Nhã nhạc cung đình Huế"),
    ("Chùa Thiên Mụ do ai cho xây?", "Chùa Thiên Mụ"),
    ("Điện Hòn Chén thờ vị thần nào?", "Điện Hòn Chén"),
    ("Cầu Trường Tiền do ai thiết kế?", "Cầu Trường Tiền"),
    ("Đèo Hải Vân dài bao nhiêu km?", "Đèo Hải Vân"),
    ("Ngũ Hành Sơn gồm những ngọn núi nào?", "Ngũ Hành Sơn"),
    ("Bán đảo Sơn Trà có loài vật quý nào?", "Bán đảo Sơn Trà"),
    ("cao lau la mon gi", "Cao lầu"),
    ("Mì Quảng nấu bằng sợi mì gì?", "Mì Quảng"),
    ("me xung lam tu gi", "Mè xửng"),
    ("Bún bò Huế có nguồn gốc từ đâu?", "Bún bò Huế"),
    ("Cơm hến gồm những nguyên liệu nào?", "Cơm hến"),
    ("bao tang co vat cung dinh hue trung bay gi", "Bảo tàng Cổ vật Cung đình Huế"),
    ("Ca Huế được biểu diễn ở đâu?", "Ca Huế"),
    ("Festival Huế tổ chức mấy năm một lần?", "Festival Huế"),
    ("Hát tuồng khác gì với cải lương?", "Hát tuồng"),
    # ALIAS - người dùng gọi tên dân gian, không gọi tên chính thức của bài.
    # Trước khi có corpus/aliases.json, find_seeds trả rỗng -> cổng anchor của
    # rag.py ném sạch kết quả mà BM25 đã tìm ra với coverage 1.0.
    ("nhà thờ con gà ở đâu?", "Nhà thờ chính tòa Đà Nẵng"),
    ("nha tho con ga xay nam nao", "Nhà thờ chính tòa Đà Nẵng"),
    ("chùa Linh Mụ ở đâu?", "Chùa Thiên Mụ"),
    ("Đại nội Huế là gì?", "Hoàng thành Huế"),
    ("cầu Tràng Tiền dài bao nhiêu?", "Cầu Trường Tiền"),
    ("Khiêm Lăng là lăng của ai?", "Lăng Tự Đức"),
    ("kẹo mè xửng làm từ gì?", "Mè xửng"),
    ("điện Huệ Nam thờ ai?", "Điện Hòn Chén"),
]

# Ngoài phạm vi: phải trả context RỖNG để llm.py ghi "Nguồn: (không có)" và LoRA
# từ chối lịch sự. Trộn 3 loại: chủ đề khác hẳn, có vẻ du lịch nhưng sai vùng,
# và câu neo đúng miền nhưng hệ CHƯA có tư liệu.
OUT_OF_DOMAIN: list[str] = [
    "Giá bitcoin hôm nay bao nhiêu?",
    "Cách học tiếng Nhật nhanh nhất",
    "Giải phương trình bậc hai x^2 - 5x + 6 = 0",
    "Thời tiết Hà Nội ngày mai thế nào?",
    "Công thức làm bánh mì bơ tỏi",
    "Đội tuyển Việt Nam đá với ai tối nay?",
    "Cho tôi xin số điện thoại của bạn",
    "Vịnh Hạ Long có bao nhiêu hòn đảo?",       # di sản, nhưng KHÔNG thuộc corpus
    "Phở Hà Nội nấu thế nào?",                  # ẩm thực, nhưng sai vùng
    "Đàn Nam Giao thờ ai?",                     # có node trong graph, KHÔNG có bài
    # ALIAS NHẬP NHẰNG. corpus/aliases.json nhận "Nhà Thờ Lớn Đà Nẵng" nhưng
    # PHẢI từ chối "Nhà Thờ Lớn" trần - tên đó có ở Hà Nội, Sài Gòn. Đây là bẫy
    # mà việc thêm alias tạo ra, nên phải đo cùng lúc với recall.
    "Nhà thờ Lớn Hà Nội xây năm nào?",
    "Chùa Một Cột ở đâu?",
]

# BẰNG CHỨNG TRONG CONTEXT: (câu hỏi, chuỗi phải có mặt trong context).
#
# recall@1 chỉ đo chọn đúng BÀI, không đo chọn đúng CHUNK. Với câu sai tiền đề
# ("Chùa Thiên Mụ ở Đà Nẵng đúng không") bài luôn đúng, nhưng nếu context chỉ có
# mục "Tên gọi" và "Kiến trúc" thì model KHÔNG có chữ "Huế" nào để bác lại - nó
# lách bằng cách nói vòng, tức là bịa. Nhóm này đo đúng chỗ đó.
#
# Cân bằng ĐÚNG/SAI có chủ ý: chỉ test câu sai thì không phát hiện được khi hệ
# học thói phản đối mọi thứ.
EVIDENCE: list[tuple[str, str]] = [
    ("Chùa Thiên Mụ ở Đà Nẵng đúng không?", "Huế"),        # tiền đề SAI
    ("Chùa Thiên Mụ ở Huế đúng không?", "Huế"),            # tiền đề ĐÚNG
    ("chùa Linh Ứng ở Huế phải không?", "Đà Nẵng"),        # SAI
    ("Chùa Linh Ứng ở Đà Nẵng phải không?", "Đà Nẵng"),    # ĐÚNG
    ("Mì Quảng là món của Huế đúng không?", "Đà Nẵng"),    # SAI
    ("Cầu Rồng ở Huế đúng không?", "Đà Nẵng"),             # SAI
    ("Cơm hến là món của Huế đúng không?", "Huế"),         # ĐÚNG
    ("Lăng Tự Đức ở Đà Nẵng có phải không?", "Huế"),       # SAI
    ("nhà thờ con gà ở đâu?", "Đà Nẵng"),                  # alias + vị trí
    ("Lăng Minh Mạng xây năm nào?", "184"),                # intent thời gian
    # SCOPE + kiểm chứng: câu nêu region NGƯỢC với thực tế. Tên riêng phải thắng
    # scope, nếu lọc theo region trong câu thì loại đúng bài cần để bác lại.
    ("Cơm hến là món ăn của Đà Nẵng đúng không?", "Huế"),
    ("Cao lầu là món Huế phải không?", "Đà Nẵng"),
]

# SCOPE: (câu hỏi KHÔNG nêu tên riêng nào, region mong đợi, category mong đợi).
#
# Đây là nhóm "thu hẹp phạm vi": câu hỏi chỉ nêu vùng + loại, hệ phải tìm SÂU
# trong phạm vi hẹp thay vì xếp hạng nông trên cả 45 bài. Trước khi có lọc scope,
# "Huế có món ăn đặc sản nào" trả về Cao lầu + Mì Quảng - cả hai đều Đà Nẵng.
#
# ("Huế", "Làng nghề") KHÔNG có trong nhóm này: corpus chỉ có làng nghề Đà Nẵng,
# nên câu đó là trường hợp scope rỗng - _scope_pool bỏ lọc và trả về Đà Nẵng để
# model tự nói rõ, thay vì trả tay trắng.
SCOPE: list[tuple[str, str, str]] = [
    ("Đà Nẵng có món ăn gì đặc trưng?", "Đà Nẵng", "Ẩm thực"),
    ("Huế có món ăn đặc sản nào?", "Huế", "Ẩm thực"),
    ("kể tôi nghe về ẩm thực Huế", "Huế", "Ẩm thực"),
    ("Huế có lễ hội nào?", "Huế", "Lễ hội"),
    ("Đà Nẵng có làng nghề gì?", "Đà Nẵng", "Làng nghề"),
    ("Đà Nẵng có danh thắng nào?", "Đà Nẵng", "Danh thắng"),
    ("Huế có nghệ thuật gì?", "Huế", "Nghệ thuật"),
    ("di tích lịch sử ở Đà Nẵng", "Đà Nẵng", "Di tích lịch sử"),
]


def main() -> int:
    r = get_retriever()
    print(f"corpus: {len(r.chunks)} chunk / {len(r.doc_index)} bài\n")

    print("== TRONG PHẠM VI ==")
    top1 = top3 = 0
    for q, gold in IN_DOMAIN:
        res = r.retrieve(q, top_k=3)
        docs = [h["doc"] for h in res["hits"]]
        ok1, ok3 = bool(docs) and docs[0] == gold, gold in docs
        top1 += ok1
        top3 += ok3
        ctx, _ = retrieve_context(q)
        flag = "OK  " if ok1 else ("top3" if ok3 else "MISS")
        print(f"  {flag} ctx={len(ctx):5d} | {q[:46]:46s} -> {docs}")

    print("\n== NGOÀI PHẠM VI (phải rỗng) ==")
    refused = 0
    for q in OUT_OF_DOMAIN:
        res = r.retrieve(q, top_k=3)
        ctx, _ = retrieve_context(q)
        ok = not ctx
        refused += ok
        print(f"  {'OK  ' if ok else 'LEAK'} ctx={len(ctx):5d} | {q[:46]:46s} "
              f"anchored={res['anchored']} specific={res['specific'][:2]}")

    print("\n== BẰNG CHỨNG TRONG CONTEXT (chọn đúng CHUNK, không chỉ đúng bài) ==")
    evidenced = 0
    for q, needle in EVIDENCE:
        ctx, sources = retrieve_context(q)
        ok = needle in ctx
        evidenced += ok
        used = [s["chunk_id"] for s in sources if s["used_in_context"]]
        print(f"  {'OK  ' if ok else 'MISS'} {needle!r:10s} | {q[:40]:40s} -> {used}")

    print("\n== SCOPE (câu không nêu tên riêng - phải thu hẹp đúng vùng + loại) ==")
    scoped = 0
    for q, region, category in SCOPE:
        res = r.retrieve(q, top_k=3)
        top = res["hits"][0] if res["hits"] else None
        ok = bool(top) and top["region"] == region and top["category"] == category
        scoped += ok
        got = f"{top['doc']} ({top['region']}/{top['category']})" if top else "-"
        print(f"  {'OK  ' if ok else 'MISS'} {region}/{category:16s} | {q[:34]:34s} -> {got}")

    n_in, n_out = len(IN_DOMAIN), len(OUT_OF_DOMAIN)
    n_ev, n_sc = len(EVIDENCE), len(SCOPE)
    print(f"\nrecall@1 = {top1}/{n_in}   recall@3 = {top3}/{n_in}   "
          f"từ chối đúng = {refused}/{n_out}   bằng chứng = {evidenced}/{n_ev}   "
          f"scope = {scoped}/{n_sc}")
    return 0 if (top1 == n_in and refused == n_out
                 and evidenced == n_ev and scoped == n_sc) else 1


if __name__ == "__main__":
    raise SystemExit(main())
