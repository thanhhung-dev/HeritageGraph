# 4 metric đánh giá

## Mục tiêu đo lường

| Metric | Mục đích | Loại |
|---|---|---|
| **NER macro-F1** | Đánh giá khả năng trích entity đúng 4 loại | Tự động |
| **Citation precision** | Đánh giá model trích dẫn đúng nguồn | Tự động |
| **Refusal accuracy** | Đánh giá model từ chối đúng khi ngoài nguồn | Tự động |
| **Style score** | Đánh giá văn phong kể chuyện, trang trọng | Bán tự động (chấm tay) |

## 1. NER macro-F1

**Công thức:**
```
F1_macro = (F1_người + F1_địa_điểm + F1_sự_kiện + F1_thời_gian) / 4
F1_type = 2 * precision * recall / (precision + recall)
precision = |pred ∩ gold| / |pred|
recall    = |pred ∩ gold| / |gold|
```

**Tại sao quan trọng:** Đây là metric chính cho mục tiêu 1 (NER domain). Trước/sau LoRA phải có sự khác biệt rõ rệt.

**Kỳ vọng:**
- Qwen2.5-7B base: F1 ~ 0.50-0.65
- Qwen2.5-7B + LoRA: F1 ~ 0.75-0.85

## 2. Citation precision

**Công thức:**
```
precision = |citation có trong source| / |tổng citation model đưa ra|
```

**Pattern tìm citation trong output:**
- `[Nguồn: ...]`
- `(Nguồn: ...)`
- `Nguồn: ...`

**Match với source:** substring match (case-insensitive).

**Tại sao quan trọng:** Đảm bảo model không bịa citation. Mục tiêu 4 của đồ án.

**Kỳ vọng:** 0.85-0.95 (sau LoRA), 0.30-0.50 (base).

## 3. Refusal accuracy

**Công thức:**
```
accuracy = |đúng refusal| / |tổng câu hỏi|
```

**Marker từ chối (case-insensitive):**
- "không tìm thấy"
- "không có thông tin"
- "ngoài phạm vi"
- "không được cung cấp"

**Tại sao quan trọng:** Tránh model bịa. Đặc biệt với văn hóa dân gian — nhiều thông tin nhạy cảm, dễ bịa.

**Kỳ vọng:** 0.85-0.95 (sau LoRA), 0.40-0.60 (base).

## 4. Style score

**Thang:** 1-5 cho mỗi mẫu, tiêu chí:
- **5**: Văn phong trang trọng, kể chuyện cuốn hút, có chi tiết văn hóa
- **4**: Trang trọng, đủ ý
- **3**: Bình thường
- **2**: Khô khan, liệt kê
- **1**: Sai chính tả, câu rời rạc

**Quy trình:** Chấm tay 30-50 mẫu, lấy trung bình.

**Tại sao quan trọng:** UI là "story panel" — văn phong là yếu tố cốt lõi.

## So sánh base vs LoRA (format bảng cho báo cáo)

| Metric | Qwen2.5-7B base | Qwen2.5-7B + LoRA | Δ |
|---|---|---|---|
| NER macro-F1 | 0.58 | 0.79 | +0.21 |
| Citation precision | 0.42 | 0.88 | +0.46 |
| Refusal accuracy | 0.55 | 0.91 | +0.36 |
| Style score (1-5) | 2.8 | 4.2 | +1.4 |

## Chạy eval

```bash
# 1. Tạo gold set template
python training/make_gold_template.py

# 2. Gán nhãn tay (mở eval/gold.jsonl, thêm ~50-100 mẫu)
nano eval/gold.jsonl

# 3. Đánh giá model LoRA
python training/score_gold.py \
  --model models/qwen-7b-fused \
  --gold eval/gold.jsonl \
  --out eval/report_lora.json

# 4. Đánh giá model base (để so sánh)
python training/score_gold.py \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --gold eval/gold.jsonl \
  --out eval/report_base.json

# 5. So sánh 2 file
diff eval/report_base.json eval/report_lora.json
```
