"""Retrieval hybrid: BM25 theo từ + BM25 theo n-gram ký tự + mở rộng bằng graph.

Không cần model embedding, không cần tải weight, chạy được offline ngay:
- Nhánh TỪ    : chính xác về chính tả, tốt cho tên riêng có dấu.
- Nhánh N-GRAM: text đã bỏ dấu -> chịu được truy vấn không dấu và sai chính tả.
- GRAPH       : xếp lại theo quan hệ tri thức, cho phép bắc cầu nhiều chặng
                ("triều Nguyễn" -> các lăng) mà từ khoá thuần không làm được.
Hai nhánh lexical hợp nhất bằng RRF, rồi graph cộng thêm điểm - graph XẾP LẠI
chứ không LỌC, nên một chunk đúng vẫn về được kể cả khi graph không biết gì về nó.

XẾP HẠNG HAI TẦNG. Chọn BÀI và chọn CHUNK TRONG BÀI là hai việc khác nhau:
- `score`       gồm cả tín hiệu cấp bài (NAMED_DOC_BONUS, graph) -> chọn bài.
- `chunk_score` chỉ gồm tín hiệu đến từ CÂU HỎI -> chọn chunk trong bài.
Trước khi tách, NAMED_DOC_BONUS là hằng số cộng cho MỌI chunk của bài đúng tên
nên 3 chunk đầu của "Chùa Thiên Mụ" chênh nhau 1% (2.1075/2.0996/2.0765) - thứ
tự trong bài do nhiễu lexical quyết định. Chunk chứa "cách trung tâm thành phố
Huế khoảng 5 km" xếp hạng 3 và bị MAX_CONTEXT_CHUNKS=2 của rag.py cắt, nên model
không có bằng chứng để bác câu hỏi sai tiền đề "Chùa Thiên Mụ ở Đà Nẵng à?".
"""
from __future__ import annotations

import math
import re
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

# --- Ý ĐỊNH CÂU HỎI ----------------------------------------------------------
# Khớp trên text ĐÃ BỎ DẤU (strip_accents) nên câu gõ không dấu cũng nhận ra.
# Chỉ 3 loại, đều là loại mà chunk chứa câu trả lời có DẤU HIỆU HÌNH THỨC rõ:
# vị trí -> nằm ở mục "Vị trí"/"Địa lý" hoặc đoạn mở đầu; thời gian -> chunk có
# chứa số năm. Đoán ý định phức tạp hơn thì bắt đầu sai nhiều hơn đúng.
LOCATION_RE = re.compile(
    r"\b(o dau|nam o|toa lac|thuoc tinh|thuoc thanh pho|thuoc dia phan|dia chi"
    r"|vi tri|o tinh|o thanh pho|cach trung tam|o mien|o khu vuc)\b"
)
TIME_RE = re.compile(
    r"\b(nam nao|khi nao|bao gio|tu nam|vao nam|nam bao nhieu|the ky nao"
    r"|thoi gian nao|nam may)\b"
)
# Câu KIỂM CHỨNG: chứa một giả định cần xác nhận hoặc bác bỏ.
VERIFY_RE = re.compile(
    r"\b(dung khong|phai khong|co phai|co dung|dung chu|that khong|phai la)\b"
)

# Mục wiki hay chứa câu trả lời về vị trí. So khớp trên heading đã bỏ dấu.
LOCATION_HEADINGS = ("vi tri", "dia ly", "dia diem", "kien tao")

INTENT_HEADING_BONUS = 0.45   # đủ để vượt chênh lệch nhiễu lexical (~0.03) trong cùng bài
YEAR_IN_CHUNK_RE = re.compile(r"(?<!\d)(1[0-9]{3}|20[0-2][0-9])(?!\d)")

