"""Retrieval hybrid: BM25 theo từ + BM25 theo n-gram ký tự + mở rộng bằng graph.

Không cần model embedding, không cần tải weight, chạy được offline ngay:
- Nhánh TỪ    : chính xác về chính tả, tốt cho tên riêng có dấu.
- Nhánh N-GRAM: text đã bỏ dấu -> chịu được truy vấn không dấu và sai chính tả.
- GRAPH       : xếp lại theo quan hệ tri thức, cho phép bắc cầu nhiều chặng
                ("triều Nguyễn" -> các lăng) mà từ khoá thuần không làm được.
Hai nhánh lexical hợp nhất bằng RRF, rồi graph cộng thêm điểm - graph XẾP LẠI
chứ không LỌC, nên một chunk đúng vẫn về được kể cả khi graph không biết gì về nó.
"""
from __future__ import annotations

import math
from collections import defaultdict
from functools import lru_cache

import networkx as nx

from backend.core.corpus import load_docs
from backend.core.kg import build_graph, expand_docs, find_seeds
from backend.core.textutil import contains_name, ngram_tokens, strip_accents, word_tokens

HEADING_WEIGHT = 3      # tiêu đề mục là tín hiệu chủ đề mạnh nhất của wiki tiếng Việt
RRF_K = 60
GRAPH_WEIGHT = 0.35
NAMED_DOC_BONUS = 0.8   # câu hỏi gọi ĐÚNG TÊN bài: mạnh hơn mọi khớp từ khoá mờ
CHUNK_ENTITY_BONUS = 0.15
CANDIDATES = 30
INJECT_PER_DOC = 3

# Kind của seed được coi là "câu hỏi có neo vào miền tri thức này".
# year KHÔNG tính: "ai sinh năm 1990" có year node nhưng không thuộc corpus.
ANCHOR_KINDS = frozenset({"entity", "doc", "region", "category"})


class Bm25:
    """BM25 trên inverted index. Tokenizer truyền vào nên dùng lại được cho n-gram."""

    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.n = len(docs)
        self.doc_len = [len(d) for d in docs]
        self.avgdl = (sum(self.doc_len) / self.n) if self.n else 0.0
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for i, toks in enumerate(docs):
            tf: dict[str, int] = defaultdict(int)
            for t in toks:
                tf[t] += 1
            for t, c in tf.items():
                self.postings[t].append((i, c))
        self.idf = {
            t: math.log(1.0 + (self.n - len(p) + 0.5) / (len(p) + 0.5))
            for t, p in self.postings.items()
        }

    def search(self, q_tokens: list[str]) -> dict[int, float]:
        scores: dict[int, float] = defaultdict(float)
        for t in set(q_tokens):
            postings = self.postings.get(t)
            if not postings:
                continue
            idf = self.idf[t]
            for i, tf in postings:
                norm = 1.0 - self.b + self.b * (self.doc_len[i] / (self.avgdl or 1.0))
                scores[i] += idf * tf * (self.k1 + 1.0) / (tf + self.k1 * norm)
        return scores


def _rrf(*rankings: dict[int, float]) -> dict[int, float]:
    """Reciprocal Rank Fusion - hợp nhất theo THỨ HẠNG nên không cần scale điểm."""
    fused: dict[int, float] = defaultdict(float)
    for scores in rankings:
        for rank, (i, _) in enumerate(sorted(scores.items(), key=lambda kv: -kv[1])):
            fused[i] += 1.0 / (RRF_K + rank + 1)
    return fused


