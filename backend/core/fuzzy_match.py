"""Fuzzy matching cho địa danh - suggest correction khi user gõ sai tén.

Tích hợp vào retrieval pipeline: khi find_seeds() trả rỗng, dùng fuzzy match
trên word n-grams để tìm địa danh gần nhất trong knowledge graph thay vì để
REQUIRE_GRAPH_ANCHOR ném sạch kết quả.

Không phụ thuộc extract_names() vì regex đó yêu cầu chữ hoa đầu tên riêng,
mà user thường gõ thường toàn tập ("lăng an định" thay vì "Lăng An Định").
"""
from __future__ import annotations

import difflib
import re
from functools import lru_cache

from backend.core.textutil import strip_accents, word_tokens, STOPWORDS, WORD_RE, nfc


@lru_cache(maxsize=1)
def _build_name_index(graph) -> tuple[list[str], list[str]]:
    """Xây index từ graph: (accented_names, stripped_names)."""
    names: list[str] = []
    for node, data in graph.nodes(data=True):
        kind = data.get("kind")
        if kind not in ("entity", "doc"):
            continue
        label = data["label"]
        names.append(label)
        for alias in data.get("aliases", ()):
            if len(alias) >= 4:
                names.append(alias)

    stripped = [strip_accents(n) for n in names]
    return names, stripped


def _fuzzy_score(a: str, b: str) -> float:
    """Điểm tương đồng 0..1, kết hợp char-level và word-level."""
    char_ratio = difflib.SequenceMatcher(None, a, b).ratio()
    a_words, b_words = set(a.split()), set(b.split())
    if a_words and b_words:
        word_overlap = len(a_words & b_words) / max(len(a_words), len(b_words))
    else:
        word_overlap = 0.0
    return 0.5 * char_ratio + 0.5 * word_overlap


def _find_ngram_in_query(query: str, gram_stripped: str) -> tuple[int, int] | None:
    """Tìm vị trí (start, end) của n-gram trong query gốc."""
    q_tokens_raw = WORD_RE.findall(nfc(query).lower())
    q_tokens_stripped = [strip_accents(t) for t in q_tokens_raw]
    gram_tokens = gram_stripped.split()
    n = len(gram_tokens)

    token_spans = [(m.start(), m.end()) for m in re.finditer(r'\S+', query)]
    if len(token_spans) != len(q_tokens_raw):
        return None

    for i in range(len(q_tokens_stripped) - n + 1):
        if q_tokens_stripped[i : i + n] == gram_tokens:
            start = token_spans[i][0]
            end = token_spans[i + n - 1][1]
            return (start, end)
    return None


def suggest_corrections(
    query: str,
    graph,
    max_suggestions: int = 3,
    cutoff: float = 0.5,
) -> list[dict]:
    """Tìm địa danh gần nhất cho tên riêng sai trong câu hỏi.

    Sinh word n-grams từ query rồi fuzzy match với tên địa danh đã bỏ dấu.
    Trả về [{"original": "lăng an định", "suggested": "Cung An Định", "score": 0.82}].
    `original` là chuỗi trong query gốc (có dấu) để replace trực tiếp.
    """
    accented, stripped = _build_name_index(graph)
    if not accented:
        return []

    q_stripped_tokens = word_tokens(strip_accents(query))
    q_word_set = set(q_stripped_tokens)

    candidates: list[tuple[float, int, str]] = []
    seen: set[tuple[str, str]] = set()

    for size in range(2, min(5, len(q_stripped_tokens) + 1)):
        for i in range(len(q_stripped_tokens) - size + 1):
            gram = " ".join(q_stripped_tokens[i : i + size])
            gram_words = set(gram.split())

            for idx, cand_stripped in enumerate(stripped):
                if not gram_words & set(cand_stripped.split()):
                    continue
                if set(cand_stripped.split()).issubset(q_word_set):
                    continue
                score = _fuzzy_score(gram, cand_stripped)
                if score >= cutoff:
                    key = (gram, accented[idx])
                    if key not in seen:
                        seen.add(key)
                        candidates.append((score, idx, gram))

    candidates.sort(reverse=True, key=lambda x: x[0])
    results: list[dict] = []
    used_suggested: set[str] = set()
    for score, idx, gram in candidates:
        suggested = accented[idx]
        if suggested in used_suggested:
            continue
        used_suggested.add(suggested)
        # Tìm vị trí trong query gốc để replace
        span = _find_ngram_in_query(query, gram)
        if span:
            original = query[span[0] : span[1]]
        else:
            original = gram
        results.append({
            "original": original,
            "suggested": suggested,
            "score": round(score, 2),
        })
        if len(results) >= max_suggestions:
            break

    return results
