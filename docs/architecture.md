# Kiến trúc hệ thống

## Sơ đồ tổng quan

```
┌──────────────────────────────────────────────────────────┐
│                       Frontend (Next.js)                  │
│  User hỏi → chat UI (localhost:3000)                     │
└────────────────────────┬─────────────────────────────────┘
                         │ POST /api/chat
                         ▼
┌──────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                     │
│  ┌────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  /api/chat │───▶│  RAG module  │───▶│  LLM module  │ │
│  └────────────┘    └──────────────┘    └──────────────┘ │
│                           │                     │        │
│                           ▼                     ▼        │
└───────────────────────────┼─────────────────────┼────────┘
                            │                     │
                            ▼                     ▼
              ┌──────────────────────┐  ┌──────────────────┐
              │  GraphRAG (local)    │  │  Qwen+LoRA fused │
              │  - entities.parquet  │  │  models/         │
              │  - relationships...  │  │  qwen-7b-fused/  │
              │  - communities...    │  │  (~5GB)          │
              └──────────────────────┘  └──────────────────┘
```

## Luồng dữ liệu chi tiết

### 1. Ingestion (1 lần, chạy offline)

```
Wikipedia VN (Đà Nẵng, Huế)
       ↓ crawl_wiki_mientrung.py
corpus/wiki/*.txt (200-300 bài)
       ↓ chunk_corpus.py
graphrag/input/*.txt (~600-1500 chunks)
       ↓ graphrag.index (chạy 8-12h)
graphrag/output/{entities, relationships, communities, embeddings}.parquet
```

### 2. Training (1 lần, chạy offline)

```
graphrag/input/*.txt  (chunks)
       ↓ bootstrap_lora_data.py (Qwen teacher sinh 1500 mẫu)
data/train.jsonl + valid.jsonl
       ↓ mlx_lm.lora
models/lora-adapter/ (50-100MB)
       ↓ mlx_lm.fuse
models/qwen-7b-fused/ (5GB, model hoàn chỉnh)
```

### 3. Runtime (user hỏi)

```
User: "Hãy kể về Festival Huế"
       ↓
Backend /api/chat nhận message
       ↓
rag.retrieve_context()  → GraphRAG query local
       ↓
context = "Festival Huế là sự kiện văn hóa nghệ thuật..."
sources = [{text: "...", score: 0.92}, ...]
       ↓
llm.generate_response(question, context)
       ↓
Qwen+LoRA: "Festival Huế được tổ chức lần đầu năm 2000... [Nguồn: ...]"
       ↓
Frontend hiển thị answer + collapsible sources
```

## Tại sao thiết kế này?

| Quyết định | Lý do |
|---|---|
| GraphRAG thay vì vector search thuần | Văn hóa dân gian có nhiều quan hệ (nghệ nhân - làng - lễ hội), graph query tốt hơn |
| LoRA thay vì RAG-only | RAG cung cấp kiến thức, LoRA tối ưu cách diễn đạt (văn phong, format NER, citation) |
| 7B thay vì 14B | Vừa RAM M4 Pro 24GB, train nhanh, đủ tốt cho demo |
| 4-bit base | Giảm RAM, không giảm chất lượng nhiều cho SFT |
| Local 100% | Demo offline, không lo API key hết hạn, reproducible |

## Trade-offs đã chọn

| Chọn | Bỏ qua | Lý do |
|---|---|---|
| GraphRAG local | OpenAI API | $0 budget, demo offline |
| Qwen 7B | Qwen 14B, GPT-4 | Vừa 24GB RAM, train nhanh |
| LoRA r=16 | LoRA r=64, full FT | Tránh overfit ~1.5k mẫu, train nhanh |
| Streamlit/Next.js | Production UI | Chỉ cần demo đồ án |
| Vector + graph | Vector only | Quan hệ trong văn hóa rất quan trọng |
