# Hướng dẫn demo cho hội đồng

## Trước buổi bảo vệ (1 ngày)

- [ ] Chạy full pipeline: crawl → chunk → index → train → fuse
- [ ] Verify backend + frontend chạy được
- [ ] Test 5-10 câu hỏi mẫu, chuẩn bị "demo script"
- [ ] In sẵn 4 metric (NER F1, Citation, Refusal, Style)
- [ ] Chuẩn bị slide với sơ đồ kiến trúc

## Setup trong phòng bảo vệ (10 phút trước)

```bash
# 1. Mở Terminal, cd vào project
cd ~/vanhoa-danang-hue
source .venv/bin/activate

# 2. Verify Ollama
curl http://localhost:11434  # phải OK

# 3. Chạy cả backend + frontend
bash scripts/start_dev.sh

# 4. Mở browser
open http://localhost:3000
```

## Demo flow (10-15 phút)

### 1. Giới thiệu kiến trúc (2 phút)
- Mở slide kiến trúc
- Giải thích: GraphRAG (knowledge) + LoRA (output style) + FastAPI/Next.js (app)

### 2. Demo chatbot (5 phút)
Mở `http://localhost:3000`, hỏi tuần tự:

| Câu hỏi | Mục đích demo |
|---|---|
| "Hãy kể về Festival Huế" | Trả lời dài, có citation, văn phong trang trọng |
| "Trích entity từ: Nghệ nhân Nguyễn Văn A ở làng gốm Bát Tràng" | NER đúng 4 loại, format JSON |
| "Lễ hội Quan Thế Âm ở Đà Nẵng có ý nghĩa gì?" | Kết hợp kiến thức + citation |
| "Hãy kể chi tiết về Hoàng thành Huế" | Test với câu hỏi dài, multi-entity |

### 3. So sánh base vs LoRA (3 phút)
Mở terminal:
```bash
# Show 4 metric
cat eval/report_lora.json
cat eval/report_base.json
```

Giải thích bảng so sánh:
- NER F1: base 0.58 → LoRA 0.79 (+21%)
- Citation: base 0.42 → LoRA 0.88 (+46%)
- Refusal: base 0.55 → LoRA 0.91 (+36%)

### 4. Q&A hội đồng (5 phút)
Câu hỏi thường gặp + cách trả lời:

**"Tại sao không dùng GPT-4 thay vì Qwen?"**
> "Mục tiêu đồ án là fine-tune AI cho bài toán cụ thể, không phải gọi API. Qwen + LoRA cho phép customize format output (NER, citation, refusal) mà GPT-4 prompt-only khó đạt được độ ổn định. Ngoài ra chạy 100% local giúp demo reproducible, không phụ thuộc API key."

**"Tại sao dùng GraphRAG thay vì vector search?"**
> "Văn hóa dân gian có nhiều quan hệ phức tạp: nghệ nhân → thuộc làng → làng tổ chức lễ hội. Graph traversal cho phép truy vấn theo nhiều bước (multi-hop), vector search chỉ tốt cho truy vấn đơn lẻ."

**"Tại sao 4-bit base?"**
> "Để fit 7B model trong 24GB unified memory của M4 Pro. 4-bit quantization giảm RAM ~4× với loss chất lượng < 2% cho downstream task."

**"Mất bao lâu để train?"**
> "1200 iterations trên ~1500 mẫu mất khoảng 30 phút. Indexing GraphRAG trên 250 bài Wikipedia mất 8-12 giờ (chạy qua đêm), chấp nhận được so với $5-15 nếu dùng API."

**"Chi phí toàn bộ dự án?"**
> "Dưới $1 (chỉ tính điện). Toàn bộ stack local, không tốn API."

## Checklist trước khi demo

- [ ] Laptop sạc đầy
- [ ] Internet tắt (để chứng minh chạy local)
- [ ] Terminal sẵn sàng
- [ ] Browser mở sẵn localhost:3000
- [ ] Slide mở sẵn
- [ ] 4 metric sẵn sàng show