class Retriever:
    def __init__(self, docs: list[dict], graph: nx.Graph):
        self.graph = graph
        self.chunks: list[dict] = []
        self.doc_index: dict[str, list[int]] = defaultdict(list)
        for doc in docs:
            for i, ch in enumerate(doc["chunks"]):
                self.doc_index[f"doc:{doc['name']}"].append(len(self.chunks))
                self.chunks.append({
                    "doc": doc["name"], "doc_node": f"doc:{doc['name']}",
                    "chunk_id": f"{doc['name']}#{i}",
                    "heading": ch["heading"], "text": ch["text"],
                    "url": doc["url"], "region": doc["region"], "category": doc["category"],
                })
        indexed = [((c["heading"] + " ") * HEADING_WEIGHT + c["text"]) for c in self.chunks]
        self.plain = [strip_accents(t) for t in indexed]
        # So khớp phủ trên bản BỎ DẤU: nếu so bằng token có dấu thì truy vấn không
        # dấu luôn ra coverage 0 và bị coi là "không liên quan" oan.
        self.plain_words = [set(word_tokens(p)) for p in self.plain]
        n = max(len(self.plain_words), 1)
        df: dict[str, int] = defaultdict(int)
        for words in self.plain_words:
            for t in words:
                df[t] += 1
        # IDF riêng cho coverage. Token KHÔNG có trong corpus nhận idf lớn nhất:
        # "bitcoin" vắng mặt phải kéo coverage xuống mạnh, còn "bao/nay/nhieu"
        # khớp được với bài tiếng Việt nào cũng được thì gần như không tính điểm.
        self.cover_idf = {t: math.log(1.0 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}
        self.max_idf = math.log(1.0 + (n + 0.5) / 0.5)
        self.word = Bm25([word_tokens(t) for t in indexed])
        self.ngram = Bm25([ngram_tokens(t) for t in indexed], k1=1.2, b=0.6)

    def _coverage(self, q_words: set[str], i: int) -> float:
        """Tỉ lệ TRỌNG SỐ IDF của từ khoá câu hỏi có mặt trong chunk."""
        if not q_words:
            return 0.0
        total = sum(self.cover_idf.get(t, self.max_idf) for t in q_words)
        if total <= 0:
            return 0.0
        hit = sum(
            self.cover_idf.get(t, self.max_idf)
            for t in q_words & self.plain_words[i]
        )
        return hit / total

    def _named_docs(self, seeds: list[str]) -> set[str]:
        """Bài mà câu hỏi gọi đúng tên - trực tiếp, hoặc qua entity curated cùng tên."""
        out: set[str] = set()
        for s in seeds:
            kind = self.graph.nodes[s].get("kind")
            if kind == "doc":
                out.add(s)
            elif kind == "entity":
                dn = "doc:" + self.graph.nodes[s]["label"]
                if dn in self.graph:
                    out.add(dn)
        return out

    def retrieve(self, query: str, top_k: int = 3) -> dict:
        """Trả về {hits, seeds, specific, named, anchored}.

        `anchored`  = câu hỏi có neo vào miền tri thức này.
        `specific`  = tên riêng cụ thể mà câu hỏi gọi (entity/doc, không phải hub).
                      `rag.py` dùng nó để đòi BẰNG CHỨNG: hỏi đúng tên một di sản
                      mà chunk tốt nhất không hề nhắc tên đó thì hệ chưa có tư liệu.
        """
        empty: dict = {"hits": [], "seeds": [], "specific": [], "named": [], "anchored": False}
        if not query.strip():
            return empty

        lexical = _rrf(
            self.word.search(word_tokens(query)),
            self.ngram.search(ngram_tokens(query)),
        )
        seeds = find_seeds(self.graph, query)
        named = self._named_docs(seeds)
        anchored = any(self.graph.nodes[s].get("kind") in ANCHOR_KINDS for s in seeds)
        if not lexical and not named:
            return empty

        cand = {i for i, _ in sorted(lexical.items(), key=lambda kv: -kv[1])[:CANDIDATES]}
        # GRAPH LÀM TĂNG RECALL, không chỉ xếp lại thứ tự: chunk của bài được gọi
        # đúng tên phải vào pool dù điểm lexical thấp. Truy vấn ngắn không dấu
        # ("cao lau la mon gi") sinh ra nhiều n-gram phổ biến làm loãng tín hiệu,
        # bài đúng rơi khỏi top-30 và rerank thuần không thể cứu được nữa.
        for dn in named:
            ranked = sorted(self.doc_index.get(dn, []), key=lambda i: -lexical.get(i, 0.0))
            cand.update(ranked[:INJECT_PER_DOC])
        best = max((lexical.get(i, 0.0) for i in cand), default=0.0) or 1.0

        doc_scores = expand_docs(self.graph, seeds)
        seed_labels = [
            self.graph.nodes[s]["label"] for s in seeds
            if self.graph.nodes[s].get("kind") in ("entity", "doc")
        ]
        q_words = set(word_tokens(strip_accents(query)))

        out: list[dict] = []
        for i in cand:
            c = self.chunks[i]
            lex = lexical.get(i, 0.0) / best
            g = doc_scores.get(c["doc_node"], 0.0)
            hits = [lb for lb in seed_labels if contains_name(self.plain[i], lb)]
            score = (lex + GRAPH_WEIGHT * g + CHUNK_ENTITY_BONUS * min(len(hits), 3)
                     + (NAMED_DOC_BONUS if c["doc_node"] in named else 0.0))
            out.append({**c, "score": round(score, 4), "lexical": round(lex, 4),
                        "graph": round(g, 4), "graph_hits": hits,
                        "named": c["doc_node"] in named,
                        "coverage": round(self._coverage(q_words, i), 3)})
        out.sort(key=lambda r: -r["score"])
        return {
            "hits": out[:top_k],
            "seeds": [self.graph.nodes[s]["label"] for s in seeds],
            "specific": seed_labels,
            "named": sorted(self.graph.nodes[n]["label"] for n in named),
            "anchored": anchored,
        }

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        return self.retrieve(query, top_k)["hits"]


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    """Dựng index + graph 1 lần. Corpus nhỏ nên build trong RAM nhanh hơn là
    đọc lại artifact từ đĩa, và không bao giờ lệch với corpus hiện tại."""
    docs, _skipped = load_docs()
    return Retriever(docs, build_graph(docs))
