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
from backend.core.kg import build_graph, expand_docs, extract_names, find_seeds, is_admin_name
from backend.core.textutil import (
    contains_name,
    name_span,
    ngram_tokens,
    strip_accents,
    word_tokens,
)

HEADING_WEIGHT = 3      # tiêu đề mục là tín hiệu chủ đề mạnh nhất của wiki tiếng Việt
RRF_K = 60
GRAPH_WEIGHT = 0.35
NAMED_DOC_BONUS = 0.8   # câu hỏi gọi ĐÚNG TÊN bài: mạnh hơn mọi khớp từ khoá mờ
CHUNK_ENTITY_BONUS = 0.15
CANDIDATES = 30
# 5, không phải 3: truy vấn KHÔNG DẤU sinh nhiều n-gram phổ biến làm loãng tín hiệu
# nên đoạn mở đầu tụt hạng trong bài. "lang khai dinh o da nang dung khong" xếp
# chunk #0 (nơi duy nhất ghi "thành phố Huế") ở hạng 4 theo lexical, nên nó không
# được bơm vào pool và `_ensure_lead` của rag.py không tìm thấy nó trong hits -
# model nhận context không có chữ "Huế" nào và xác nhận một tiền đề sai. Đo trên
# 45 bài: câu không dấu mất bằng chứng vùng ở 7 bài, câu có dấu ở 4 bài.
INJECT_PER_DOC = 5

ANCHOR_KINDS = frozenset({"entity", "doc", "region", "category"})


LOCATION_RE = re.compile(
    r"\b(o dau|nam o|toa lac|thuoc tinh|thuoc thanh pho|thuoc dia phan|dia chi"
    r"|vi tri|o tinh|o thanh pho|cach trung tam|o mien|o khu vuc"
    r"|o phuong|o quan|o xa|o huyen|o lang|o thi xa"
    r"|thuoc phuong|thuoc quan|thuoc xa|thuoc huyen|thuoc lang)\b"
)
TIME_RE = re.compile(
    r"\b(nam nao|khi nao|bao gio|tu nam|vao nam|nam bao nhieu|the ky nao"
    r"|thoi gian nao|nam may)\b"
)

WARD_RE = re.compile(
    r"\b(phuong|quan|xa|huyen|thi xa|thi tran|lang|thon)\s+(nao|gi|may)\b"
    r"|\b(o|tai|thuoc)\s+(phuong|quan|xa|huyen|thi xa|thi tran|lang|thon)\b"
)
VERIFY_RE = re.compile(
    r"\b(dung khong|phai khong|co phai|co dung|dung chu|that khong|phai la)\b"
)

CLAIM_PREFIX_RE = re.compile(
    r"\b(o|tai|thuoc|cua|gan|tren|ben|canh|trong)\s+"
    r"(?:(?:phuong|quan|xa|huyen|tinh|thanh pho|tp|thi xa|thi tran|lang|tong"
    r"|khu|khu vuc|mien|vung|dia phan|dia ban|to dan pho|bo|bo song)\s+)*$"
)

LOCATION_HEADINGS = ("vi tri", "dia ly", "dia diem", "kien tao")