# --- SCOPE: thu hẹp phạm vi tìm kiếm ------------------------------------------
# region/category đã có sẵn trên từng chunk và đã là hub node trong KG, nhưng
# HUB_FACTOR=0.25 (kg.py) CỐ TÌNH hạ ảnh hưởng của hub để "hỏi gì về Huế" không
# kéo về cả 18 bài Huế - và expand_docs chỉ XẾP LẠI, chưa bao giờ LỌC. Nên câu
# "Huế có món ăn đặc sản nào" đo được trả về Cao lầu + Mì Quảng (đều Đà Nẵng).
# Ở đây lọc THẬT: giới hạn pool trước khi tính điểm, tức là tìm SÂU trong phạm
# vi hẹp thay vì tìm nông trên toàn corpus.
#
# Nhãn category trong locations_index.json là danh từ Hán-Việt ("Ẩm thực") còn
# người dùng gõ tiếng thuần ("món ăn"), nên cần bảng đồng nghĩa. Chỉ nhận từ
# khoá ĐẶC TRƯNG cho đúng một category: lọc sai loại bỏ mất bài đúng, tệ hơn là
# không lọc. Vì vậy không có "hát"/"nhạc" (khớp cả Nghệ thuật lẫn Lễ hội).
CATEGORY_SYNONYMS: dict[str, tuple[str, ...]] = {
    "Ẩm thực": ("mon an", "am thuc", "dac san", "mon ngon", "do an", "mon gi", "an gi"),
    "Lễ hội": ("le hoi", "festival"),
    "Nghệ thuật": ("nghe thuat", "loai hinh dien xuong", "nghe thuat bieu dien"),
    "Làng nghề": ("lang nghe", "nghe truyen thong", "thu cong my nghe"),
    "Danh thắng": ("danh thang", "thang canh", "canh dep"),
    "Di tích lịch sử": ("di tich", "di tich lich su"),
}
REGION_SYNONYMS: dict[str, tuple[str, ...]] = {
    "Huế": ("hue", "thua thien hue", "co do hue"),
    "Đà Nẵng": ("da nang", "danang"),
}


def _match_any(plain_query: str, keys: tuple[str, ...]) -> bool:
    return any(re.search(rf"(?<!\w){re.escape(k)}(?!\w)", plain_query) for k in keys)


def query_scope(query: str) -> tuple[str, str]:
    """('Huế', 'Ẩm thực') - chuỗi rỗng nghĩa là KHÔNG giới hạn chiều đó."""
    plain = strip_accents(query)
    region = next((r for r, keys in REGION_SYNONYMS.items() if _match_any(plain, keys)), "")
    category = next((c for c, keys in CATEGORY_SYNONYMS.items() if _match_any(plain, keys)), "")
    return (region, category)


def query_intent(query: str) -> frozenset[str]:
    """{'location'} / {'time'} / {'verify','location'} ... - rỗng nếu không rõ.

    Câu kiểm chứng về di sản gần như luôn kiểm chứng VỊ TRÍ ("X ở Huế đúng
    không"), nên 'verify' kéo theo 'location': bằng chứng cần tìm cùng một chỗ.
    """
    q = strip_accents(query)
    found = set()
    if LOCATION_RE.search(q):
        found.add("location")
    if TIME_RE.search(q):
        found.add("time")
    if VERIFY_RE.search(q):
        found.add("verify")
        found.add("location")
    return frozenset(found)


