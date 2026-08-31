"""Core RAG module - GraphRAG retrieval (hybrid lexical + knowledge graph).

Trả về context ĐÚNG HÌNH DẠNG mà LoRA được train: một đoạn văn liền mạch, vì
mỗi mẫu train có `Nguồn:` là nội dung của MỘT chunk. Nối nhiều chunk bằng dấu
phân cách lạ là tạo ra định dạng model chưa từng thấy.

Khi không tìm được đoạn đủ liên quan thì trả về context RỖNG - `llm.py` sẽ ghi
"Nguồn: (không có)", đúng dạng các mẫu refusal đã train, nên model từ chối lịch
sự thay vì bịa. Đây là hành vi mong muốn, không phải lỗi.
"""
from __future__ import annotations

from backend.core.retriever import get_retriever

# CỔNG TỪ CHỐI. Đo trên 12 câu trong phạm vi / 8 câu ngoài phạm vi:
#   - coverage (tỉ lệ từ khoá khớp) KHÔNG phân tách được: trong 0.36-0.80,
#     ngoài 0.19-1.00. Tiếng Việt hư từ nào cũng có mặt trong corpus wiki nào.
#   - "câu hỏi có neo vào graph" (nhắc tên một entity/bài/vùng/loại mà KG biết)
#     phân tách 12/12 vs 0/8.
# Đây chính là chỗ graph trả giá trị rõ nhất: nó là thứ duy nhất biết câu hỏi có
# thuộc miền tri thức này hay không. Không neo được -> để model từ chối lịch sự.
REQUIRE_GRAPH_ANCHOR = True
MIN_COVERAGE = 0.25   # chốt phụ; câu trong phạm vi thấp nhất đo được là 0.36

# CỔNG BẰNG CHỨNG. Graph có 49 địa điểm curated nhưng chỉ 23 bài crawl được, nên
# một câu hỏi có thể neo ĐÚNG miền tri thức mà hệ vẫn KHÔNG có tư liệu về nó
# ("Đàn Nam Giao thờ ai?" - node có, bài không). Khi đó retrieval vẫn trả về
# chunk điểm cao nhất của bài khác và model trả lời rất tự tin về một di sản
# hoàn toàn khác - sai tệ hơn là từ chối. Vì vậy: câu hỏi gọi đúng tên riêng nào
# thì chunk được chọn phải thuộc bài đó hoặc phải nhắc tên đó.
REQUIRE_EVIDENCE_FOR_NAMED = True

# Ngữ cảnh dài hơn mẫu train nhiều thì model bắt đầu lạc; 2 chunk là đủ.
CONTEXT_MAX_CHARS = 2200
MAX_CONTEXT_CHUNKS = 2

# Chỉ lấy chunk của doc thứ hai khi nó gần bằng doc tốt nhất (câu hỏi so sánh).
SECOND_DOC_RATIO = 0.75

SNIPPET_CHARS = 240


def _snippet(text: str) -> str:
    if len(text) <= SNIPPET_CHARS:
        return text
    cut = text.rfind(" ", 0, SNIPPET_CHARS)
    return text[: cut if cut > 0 else SNIPPET_CHARS].rstrip(" ,;:") + " ..."


def retrieve_context(query: str, top_k: int = 3) -> tuple[str, list[dict]]:
    """Trả về (context_text, list_of_source_dicts).

    Source dict: {text, score, doc, heading, url, chunk_id, graph, graph_hits}
    """
    res = get_retriever().retrieve(query, top_k=top_k)
    hits = res["hits"]
    if not hits:
        return ("", [])
    if REQUIRE_GRAPH_ANCHOR and not res["anchored"]:
        return ("", [])
    if hits[0]["coverage"] < MIN_COVERAGE:
        return ("", [])
    if REQUIRE_EVIDENCE_FOR_NAMED and res["specific"]:
        top = hits[0]
        if not top["named"] and not top["graph_hits"]:
            return ("", [])

    top_doc, top_score = hits[0]["doc"], hits[0]["score"]
    picked: list[dict] = []
    total = 0
    for h in hits:
        if h["doc"] != top_doc and h["score"] < SECOND_DOC_RATIO * top_score:
            continue
        if total + len(h["text"]) > CONTEXT_MAX_CHARS and picked:
            break
        picked.append(h)
        total += len(h["text"])
        if len(picked) >= MAX_CONTEXT_CHUNKS:
            break

    # Giữ thứ tự chunk trong bài để đoạn văn đọc liền mạch, không nhảy ngược
    picked.sort(key=lambda h: (h["doc"] != top_doc, h["chunk_id"]))
    context = " ".join(h["text"] for h in picked)

    sources = [
        {
            "text": _snippet(h["text"]),
            "score": h["score"],
            "doc": h["doc"],
            "heading": h["heading"],
            "url": h["url"],
            "chunk_id": h["chunk_id"],
            "graph": h["graph"],
            "graph_hits": h["graph_hits"],
            "used_in_context": any(p["chunk_id"] == h["chunk_id"] for p in picked),
        }
        for h in hits
    ]
    return (context, sources)
