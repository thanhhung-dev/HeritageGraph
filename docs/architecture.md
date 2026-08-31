# Kiến trúc hệ thống

Số liệu trong tài liệu này là ĐO ĐƯỢC trên repo hiện tại, không phải dự kiến.
Muốn tự đo lại: `bash scripts/run_indexing.sh` và `backend/.venv/bin/python eval/eval_retrieval.py`.

## Sơ đồ tổng quan

```
┌──────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                    │
│  User hỏi → chat UI (localhost:3000)                     │
└────────────────────────┬─────────────────────────────────┘
                         │ POST /api/chat
                         ▼
┌──────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                     │
│  ┌────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  /api/chat │───▶│   rag.py     │───▶│    llm.py    │ │
│  │ /api/graph │    │ (cổng từ chối)│    │              │ │
│  └────────────┘    └──────┬───────┘    └──────┬───────┘ │
└───────────────────────────┼───────────────────┼─────────┘
                            ▼                   ▼
        ┌───────────────────────────────┐  ┌──────────────────┐
        │  retriever.py + kg.py         │  │  Qwen+LoRA fused │
        │  - BM25 theo từ               │  │  models/         │
        │  - BM25 theo n-gram (bỏ dấu)  │  │  qwen-fused/     │
        │  - graph 331 node / 563 edge  │  │  (~2GB, 3B-4bit) │
        │  dựng trong RAM, 0.14s        │  └──────────────────┘
        └───────────────────────────────┘
```

Không có Ollama, không có vector DB, không có file parquet. Retrieval và graph
đều dựng trong RAM lúc khởi động (`@lru_cache` trên `get_retriever()`).

## Luồng dữ liệu chi tiết

### 1. Ingestion (1 lần, offline)

```
Wikipedia VN (49 địa điểm Huế + Đà Nẵng trong training/locations_hue_danang.py)
       ↓ ingestion/crawl_by_location.py
corpus/wiki_by_location/*.txt   (25 crawl được, 24 chưa - xem locations_index.json)
       ↓ backend/core/corpus.py: load_docs()
23 bài dùng được / 215 chunk    (bỏ 1 bài trùng nội dung, 1 trang định hướng)
```

`backend/core/corpus.py` là NGUỒN DUY NHẤT của việc chunk. Cả training và serving
đều import từ đây, nên đoạn `Nguồn:` lúc train có đúng hình dạng đoạn `Nguồn:`
lúc chạy thật.

### 2. Knowledge graph (dựng lại mỗi lần khởi động, 0.14s)

```
23 bài + corpus/locations_index.json
       ↓ backend/core/kg.py: build_graph()   ← KHÔNG gọi LLM
331 node: 147 entity, 153 year, 23 doc, 6 category, 2 region
563 edge: 214 year, 141 mentions, 72 in_region, 72 in_category, 41 related, 23 is_about
1 thành phần liên thông, không có bài cô lập
```

Node entity đến từ hai nguồn deterministic:
- 49 địa điểm curated trong `locations_index.json` (kể cả 24 chưa crawl được -
  chúng vẫn là node hợp lệ để nối quan hệ);
- tên riêng bắt bằng mẫu "danh từ loại + tên riêng" của tiếng Việt
  (`lăng X`, `vua X`, `triều X`, `chùa X`...), yêu cầu xuất hiện ≥ 2 lần.

Vì vậy mọi node đều truy được về một chuỗi CÓ THẬT trong văn bản: graph không bao
giờ thêm thông tin sai vào hệ. Xuất artifact xem bằng Gephi/D3:
`bash scripts/run_indexing.sh` → `graphrag/output/{graph.gexf, graph.json, stats.json}`.

### 3. Training (1 lần, offline)

```
23 bài (cùng chunker với serving)
       ↓ training/bootstrap_deep_qa.py
data/train.jsonl 169 mẫu (30 refusal) + valid.jsonl 38 mẫu (9 refusal)
       ↓ mlx_lm.lora  (training/lora_config.yaml: r=16, 16 layer, mask_prompt, cosine_decay)
models/lora-adapter/                 13.3M tham số huấn luyện
       ↓ mlx_lm.fuse (training/fuse.sh)
models/qwen-fused/
```

Valid tách theo ĐỊA ĐIỂM, và mẫu valid nào dùng chung đoạn nguồn với train thì bị
bỏ - kiểm tra lại được bằng `source_of()` trong `bootstrap_deep_qa.py`.

### 4. Runtime (user hỏi)

```
User: "lang minh mang o dau"        (gõ không dấu - trường hợp rất thường gặp)
       ↓  POST /api/chat
retriever.retrieve()
   ├── BM25 theo từ    (có dấu, chính xác chính tả)
   ├── BM25 theo n-gram (4-gram trên text bỏ dấu → chịu được không dấu, sai chính tả)
   ├── hợp nhất bằng RRF (k=60, không cần scale điểm)
   ├── graph: find_seeds → "Lăng Minh Mạng" [entity]
   │          expand_docs 2 hop → điểm cho từng bài
   │          BƠM ỨNG VIÊN: chunk của bài được gọi đúng tên vào pool dù lexical thấp
   └── điểm = lexical + 0.35·graph + 0.15·entity_trong_chunk + 0.8·gọi-đúng-tên
       ↓
rag.retrieve_context()  → BA CỔNG TỪ CHỐI (xem bên dưới)
       ↓
context = 1 hoặc 2 chunk NỐI LIỀN (≤ 2200 ký tự, giữ thứ tự trong bài)
       ↓
llm.generate_response(): "Nguồn: {context}\n\nCâu hỏi: {question}"
       ↓
Qwen+LoRA: "... [Nguồn: <trích đoạn> — <url>]"
```