def is_lead(chunk: dict) -> bool:
    """Đoạn mở đầu bài. Ở corpus wiki nó gần như LUÔN chứa tỉnh/thành."""
    return not chunk["heading"] or chunk["chunk_id"].endswith("#0")


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
        # Index scope: (region, category) -> chỉ số chunk. Dùng để LỌC pool trước
        # khi tính điểm, nên phải dựng sẵn thay vì quét 349 chunk mỗi truy vấn.
        self.by_region: dict[str, list[int]] = defaultdict(list)
        self.by_category: dict[str, list[int]] = defaultdict(list)
        for i, c in enumerate(self.chunks):
            self.by_region[c["region"]].append(i)
            self.by_category[c["category"]].append(i)
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

    def _intent_bonus(self, intent: frozenset[str], chunk: dict) -> float:
        """Điểm cho chunk KHỚP Ý ĐỊNH câu hỏi - tín hiệu cấp CHUNK, không cấp bài."""
        if not intent:
            return 0.0
        bonus = 0.0
        if "location" in intent:
            heading = strip_accents(chunk["heading"])
            if any(h in heading for h in LOCATION_HEADINGS) or is_lead(chunk):
                bonus += INTENT_HEADING_BONUS
        if "time" in intent and YEAR_IN_CHUNK_RE.search(chunk["text"]):
            bonus += INTENT_HEADING_BONUS
        return bonus

    def _scope_pool(self, scope: tuple[str, str]) -> set[int] | None:
        """Chỉ số chunk nằm trong scope; None = không giới hạn.

        Giao hai chiều region x category. Nếu giao lại RỖNG thì trả None chứ
        không trả tập rỗng: "Huế có làng nghề gì" - corpus không có bài nào khớp
        cả hai, lọc cứng sẽ ra tay trắng còn không lọc thì ít nhất còn trả về
        làng nghề Đà Nẵng để model tự nói rõ đó là Đà Nẵng.
        """
        region, category = scope
        pools = []
        if region:
            pools.append(set(self.by_region.get(region, ())))
        if category:
            pools.append(set(self.by_category.get(category, ())))
        if not pools:
            return None
        pool = set.intersection(*pools)
        return pool or None

    def retrieve(self, query: str, top_k: int = 3) -> dict:
        """Trả về {hits, seeds, specific, named, anchored, intent, scope}.

        `anchored`  = câu hỏi có neo vào miền tri thức này.
        `specific`  = tên riêng cụ thể mà câu hỏi gọi (entity/doc, không phải hub).
                      `rag.py` dùng nó để đòi BẰNG CHỨNG: hỏi đúng tên một di sản
                      mà chunk tốt nhất không hề nhắc tên đó thì hệ chưa có tư liệu.
        `intent`    = ý định câu hỏi; `rag.py` dùng để ép kèm chunk mở đầu.
        `scope`     = (region, category) suy từ câu hỏi; "" nghĩa là không giới hạn.

        Mỗi hit có HAI điểm: `score` (cấp bài, để chọn bài) và `chunk_score`
        (chỉ tín hiệu từ câu hỏi, để chọn chunk trong bài). Xem docstring module.
        """
        empty: dict = {"hits": [], "seeds": [], "specific": [], "named": [],
                       "anchored": False, "intent": frozenset(), "scope": ("", "")}
        if not query.strip():
            return empty

        lexical = _rrf(
            self.word.search(word_tokens(query)),
            self.ngram.search(ngram_tokens(query)),
        )
        seeds = find_seeds(self.graph, query)
        named = self._named_docs(seeds)
        anchored = any(self.graph.nodes[s].get("kind") in ANCHOR_KINDS for s in seeds)
        intent = query_intent(query)
        scope = query_scope(query)
        if not lexical and not named:
            return empty

        # LỌC SCOPE - nhưng TÊN RIÊNG THẮNG SCOPE. "Chùa Thiên Mụ ở Đà Nẵng đúng
        # không" có scope region=Đà Nẵng, lọc theo đó sẽ loại đúng bài Chùa Thiên
        # Mụ (thuộc Huế) - chính bài cần để bác lại. Câu gọi đúng tên bài thì bài
        # đó là câu trả lời, không phải phạm vi trong câu hỏi.
        pool = None if named else self._scope_pool(scope)
        if pool is not None:
            lexical = {i: s for i, s in lexical.items() if i in pool}
            if not lexical:
                # Không chunk nào trong scope khớp từ khoá: bỏ lọc, thà xếp hạng
                # rộng còn hơn trả rỗng cho câu hỏi hợp lệ.
                lexical = _rrf(
                    self.word.search(word_tokens(query)),
                    self.ngram.search(ngram_tokens(query)),
                )
                pool = None

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
            intent_bonus = self._intent_bonus(intent, c)
            # TẦNG 2 (chọn chunk): chỉ tín hiệu từ câu hỏi. KHÔNG có NAMED_DOC_BONUS
            # vì nó là hằng số cho cả bài, cộng vào chỉ làm mọi chunk hoà nhau.
            chunk_score = lex + CHUNK_ENTITY_BONUS * min(len(hits), 3) + intent_bonus
            # TẦNG 1 (chọn bài): cộng thêm tín hiệu cấp bài.
            score = (chunk_score + GRAPH_WEIGHT * g
                     + (NAMED_DOC_BONUS if c["doc_node"] in named else 0.0))
            out.append({**c, "score": round(score, 4),
                        "chunk_score": round(chunk_score, 4),
                        "lexical": round(lex, 4),
                        "graph": round(g, 4), "graph_hits": hits,
                        "named": c["doc_node"] in named,
                        "intent_bonus": round(intent_bonus, 4),
                        "coverage": round(self._coverage(q_words, i), 3)})

        # Sắp theo TẦNG 1 để chọn bài, rồi trong cùng bài sắp lại theo TẦNG 2.
        # Hai lần sort thay vì một: bài tốt nhất vẫn thắng, nhưng thứ tự chunk bên
        # trong bài được quyết định bởi câu hỏi chứ không bởi hằng số cấp bài.
        out.sort(key=lambda r: -r["score"])
        if out:
            top_doc = out[0]["doc_node"]
            out.sort(key=lambda r: (r["doc_node"] != top_doc, -r["chunk_score"]))

        return {
            "hits": out[:top_k],
            "seeds": [self.graph.nodes[s]["label"] for s in seeds],
            "specific": seed_labels,
            "named": sorted(self.graph.nodes[n]["label"] for n in named),
            "anchored": anchored,
            "intent": intent,
            "scope": scope,
        }

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        return self.retrieve(query, top_k)["hits"]


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    """Dựng index + graph 1 lần. Corpus nhỏ nên build trong RAM nhanh hơn là
    đọc lại artifact từ đĩa, và không bao giờ lệch với corpus hiện tại."""
    docs, _skipped = load_docs()
    return Retriever(docs, build_graph(docs))
