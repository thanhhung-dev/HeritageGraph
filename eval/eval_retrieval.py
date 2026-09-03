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
    ("nhà thờ con gà ở đâu?", "Nhà thờ chính tòa Đà Nẵng"),
    ("nha tho con ga xay nam nao", "Nhà thờ chính tòa Đà Nẵng"),
    ("chùa Linh Mụ ở đâu?", "Chùa Thiên Mụ"),
    ("Đại nội Huế là gì?", "Hoàng thành Huế"),
    ("cầu Tràng Tiền dài bao nhiêu?", "Cầu Trường Tiền"),
    ("Khiêm Lăng là lăng của ai?", "Lăng Tự Đức"),
    ("kẹo mè xửng làm từ gì?", "Mè xửng"),
    ("điện Huệ Nam thờ ai?", "Điện Hòn Chén"),
]

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
    "Nhà thờ Lớn Hà Nội xây năm nào?",
    "Chùa Một Cột ở đâu?",
    "phường Cầu Giấy có di tích gì?",
    "quận Ba Đình có lăng nào?",
    "phường Bến Nghé có món ăn nào?",
    "xã Đông Anh có lễ hội gì?",
]

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
    # GIẢ ĐỊNH LÀ MỘT BÀI KHÁC TRONG CORPUS. "phường Ngũ Hành Sơn" là tên một bài
    # thật, nên cả hai tên đều được gọi đúng tên và bài có lexical cao hơn (tên dài
    # hơn) thắng - hệ đi lấy tư liệu về GIẢ ĐỊNH thay vì về thứ đang được hỏi, và
    # model xác nhận "Đúng vậy, Lăng Tự Đức thuộc phường Ngũ Hành Sơn" bằng một
    # đoạn nguồn chỉ chứng minh Ngũ Hành Sơn ở Đà Nẵng.
    ("Lăng Tự Đức ở phường Ngũ Hành Sơn đúng không?", "Thủy Xuân"),
    ("Chùa Thiên Mụ ở Ngũ Hành Sơn đúng không?", "Huế"),
    ("Cầu Rồng ở sông Hương đúng không?", "Đà Nẵng"),
    ("Lăng Khải Định nằm ở làng Non Nước phải không?", "Huế"),
    ("Chùa Linh Ứng ở Bán đảo Sơn Trà đúng không?", "Sơn Trà"),
    # CÂU KIỂM CHỨNG KHÔNG DẤU. Nhóm IN_DOMAIN có câu không dấu nhưng chỉ đo CHỌN
    # ĐÚNG BÀI, không đo có bằng chứng để bác tiền đề sai. Truy vấn không dấu sinh
    # nhiều n-gram phổ biến làm loãng tín hiệu nên đoạn mở đầu - nơi duy nhất ghi
    # tỉnh/thành - tụt hạng trong bài: "lang khai dinh o da nang dung khong" đo được
    # chunk #0 ở hạng 4, ngoài INJECT_PER_DOC cũ (3), nên context về tay model không
    # có chữ "Huế" nào và model xác nhận một điều sai. Đo trên 45 bài: câu không dấu
    # mất bằng chứng vùng ở 7 bài, câu có dấu ở 4 bài - nên nhóm này phải có mặt.
    ("lang khai dinh o da nang dung khong", "Huế"),
    ("lang tu duc o da nang dung khong", "Huế"),
    ("com hen la mon da nang phai khong", "Huế"),
    ("chua linh ung o hue phai khong", "Đà Nẵng"),
    ("mi quang la mon hue dung khong", "Đà Nẵng"),
]