Context là MỘT đoạn văn liền mạch, không có dấu phân cách lạ, vì mỗi mẫu train có
`Nguồn:` là nội dung của một chunk. Nối nhiều chunk bằng ký hiệu lạ là tạo ra định
dạng model chưa từng thấy.

## Ba cổng từ chối (`backend/core/rag.py`)

Chatbot miền đóng thì TỪ CHỐI ĐÚNG quan trọng ngang trả lời đúng.

| Cổng | Điều kiện | Chặn được gì |
|---|---|---|
| Neo vào graph | câu hỏi phải nhắc tên một entity/bài/vùng/loại mà graph biết | câu ngoài miền ("giá bitcoin", "giải phương trình") |
| Bằng chứng | đã gọi đúng tên riêng thì chunk tốt nhất phải thuộc bài đó hoặc phải nhắc tên đó | câu neo đúng miền nhưng hệ CHƯA có tư liệu ("Đàn Nam Giao thờ ai" - có node, không có bài) |
| Coverage | ≥ 0.25 trọng số IDF của từ khoá câu hỏi có trong chunk | phần dư |

Đo trên 22 câu trong phạm vi / 10 câu ngoài phạm vi: coverage một mình KHÔNG phân
tách được (trong 0.36-0.80, ngoài 0.19-1.00 - hư từ tiếng Việt có mặt trong bài
wiki nào cũng vậy), còn "có neo vào graph" phân tách sạch. Đây là chỗ graph trả
giá trị rõ nhất: nó là thứ duy nhất biết câu hỏi có thuộc miền tri thức này không.

Khi cổng chặn, context rỗng → `llm.py` ghi `Nguồn: (không có)` → đúng dạng các mẫu
refusal đã train, nên model từ chối lịch sự. Đây là hành vi mong muốn, không phải lỗi.

## Kết quả đo (`eval/eval_retrieval.py`)

```
recall@1 = 22/22   recall@3 = 22/22   từ chối đúng = 10/10
```

Bao gồm cả truy vấn không dấu (`lang minh mang o dau`, `me xung lam tu gi`,
`cao lau la mon gi`, `bao tang co vat cung dinh hue trung bay gi`).

Con số này chỉ là NỬA TRÊN của độ chính xác:
`P(đúng) = P(lấy đúng đoạn) × P(model trung thực với đoạn đó)`. Nửa dưới do LoRA
lo và phải đo riêng bằng gold set (`eval/`).

## Tại sao thiết kế này?

| Quyết định | Lý do |
|---|---|
| Graph deterministic thay vì để LLM extract entity | Corpus 23 bài; index bằng LLM local mất 8-12 giờ, prompt extract mặc định bằng tiếng Anh trên văn bản tiếng Việt sai nhiều, và entity do LLM sinh có thể BỊA. Cách này build 0.14s và không bao giờ bịa. |
| Graph để MỞ RỘNG/XẾP LẠI retrieval, không để sinh câu trả lời | Câu trả lời phải truy được về văn bản gốc để trích nguồn |
| Graph vừa rerank vừa BƠM ứng viên | Truy vấn ngắn không dấu sinh nhiều n-gram phổ biến làm bài đúng rơi khỏi top-30; rerank thuần không cứu được, phải đưa bài đúng vào pool |
| BM25 + n-gram thay vì embedding | Không phải tải model, chạy offline ngay, và n-gram bỏ dấu xử lý được truy vấn không dấu - chỗ mà embedding tiếng Việt cũng hay trượt |
| RRF thay vì cộng điểm có trọng số | Hợp nhất theo THỨ HẠNG nên không phải chuẩn hoá thang điểm giữa hai nhánh |
| LoRA thay vì RAG-only | RAG cấp kiến thức, LoRA dạy văn phong + định dạng trích dẫn + CÁCH TỪ CHỐI |
| Qwen2.5-3B-4bit | Vừa RAM, train nhanh; kiến thức đến từ nguồn nên không cần model to |

## Trade-offs đã chọn

| Chọn | Bỏ qua | Lý do |
|---|---|---|
| kg.py tự viết | Microsoft GraphRAG + Ollama | 8-12h index, prompt tiếng Anh, entity có thể bịa, corpus quá nhỏ để đáng |
| Dựng index trong RAM | Vector DB / file parquet | 0.14s, và không bao giờ lệch với corpus hiện tại |
| Từ chối khi không neo được | Cố trả lời mọi câu | Câu bịa tự tin tệ hơn câu từ chối |
| LoRA r=16 | r=64, full FT | Tránh overfit trên 169 mẫu |
| Corpus Wikipedia trước | Nguồn học thuật | Mở rộng dần; pipeline không phụ thuộc nguồn |
