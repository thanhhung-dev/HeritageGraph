"""Core RAG module - GraphRAG retrieval.

TODO: tích hợp thật với graphrag sau khi indexing xong.
Hiện tại: trả về context rỗng, để backend chạy được smoke test.
"""
from __future__ import annotations


def retrieve_context(query: str, top_k: int = 3) -> tuple[str, list[dict]]:
    """Trả về (context_text, list_of_source_dicts).

    Source dict format: {"text": "...", "score": 0.92, "entity": "..."}
    """
    # TODO: gọi graphrag query
    # Hiện tại trả về context mẫu để test pipeline
    return ("", [])