# CHỦ ĐỀ vs GIẢ ĐỊNH: (câu hỏi, chủ đề mong đợi). "" = câu không có cấu trúc
# chủ đề/giả định, hệ PHẢI không thu hẹp.
#
# Nhóm này đo phép tách trong `subject_and_claims` cùng với hệ quả của nó: context
# phải khác rỗng. Đo `subject` chứ không đo tên bài được chọn, vì với câu so sánh
# thì bài nào trong hai bài cũng hợp lệ - còn `subject` thì có đúng một đáp án.
#
# Ba câu giữa KHÔNG phải câu kiểm chứng: cấu trúc "X ở Y" xuất hiện ở mọi loại câu
# hỏi, nên phép tách phải đúng cả khi không có "đúng không".
SUBJECT: list[tuple[str, str]] = [
    ("Lăng Tự Đức ở phường Ngũ Hành Sơn đúng không?", "Lăng Tự Đức"),
    ("Lăng Tự Đức Ở Phường Ngũ Hành Sơn Đúng Không", "Lăng Tự Đức"),
    ("lang tu duc o phuong ngu hanh son dung khong", "Lăng Tự Đức"),
    ("Chùa Thiên Mụ ở Ngũ Hành Sơn đúng không?", "Chùa Thiên Mụ"),
    ("Cầu Rồng ở sông Hương đúng không?", "Cầu Rồng"),
    ("Lăng Khải Định nằm ở làng Non Nước phải không?", "Lăng Khải Định"),
    ("Lăng Minh Mạng gần Lăng Gia Long phải không?", "Lăng Minh Mạng"),
    ("Chùa Linh Ứng ở Ngũ Hành Sơn có gì đặc biệt?", "Chùa Linh Ứng"),
    ("Cầu Trường Tiền trên sông Hương dài bao nhiêu?", "Cầu Trường Tiền"),
    # Câu SO SÁNH: hai tên NGANG HÀNG, không tên nào nằm trong giả định. Phép tách
    # phải nhận ra và KHÔNG thu hẹp - chọn bừa một cái làm chủ đề rồi đòi bằng
    # chứng về nó sẽ ném sạch context của một câu hỏi hoàn toàn hợp lệ.
    ("Lăng Tự Đức và Lăng Khải Định khác nhau thế nào?", ""),
    ("So sánh Mì Quảng và Cao lầu", ""),
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

# QUAN HỆ CẤP HÀNH CHÍNH: (câu hỏi, tập bài mà câu trả lời có thể nằm trong).
#
# Đây là nhóm đo THẲNG vào giá trị của lớp graph. BM25 không có khái niệm "phường
# này chứa những di sản nào" - quan hệ đó chỉ tồn tại dưới dạng edge doc <-> ward
# trong kg.py, và trước khi ADMIN_CLASSIFIERS được miễn ngưỡng tần suất thì chỉ
# 6/45 cặp (phường, bài) có thật thành được edge, nên "di sản nào ở phường Long
# Hồ" không neo được và cổng anchor ném sạch một câu hỏi hoàn toàn hợp lệ.
#
# Tập bài chứ không phải một bài: "phường Thủy Xuân" thật sự có 4 di sản, xếp cái
# nào lên đầu cũng đúng. Cái phải đo là "có trả lời không" và "trả lời có nằm trong
# phường được hỏi không".
WARD: list[tuple[str, set[str]]] = [
    ("lăng nào ở phường Thủy Xuân?",
     {"Lăng Tự Đức", "Lăng Khải Định", "Lăng Đồng Khánh", "Chùa Từ Hiếu"}),
    ("phường Thủy Xuân có di tích gì?",
     {"Lăng Tự Đức", "Lăng Khải Định", "Lăng Đồng Khánh", "Chùa Từ Hiếu"}),
    ("di sản nào ở phường Long Hồ?", {"Lăng Minh Mạng", "Điện Hòn Chén"}),
    ("phường Hòa Hải có gì?", {"Ngũ Hành Sơn", "Làng Non Nước"}),
    ("phường Sơn Trà có danh thắng nào?", {"Bán đảo Sơn Trà"}),
    ("phường Thủy Biều có gì?", {"Hổ Quyền"}),
    ("quận Sơn Trà có chùa nào?", {"Chùa Linh Ứng", "Bán đảo Sơn Trà", "Sông Hàn"}),
    ("phường Đông Ba có gì?", {"Chợ Đông Ba", "Kinh thành Huế"}),
    # Chiều NGƯỢC LẠI: hỏi di sản thuộc phường nào. Bằng chứng nằm ở chunk nêu
    # phường, KHÔNG phải đoạn mở đầu - bài Thành Điện Hải mở đầu bằng "thành phố Đà
    # Nẵng" còn "phường Thạch Thang" ở chunk #1 và #7. Xem `_ensure_ward` (rag.py).
    ("Thành Điện Hải thuộc phường nào?", {"Thành Điện Hải"}),
    ("Lăng Tự Đức ở phường nào?", {"Lăng Tự Đức"}),
    ("Chùa Từ Hiếu thuộc phường nào?", {"Chùa Từ Hiếu"}),
    ("Cầu Trường Tiền ở phường nào?", {"Cầu Trường Tiền"}),
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

    print("\n== CHỦ ĐỀ (câu nêu 2 tên riêng - phải hỏi về CHỦ ĐỀ, không về GIẢ ĐỊNH) ==")
    subjected = 0
    for q, want in SUBJECT:
        res = r.retrieve(q, top_k=3)
        ctx, _ = retrieve_context(q)
        # Tách sai chủ đề thì cổng REQUIRE_SUBJECT_EVIDENCE ném context - context
        # rỗng ở đây là hỏng, không phải từ chối đúng.
        ok = res["subject"] == want and bool(ctx)
        subjected += ok
        top = res["hits"][0]["doc"] if res["hits"] else "-"
        print(f"  {'OK  ' if ok else 'MISS'} ctx={len(ctx):5d} subject={res['subject'] or '-':18s} "
              f"| {q[:40]:40s} -> {top}")

    print("\n== PHƯỜNG/XÃ (quan hệ chỉ graph biết - BM25 không có khái niệm này) ==")
    warded = 0
    for q, gold in WARD:
        res = r.retrieve(q, top_k=3)
        ctx, _ = retrieve_context(q)
        top = res["hits"][0]["doc"] if res["hits"] else ""
        # Cả HAI điều kiện: bài đúng phường VÀ context khác rỗng. Chỉ đo bài thì
        # không thấy cổng anchor đang ném; chỉ đo context thì không thấy chọn sai bài.
        ok = top in gold and bool(ctx)
        warded += ok
        print(f"  {'OK  ' if ok else 'MISS'} ctx={len(ctx):5d} | {q[:34]:34s} -> "
              f"{[h['doc'] for h in res['hits']][:3]}")

    n_in, n_out = len(IN_DOMAIN), len(OUT_OF_DOMAIN)
    n_ev, n_sc, n_sb, n_wd = len(EVIDENCE), len(SCOPE), len(SUBJECT), len(WARD)
    print(f"\nrecall@1 = {top1}/{n_in}   recall@3 = {top3}/{n_in}   "
          f"từ chối đúng = {refused}/{n_out}   bằng chứng = {evidenced}/{n_ev}")
    print(f"scope = {scoped}/{n_sc}   chủ đề = {subjected}/{n_sb}   "
          f"phường/xã = {warded}/{n_wd}")
    return 0 if (top1 == n_in and refused == n_out and evidenced == n_ev
                 and scoped == n_sc and subjected == n_sb and warded == n_wd) else 1


if __name__ == "__main__":
    raise SystemExit(main())
