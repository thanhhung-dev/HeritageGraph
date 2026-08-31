# Hướng dẫn demo cho hội đồng

## Trước buổi bảo vệ (1 ngày)

- [ ] Chạy full pipeline: crawl → xây graph → sinh data → train → fuse
- [ ] Verify backend + frontend chạy được
- [ ] Test 5-10 câu hỏi mẫu, chuẩn bị "demo script"
- [ ] In sẵn 4 metric (NER F1, Citation, Refusal, Style) + số đo retrieval
- [ ] Chuẩn bị slide với sơ đồ kiến trúc

## Setup trong phòng bảo vệ (10 phút trước)

```bash
# 1. Mở Terminal, cd vào project
cd ~/CAP/HeritageGraph

# 2. Verify graph + retrieval (1 giây, không cần model)
backend/.venv/bin/python eval/eval_retrieval.py
#    → recall@1 = 22/22   từ chối đúng = 10/10

# 3. Chạy cả backend + frontend
bash scripts/start_dev.sh

# 4. Mở browser
open http://localhost:3000
```

Không cần khởi động Ollama: graph được xây deterministic trong RAM lúc backend
lên, không có bước index bằng LLM.

## Demo flow (10-15 phút)

### 1. Giới thiệu kiến trúc (2 phút)
- Mở slide kiến trúc
- Giải thích: graph + BM25 (knowledge) + LoRA (output style) + FastAPI/Next.js (app)
- Cho xem graph thật, không chỉ sơ đồ:
  `backend/.venv/bin/python scripts/build_graph.py --node "triều Nguyễn"`

### 2. Demo chatbot (5 phút)
Mở `http://localhost:3000`, hỏi tuần tự:

| Câu hỏi | Mục đích demo |
|---|---|
| "Hãy kể về Festival Huế" | Trả lời dài, có citation, văn phong trang trọng |
| "Trích entity từ đoạn sau: Điện Hòn Chén được vua Minh Mạng cho tu sửa và mở rộng vào tháng 3/1832." | NER đúng 4 loại, format JSON |
| "Ngũ Hành Sơn có ý nghĩa gì trong văn hóa Đà Nẵng?" | Kết hợp kiến thức + citation |
| "Hãy kể chi tiết về Hoàng thành Huế" | Test với câu hỏi dài, multi-entity |
| "Chùa Một Cột được xây năm nào?" | Ngoài phạm vi corpus → phải TỪ CHỐI, không bịa |

Chỉ hỏi về 23 bài đã crawl được (`backend/.venv/bin/python -c "..."` hoặc xem
`data/corpus/locations_index.json`). 24 địa điểm bị crawl lỗi - trong đó có CẢ 7
lễ hội, nên câu "Lễ hội Quan Thế Âm ở Đà Nẵng có ý nghĩa gì?" sẽ bị từ chối:
đúng theo thiết kế, nhưng đừng đưa vào phần demo kiến thức.

### 3. So sánh base vs LoRA (3 phút)
Mở terminal:
```bash
# Sinh gold set (lấy từ 5 bài KHÔNG có trong train) rồi soát tay phần ner-*
backend/.venv/bin/python eval/make_gold_template.py

# Đo base và đo LoRA bằng CÙNG một prompt (backend/core/prompt.py)
backend/.venv/bin/python training/score_gold.py --model mlx-community/Qwen2.5-3B-Instruct-4bit \
  --gold eval/gold.jsonl --out eval/report_base.json
backend/.venv/bin/python training/score_gold.py --model ./models/qwen-fused \
  --gold eval/gold.jsonl --out eval/report_lora.json
```

Bảng so sánh - cột base ĐÃ ĐO THẬT, cột LoRA điền sau khi train + fuse:

| Metric | base (đo thật) | LoRA | Lấy ở đâu trong report |
|---|---|---|---|
| NER micro-F1 | 0.08 | ? | `ner_micro.f1` |
| Citation faithful rate | 0.00 | ? | `citation_faithful_rate` |
| Refusal accuracy | 0.33 | ? | `refusal_accuracy` |

