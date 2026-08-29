# vanhoa-danang-hue

Chatbot về văn hóa dân gian **Đà Nẵng – Huế** (miền Trung Việt Nam).
- **RAG**: Microsoft GraphRAG + Ollama (Qwen2.5-7B)
- **LoRA fine-tune**: Qwen2.5-7B-Instruct-4bit trên Apple Silicon (MLX)
- **Backend**: FastAPI
- **Frontend**: Next.js
- **100% local**, không cần API key, không cần internet (sau khi setup)

## Cấu trúc

```
vanhoa-danang-hue/
├── ingestion/                # Thu thập + xử lý corpus
│   ├── crawl_wiki_mientrung.py
│   └── chunk_corpus.py
├── training/                 # Fine-tune LoRA
│   ├── lora_config.yaml
│   ├── train.sh
│   ├── fuse.sh
│   ├── score_gold.py
│   └── ...
├── graphrag/                 # Knowledge graph
│   ├── input/                # chunks đầu vào
│   ├── settings.yaml
│   └── output/               # entities, relationships, communities
├── backend/                  # FastAPI
│   ├── app.py
│   ├── api/chat.py
│   ├── api/health.py
│   └── core/llm.py           # Qwen+LoRA inference
├── frontend/                 # Next.js
│   ├── app/page.tsx
│   └── package.json
├── data/                     # training data
├── models/                   # LoRA adapter + fused model
├── eval/                     # gold set + report
├── scripts/                  # utility (start_dev, run_indexing, ...)
└── docs/                     # tài liệu đồ án
```

## Quick start

### Bước 0: Setup (30 phút)

```bash
# 1. Clone + venv
cd ~/vanhoa-danang-hue
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# 2. Ollama
brew install ollama
ollama serve &
ollama pull qwen2.5:7b-instruct
ollama pull bge-m3

# 3. Frontend deps
cd frontend && npm install && cd ..
```

### Bước 1: Crawl corpus (2-3 giờ)

```bash
source .venv/bin/activate
python ingestion/crawl_wiki_mientrung.py --max 300
python ingestion/chunk_corpus.py
```

### Bước 2: Index GraphRAG (chạy qua đêm, 8-12 giờ)

```bash
python -m graphrag.index --init --root ./graphrag
# Sửa graphrag/settings.yaml → dùng Ollama
bash scripts/run_indexing.sh
```

### Bước 3: Train LoRA (30 phút)

```bash
# Bootstrap training data từ chunks (3-4 giờ, dùng Qwen làm teacher)
# ... (xem docs/bootstrap-data.md)

# Train
bash training/train.sh
bash training/fuse.sh
```

### Bước 4: Chạy app (demo)

```bash
# Backend
source .venv/bin/activate
uvicorn backend.app:app --port 8000

# Frontend (terminal khác)
cd frontend && npm run dev

# Mở http://localhost:3000
```

Hoặc chạy cả 2 cùng lúc:
```bash
bash scripts/start_dev.sh
```

## Tech stack chi tiết

| Layer | Công nghệ | Vai trò |
|---|---|---|
| **Frontend** | Next.js 14, React 18, TypeScript | UI chat cho hội đồng demo |
| **Backend** | FastAPI, Pydantic, Uvicorn | API server, orchestration |
| **LLM** | Qwen2.5-7B-Instruct-4bit (MLX) | Generation, có LoRA fine-tune |
| **RAG** | Microsoft GraphRAG + bge-m3 | Truy xuất context từ knowledge graph |
| **Fine-tune** | mlx-lm, LoRA rank 16 | Tối ưu cho domain văn hóa |
| **Corpus** | Wikipedia VN (Đà Nẵng, Huế) | 200-300 bài crawl tự động |

## Đánh giá

```bash
# Tạo gold set (cần gán nhãn tay ~50-100 mẫu)
python training/make_gold_template.py
nano eval/gold.jsonl

# Chạy eval 4 metric: NER F1 / Citation / Refusal / Style
python training/score_gold.py \
  --model models/qwen-7b-fused \
  --gold eval/gold.jsonl \
  --out eval/report.json
```

## Tài liệu

- [docs/architecture.md](docs/architecture.md) - Kiến trúc chi tiết
- [docs/metrics.md](docs/metrics.md) - 4 metric đánh giá
- [docs/demo-guide.md](docs/demo-guide.md) - Hướng dẫn demo cho hội đồng

## Chi phí

| Hạng mục | Chi phí |
|---|---|
| API | $0 |
| Điện (~30h × 40W) | ~$0.20 |
| Phần mềm | $0 |
| **Tổng** | **~$0.20** |
