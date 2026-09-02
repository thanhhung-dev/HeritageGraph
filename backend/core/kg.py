"""Knowledge graph tri thức di sản - xây HOÀN TOÀN DETERMINISTIC, không gọi LLM.

Vì sao không dùng LLM để extract entity (như MS GraphRAG làm):
- Corpus 22 bài, index bằng model 3B local mất nhiều giờ và entity tiếng Việt
  extract bằng prompt tiếng Anh mặc định thì sai nhiều.
- Entity do LLM sinh ra có thể BỊA. Ở đây mọi node đều truy được về một chuỗi
  có thật trong văn bản, nên graph không bao giờ thêm thông tin sai vào hệ.
Graph này dùng để MỞ RỘNG/XẾP LẠI kết quả retrieval, không dùng để sinh câu trả lời.

Nguồn node:
- doc      : mỗi bài trong corpus
- entity   : 49 địa điểm curated trong locations_index.json (kể cả 24 chưa crawl
             được - chúng vẫn là node hợp lệ để nối quan hệ) + tên riêng bắt được
             bằng mẫu "danh từ loại + tên riêng" của tiếng Việt
- region / category : hub phân loại
- year     : mốc thời gian (rất hay được hỏi với di sản)

ALIAS là THUỘC TÍNH của node doc, không phải node riêng: tạo node riêng thì
`_named_docs` và `expand_docs` đếm MỘT thực thể thành HAI, điểm graph phồng sai.
Artifact do ingestion/fetch_aliases.py sinh, commit vào repo nên runtime offline.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from functools import lru_cache

import networkx as nx

from backend.core.config import PROJECT_ROOT
from backend.core.corpus import INDEX_FILE
from backend.core.textutil import contains_name, nfc, strip_accents

ALIAS_FILE = PROJECT_ROOT / "corpus" / "aliases.json"

# Alias ngắn hơn ngưỡng này khớp bừa vào mọi bài ("Huế", "Sơn"). fetch_aliases.py
# đã lọc, nhắc lại ở đây để artifact chỉnh tay cũng không phá được retrieval.
MIN_ALIAS_CHARS = 4

U = "A-ZĐÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ"
L = "a-zđàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ"

# Tiếng Việt gần như luôn đặt danh từ loại trước tên riêng ("lăng Tự Đức",
# "sông Hương", "vua Minh Mạng"). Mẫu này vì thế vừa deterministic vừa mở rộng
# được khi corpus lớn dần - không phải danh sách hardcode.
CLASSIFIERS = (
    "vua", "chúa", "hoàng đế", "hoàng hậu", "công chúa", "thái tử",
    "lăng", "chùa", "đền", "miếu", "đình", "điện", "cung", "thành", "đàn",
    "làng", "phường", "xã", "huyện", "quận", "tỉnh", "thị xã",
    "sông", "núi", "đèo", "biển", "bán đảo", "cầu", "hồ", "vịnh",
    "bảo tàng", "lễ hội", "nhà hát",
    # "nhà thờ chính tòa" phải có mặt CÙNG "nhà thờ": hàm sort dưới đây lo thứ tự,
    # nhưng thiếu bản dài thì "nhà thờ chính tòa Đà Nẵng" chỉ bắt được "nhà thờ
    # chính" - danh từ loại ăn mất một chữ của tên riêng.
    "nhà thờ", "nhà thờ chính tòa",
    # triều đại: cầu nối nhiều chặng quan trọng nhất của corpus di sản
    # ("triều Nguyễn" -> tất cả các lăng, hoàng thành, nhã nhạc)
    "vương triều", "triều", "nhà", "thời", "kinh thành", "hoàng thành",
)
# Sắp theo độ dài GIẢM DẦN: regex alternation lấy nhánh khớp ĐẦU TIÊN, nếu để
# "thành" trước "hoàng thành" thì "hoàng thành Huế" bị bắt thành "thành Huế".
NAME_RE = re.compile(
    r"(?<!\w)("
    + "|".join(sorted(CLASSIFIERS, key=len, reverse=True))
    + r")\s+((?:[" + U + r"][" + L + r"]+\s?){1,3})"
)
YEAR_RE = re.compile(r"(?<!\d)(1[0-9]{3}|20[0-2][0-9])(?!\d)")

MIN_ENTITY_MENTIONS = 2   # tên chỉ xuất hiện 1 lần thường là nhiễu của mẫu regex
MAX_RELATED_PER_DOC = 6   # không để graph thành đồ thị đầy


def extract_names(text: str) -> Counter:
    """Trả về Counter{"lăng Tự Đức": n} - danh từ loại viết thường, tên giữ nguyên."""
    found: Counter = Counter()
    for cls, name in NAME_RE.findall(nfc(text)):
        name = name.strip()
        if len(name) >= 2:
            found[f"{cls.lower()} {name}"] += 1
    return found


def extract_years(text: str) -> Counter:
    return Counter(YEAR_RE.findall(text))


def curated_entities() -> list[dict]:
    """49 địa điểm trong locations_index.json - cả success và failed."""
    data = json.loads(INDEX_FILE.read_text("utf-8"))
    return [
        {"name": e["name"], "region": e.get("region", ""), "category": e.get("category", "")}
        for e in list(data.get("success", [])) + list(data.get("failed", []))
    ]


@lru_cache(maxsize=1)
def load_aliases() -> dict[str, tuple[str, ...]]:
    """{tên bài: (alias,)} từ corpus/aliases.json. Thiếu file -> rỗng, không lỗi.

    Alias là thứ TĂNG recall; vắng nó hệ vẫn chạy đúng như trước, nên không nên
    làm backend chết vì một artifact chưa sinh.
    """
    if not ALIAS_FILE.exists():
        return {}
    raw = json.loads(ALIAS_FILE.read_text("utf-8"))
    return {
        name: tuple(a for a in aliases if len(a) >= MIN_ALIAS_CHARS)
        for name, aliases in raw.items()
    }


def build_graph(docs: list[dict]) -> nx.Graph:
    G = nx.Graph()
    aliases = load_aliases()

    for ent in curated_entities():
        G.add_node(f"entity:{ent['name']}", kind="entity", label=ent["name"], curated=True)
        for kind, val in (("region", ent["region"]), ("category", ent["category"])):
            if val:
                G.add_node(f"{kind}:{val}", kind=kind, label=val)
                G.add_edge(f"entity:{ent['name']}", f"{kind}:{val}", rel=f"in_{kind}", weight=1.0)

    doc_names: dict[str, Counter] = {}

    for doc in docs:
        dnode = f"doc:{doc['name']}"
        full = " ".join(c["heading"] + " " + c["text"] for c in doc["chunks"])
        G.add_node(
            dnode, kind="doc", label=doc["name"], url=doc["url"],
            region=doc["region"], category=doc["category"], n_chunks=len(doc["chunks"]),
            aliases=list(aliases.get(doc["name"], ())),
        )
        # bài viết và địa điểm curated cùng tên là CÙNG một thực thể
        if f"entity:{doc['name']}" in G:
            G.add_edge(dnode, f"entity:{doc['name']}", rel="is_about", weight=3.0)
        for kind, val in (("region", doc["region"]), ("category", doc["category"])):
            if val:
                G.add_node(f"{kind}:{val}", kind=kind, label=val)
                G.add_edge(dnode, f"{kind}:{val}", rel=f"in_{kind}", weight=1.0)

        plain = strip_accents(full)
        mentions: Counter = Counter()

        # (a) địa điểm curated được nhắc trong bài -> quan hệ giữa các di sản
        for ent in curated_entities():
            if ent["name"] != doc["name"] and contains_name(plain, ent["name"]):
                mentions[f"entity:{ent['name']}"] += 1

        # (b) tên riêng bắt bằng mẫu danh từ loại
        for name, cnt in extract_names(full).items():
            if cnt >= MIN_ENTITY_MENTIONS:
                node = f"entity:{name}"
                if node not in G:
                    G.add_node(node, kind="entity", label=name, curated=False)
                mentions[node] += cnt

        for node, cnt in mentions.items():
            G.add_edge(dnode, node, rel="mentions", weight=float(min(cnt, 5)))

        for year, cnt in extract_years(full).items():
            if cnt >= 1:
                G.add_node(f"year:{year}", kind="year", label=year)
                G.add_edge(dnode, f"year:{year}", rel="year", weight=float(min(cnt, 3)))

        doc_names[dnode] = mentions

    # doc <-> doc: chia sẻ càng nhiều entity thì càng liên quan
    for a in doc_names:
        shared = Counter()
        for b in doc_names:
            if a != b:
                common = set(doc_names[a]) & set(doc_names[b])
                if common:
                    shared[b] = len(common)
        for b, n in shared.most_common(MAX_RELATED_PER_DOC):
            if not G.has_edge(a, b):
                G.add_edge(a, b, rel="related", weight=float(min(n, 5)))

    return G


def graph_stats(G: nx.Graph) -> dict:
    kinds = Counter(d.get("kind", "?") for _, d in G.nodes(data=True))
    rels = Counter(d.get("rel", "?") for _, _, d in G.edges(data=True))
    docs = [n for n, d in G.nodes(data=True) if d.get("kind") == "doc"]
    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "by_kind": dict(kinds),
        "by_rel": dict(rels),
        "components": nx.number_connected_components(G),
        "top_hub": [
            (G.nodes[n]["label"], G.degree(n))
            for n in sorted(G, key=G.degree, reverse=True)[:8]
        ],
        "isolated_docs": [G.nodes[n]["label"] for n in docs if G.degree(n) <= 2],
    }


# --- Phía truy vấn -----------------------------------------------------------

# region/category có bậc rất lớn; nếu lan truyền bình thường thì hỏi bất cứ gì về
# Huế cũng kéo về cả 15 bài Huế. Hạ đóng góp của hub xuống thấp.
HUB_KINDS = frozenset({"region", "category"})
HUB_FACTOR = 0.25
DECAY = 0.45


def find_seeds(G: nx.Graph, query: str) -> list[str]:
    """Node xuất hiện TRỰC TIẾP trong câu hỏi. Ưu tiên tên dài (khớp cụ thể hơn).

    Khớp cả ALIAS nhưng luôn trả về NODE GỐC: người dùng gõ "nhà thờ con gà",
    hệ phải neo vào doc "Nhà thờ chính tòa Đà Nẵng". Trước khi có alias, câu đó
    cho seeds rỗng -> cổng REQUIRE_GRAPH_ANCHOR (rag.py) ném sạch kết quả đúng
    mà BM25 đã tìm ra với coverage 1.0.
    """
    plain = strip_accents(query)
    # (node, chuỗi để khớp). Alias và label vào CÙNG một danh sách rồi sort theo
    # độ dài: alias dài phải thắng label ngắn của bài khác, nếu tách hai vòng thì
    # "Đại nội Huế" (alias) mất cho "Huế" (label region).
    candidates: list[tuple[str, str]] = []
    for node, data in G.nodes(data=True):
        if data.get("kind") == "year":
            continue
        label = data["label"]
        if len(label) >= 3:
            candidates.append((node, label))
        for alias in data.get("aliases", ()):
            if len(alias) >= MIN_ALIAS_CHARS:
                candidates.append((node, alias))
    candidates.sort(key=lambda ns: -len(ns[1]))

    seeds: list[str] = []
    taken = ""
    for node, name in candidates:
        if node in seeds or not contains_name(plain, name):
            continue
        # bỏ tên bị bao trong tên đã lấy ("lăng" khi đã có "lăng Tự Đức")
        if strip_accents(name) in taken:
            continue
        seeds.append(node)
        taken += " " + strip_accents(name)
    for year in YEAR_RE.findall(query):
        if f"year:{year}" in G:
            seeds.append(f"year:{year}")
    return seeds


def expand_docs(G: nx.Graph, seeds: list[str], hops: int = 2) -> dict[str, float]:
    """Lan truyền từ seed ra các doc node, trả về {doc node: điểm 0..1}."""
    scores: dict[str, float] = {}
    frontier = {s: 1.0 for s in seeds if s in G}
    seen = set(frontier)

    for _ in range(max(hops, 0)):
        nxt: dict[str, float] = {}
        for node, w in frontier.items():
            kind = G.nodes[node].get("kind")
            if kind == "doc":
                scores[node] = max(scores.get(node, 0.0), w)
            step = w * DECAY * (HUB_FACTOR if kind in HUB_KINDS else 1.0)
            if step < 0.02:
                continue
            for nb in G.neighbors(node):
                if nb in seen:
                    continue
                ew = G[node][nb].get("weight", 1.0)
                nxt[nb] = max(nxt.get(nb, 0.0), step * min(ew, 3.0) / 3.0)
        seen |= set(nxt)
        frontier = nxt

    for node, w in frontier.items():
        if G.nodes[node].get("kind") == "doc":
            scores[node] = max(scores.get(node, 0.0), w)
    return scores