Ba điều phải nói thẳng nếu hội đồng hỏi:
- Nhãn NER trong gold do `backend/core/nerlabel.py` điền sẵn từ graph rồi soát tay;
  phần chưa soát vẫn còn cờ `"_prefilled": true`.
- Loại `sự kiện` gần như không có mẫu (cả corpus chỉ có 6 nhãn / 3 bài), nên F1 của
  riêng loại đó không đủ dữ liệu để kết luận - đọc `ner_by_type.<loại>.n_gold`.
  Nguyên nhân gốc: 24 bài crawl lỗi, trong đó có CẢ 7 bài lễ hội.
- NER base 0.08 phần lớn là lỗi ĐỊNH DẠNG (4/8 mẫu trả về markdown thay vì JSON),
  không phải trích sai hết. Nói đúng như vậy, đừng để bảng tự nói quá.

### 4. Q&A hội đồng (5 phút)
Câu hỏi thường gặp + cách trả lời:

**"Tại sao không dùng GPT-4 thay vì Qwen?"**
> "Mục tiêu đồ án là fine-tune AI cho bài toán cụ thể, không phải gọi API. Qwen + LoRA cho phép customize format output (NER, citation, refusal) mà GPT-4 prompt-only khó đạt được độ ổn định. Ngoài ra chạy 100% local giúp demo reproducible, không phụ thuộc API key."

**"Tại sao dùng graph thay vì vector search?"**
> "Hai lý do đo được. Một: graph là thứ duy nhất biết câu hỏi có thuộc miền tri thức này hay không — 22 câu trong phạm vi đều neo được vào một node, 10 câu ngoài phạm vi không câu nào neo được, nên hệ từ chối đúng 10/10; coverage từ khoá một mình không phân tách được. Hai: graph bơm thêm ứng viên vào pool retrieval, nên câu gõ không dấu như 'cao lau la mon gi' vẫn lấy đúng bài dù điểm từ khoá thấp."

**"Sao không dùng Microsoft GraphRAG?"**
> "Đã cân nhắc và bỏ. Nó cần LLM extract entity: 8-12 giờ index trên corpus này, prompt mặc định bằng tiếng Anh chạy trên văn bản tiếng Việt sai nhiều, và entity do LLM sinh ra có thể bịa. Graph ở đây xây deterministic bằng khớp tên thực thể + mẫu 'danh từ loại + tên riêng' của tiếng Việt: 331 node / 563 edge, build hết 0.14 giây, và mọi node đều truy được về một chuỗi có thật trong văn bản."

**"Tại sao 4-bit base?"**
> "Để model 3B + LoRA vừa RAM và train nhanh trên M4 Pro. 4-bit quantization giảm RAM ~4× với loss chất lượng nhỏ cho downstream task. Kiến thức đến từ nguồn được truy xuất, nên không cần model to."

**"Mất bao lâu để train?"**
> "Sinh data vài giây. Train LoRA (r=16, 16 lớp cuối) 1000 iters trên M4 Pro: lần chạy rank-8 trước đo được ~2 giờ 05; cấu hình hiện tại giảm grad_accumulation 8→4 nên dự kiến ~1–1,5 giờ. Xây graph 0.14 giây, đo retrieval 1 giây — nên vòng lặp sửa retrieval rất nhanh, không phải index lại gì cả."

**"Chi phí toàn bộ dự án?"**
> "Dưới $1 (chỉ tính điện). Toàn bộ stack local, không tốn API."

## Checklist trước khi demo

- [ ] Laptop sạc đầy
- [ ] Internet tắt (để chứng minh chạy local)
- [ ] Terminal sẵn sàng
- [ ] Browser mở sẵn localhost:3000
- [ ] Slide mở sẵn
- [ ] 4 metric sẵn sàng show