INTENT_HEADING_BONUS = 0.45   # đủ để vượt chênh lệch nhiễu lexical (~0.03) trong cùng bài
YEAR_IN_CHUNK_RE = re.compile(r"(?<!\d)(1[0-9]{3}|20[0-2][0-9])(?!\d)")


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
    """{'location'} / {'time'} / {'ward','verify','location'} ... - rỗng nếu không rõ.

    Câu kiểm chứng về di sản gần như luôn kiểm chứng VỊ TRÍ ("X ở Huế đúng
    không"), nên 'verify' kéo theo 'location': bằng chứng cần tìm cùng một chỗ.

    'ward' cũng kéo theo 'location' - nó hẹp hơn, không khác loại - nhưng `rag.py`
    xử lý riêng: xem WARD_RE và `_ensure_ward`.
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
    if WARD_RE.search(q):
        found.add("ward")
        found.add("location")
    return frozenset(found)


def is_lead(chunk: dict) -> bool:
    """Đoạn mở đầu bài. Ở corpus wiki nó gần như LUÔN chứa tỉnh/thành."""
    return not chunk["heading"] or chunk["chunk_id"].endswith("#0")


def is_admin_chunk(chunk: dict) -> bool:
    """Chunk có nêu đơn vị hành chính cấp phường/xã ('phường Thạch Thang').

    Khác `is_lead`: chỉ 18/45 bài nêu phường trong đoạn mở đầu, số còn lại nêu ở
    giữa bài hoặc không nêu. Dùng để chọn chunk cho câu hỏi cấp phường - xem
    `_ensure_ward` trong rag.py.
    """
    return any(is_admin_name(n) for n in extract_names(chunk["text"]))


def subject_and_claims(query: str, names: list[str]) -> tuple[str, list[str]]:
    """Tách tên riêng trong câu hỏi thành (CHỦ ĐỀ, các tên chỉ nằm trong GIẢ ĐỊNH).

    Chủ đề = tên riêng đầu tiên KHÔNG đứng sau giới từ định vị. Câu hỏi tiếng Việt
    đặt chủ đề trước vị ngữ, nên tên bị "ở/tại/thuộc/của/gần" dẫn vào là phần cần
    kiểm chứng, không phải thứ đang được hỏi.

    Trả ("", []) khi KHÔNG có tên nào nằm trong vị ngữ - tức là câu không có cấu
    trúc chủ đề/giả định để tách. Câu so sánh ("Lăng Tự Đức và Lăng Khải Định khác
    nhau thế nào") thuộc nhóm này: hai tên NGANG HÀNG, chọn một cái làm chủ đề rồi
    đòi bằng chứng về nó sẽ ném sạch context của một câu hỏi hoàn toàn hợp lệ.
    """
    if len(names) < 2:
        return ("", [])
    plain = strip_accents(query)
    spans: list[tuple[int, str, bool]] = []
    for name in names:
        span = name_span(plain, name)
        if span is None:
            continue
        spans.append((span[0], name, bool(CLAIM_PREFIX_RE.search(plain[: span[0]]))))
    spans.sort()
    claims = [n for _, n, in_claim in spans if in_claim]
    subject = next((n for _, n, in_claim in spans if not in_claim), "")
    if not subject or not claims:
        return ("", [])
    return (subject, [n for n in claims if n != subject])


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
        self.by_region: dict[str, list[int]] = defaultdict(list)
        self.by_category: dict[str, list[int]] = defaultdict(list)
        for i, c in enumerate(self.chunks):
            self.by_region[c["region"]].append(i)
            self.by_category[c["category"]].append(i)
        self.plain_words = [set(word_tokens(p)) for p in self.plain]
        n = max(len(self.plain_words), 1)
        df: dict[str, int] = defaultdict(int)
        for words in self.plain_words:
            for t in words:
                df[t] += 1
        self.cover_idf = {t: math.log(1.0 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}
        self.max_idf = math.log(1.0 + (n + 0.5) / 0.5)
        self.word = Bm25([word_tokens(t) for t in indexed])
        self.ngram = Bm25([ngram_tokens(t) for t in indexed], k1=1.2, b=0.6)
        self.admin_labels = {
            strip_accents(d["label"]) for _, d in graph.nodes(data=True)
            if is_admin_name(d.get("label", ""))
        }

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

    def foreign_admin(self, query: str) -> list[str]:
        """Địa danh hành chính trong câu hỏi mà corpus KHÔNG hề nhắc tới.

        "phường Hoàn Kiếm có danh thắng nào" nêu một phường Hà Nội. Cổng
        REQUIRE_GRAPH_ANCHOR không chặn được vì câu vẫn neo qua từ "danh thắng"
        (hub category), nên retrieval trả về Ngũ Hành Sơn và model kể về Đà Nẵng
        như thể đó là câu trả lời. Đây là bẫy mà việc thêm node phường tạo ra:
        thêm 67 địa danh vào KG cũng là thêm 67 cách để câu ngoài vùng trông giống
        câu trong vùng.

        Chỉ nhận danh từ loại HÀNH CHÍNH: chúng có tập giá trị đóng trong corpus
        (67 địa danh), nên "không có trong KG" nghĩa là "corpus chắc chắn không nói
        về nơi này". Với danh từ loại khác thì suy luận đó sai - "chùa Bái Đính"
        vắng mặt có thể chỉ vì regex trượt.
        """
        return [
            name for name in extract_names(query)
            if is_admin_name(name) and strip_accents(name) not in self.admin_labels
        ]

    def _intent_bonus(self, intent: frozenset[str], chunk: dict) -> float:
        """Điểm cho chunk KHỚP Ý ĐỊNH câu hỏi - tín hiệu cấp CHUNK, không cấp bài."""
        if not intent:
            return 0.0
        bonus = 0.0
        if "location" in intent:
            heading = strip_accents(chunk["heading"])
            if any(h in heading for h in LOCATION_HEADINGS) or is_lead(chunk):
                bonus += INTENT_HEADING_BONUS
        if "ward" in intent and is_admin_chunk(chunk):
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
        """Trả về {hits, seeds, specific, named, subject, anchored, intent, scope}.

        `anchored`  = câu hỏi có neo vào miền tri thức này.
        `specific`  = tên riêng cụ thể mà câu hỏi gọi (entity/doc, không phải hub).
                      `rag.py` dùng nó để đòi BẰNG CHỨNG: hỏi đúng tên một di sản
                      mà chunk tốt nhất không hề nhắc tên đó thì hệ chưa có tư liệu.
        `subject`   = tên riêng ĐANG ĐƯỢC HỎI khi câu nêu nhiều tên; "" nếu không
                      phân định được. `rag.py` dùng để đòi bằng chứng đúng chỗ.
        `foreign_admin` = địa danh hành chính trong câu mà corpus không nhắc tới;
                      `rag.py` dùng để từ chối câu hỏi về vùng ngoài phạm vi.
        `intent`    = ý định câu hỏi; `rag.py` dùng để ép kèm chunk mở đầu.
        `scope`     = (region, category) suy từ câu hỏi; "" nghĩa là không giới hạn.

        Mỗi hit có HAI điểm: `score` (cấp bài, để chọn bài) và `chunk_score`
        (chỉ tín hiệu từ câu hỏi, để chọn chunk trong bài). Xem docstring module.
        """
        empty: dict = {"hits": [], "seeds": [], "specific": [], "named": [],
                       "subject": "", "anchored": False, "foreign_admin": [],
                       "intent": frozenset(), "scope": ("", "")}
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
        foreign = self.foreign_admin(query)
        if not lexical and not named:
            return empty

        seed_labels = [
            self.graph.nodes[s]["label"] for s in seeds
            if self.graph.nodes[s].get("kind") in ("entity", "doc")
        ]
        # CHỈ CHỦ ĐỀ ĐƯỢC CỘNG NAMED_DOC_BONUS. Câu nêu hai tên riêng thì tên nằm
        # trong giả định KHÔNG phải thứ đang được hỏi, nên bài của nó không được
        # coi là "bài mà câu hỏi gọi đúng tên". Bỏ bước này thì "Lăng Tự Đức ở
        # phường Ngũ Hành Sơn đúng không" trả về bài Ngũ Hành Sơn (lexical cao hơn
        # vì tên đó dài hơn), và model xác nhận một điều sai bằng nguồn nói về nơi
        # khác - sai tệ hơn hẳn so với từ chối.
        subject, claim_names = subject_and_claims(query, seed_labels)
        if subject:
            named -= {f"doc:{n}" for n in claim_names}

        pool = None if named else self._scope_pool(scope)
        if pool is not None:
            lexical = {i: s for i, s in lexical.items() if i in pool}
            if not lexical:
                lexical = _rrf(
                    self.word.search(word_tokens(query)),
                    self.ngram.search(ngram_tokens(query)),
                )
                pool = None

        cand = {i for i, _ in sorted(lexical.items(), key=lambda kv: -kv[1])[:CANDIDATES]}
        for dn in named:
            ranked = sorted(self.doc_index.get(dn, []), key=lambda i: -lexical.get(i, 0.0))
            cand.update(ranked[:INJECT_PER_DOC])
        best = max((lexical.get(i, 0.0) for i in cand), default=0.0) or 1.0

        doc_scores = expand_docs(self.graph, seeds)
        q_words = set(word_tokens(strip_accents(query)))

        out: list[dict] = []
        for i in cand:
            c = self.chunks[i]
            lex = lexical.get(i, 0.0) / best
            g = doc_scores.get(c["doc_node"], 0.0)
            hits = [lb for lb in seed_labels if contains_name(self.plain[i], lb)]
            intent_bonus = self._intent_bonus(intent, c)
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

        out.sort(key=lambda r: -r["score"])
        if out:
            top_doc = out[0]["doc_node"]
            out.sort(key=lambda r: (r["doc_node"] != top_doc, -r["chunk_score"]))

        return {
            "hits": out[:top_k],
            "seeds": [self.graph.nodes[s]["label"] for s in seeds],
            "specific": seed_labels,
            "named": sorted(self.graph.nodes[n]["label"] for n in named),
            "subject": subject,
            "anchored": anchored,
            "foreign_admin": foreign,
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
