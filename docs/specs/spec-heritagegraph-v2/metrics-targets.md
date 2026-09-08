# Bảng chỉ số mục tiêu và baseline

Dự án thành công khi hai hành trình trình diễn (Mục 12.4) hoàn tất đầu-cuối cho người dùng đã xác thực có hồ sơ, và các chỉ số dưới đây được đo và báo cáo — bất kể đạt hay không. Mục tiêu không đạt nhưng được đo + giải thích là kết quả chấp nhận được; mục tiêu không được đo thì không.

| Chỉ số | Mục tiêu | Baseline (08/09/2026) |
|---|---|---|
| recall@1 truy hồi, trong phạm vi | ≥ 95% | 68/70 |
| Từ chối ngoài phạm vi | ≥ 95% | 31/38 |
| Micro-F1 trích xuất thực thể | ≥ 0,75 | 0,786 (nhãn máy điền trước, chờ rà soát) |
| Độ trung thực trích nguồn | ≥ 85% | 0,704 (precision 0,95 khi có trích) |
| Độ phủ trích nguồn trên câu trả lời được | ≥ 90% | 0,741 |
| Độ chính xác từ chối | ≥ 90% | 0,917 |
| Macro-F1 phân loại ý định | ≥ 85% trên 100 câu gán nhãn | Mới |
| Precision@5 gợi ý | ≥ 70%, 2 người đánh giá, báo cáo độ đồng thuận | Mới |
| nDCG@5 gợi ý | Báo cáo, chưa đặt mục tiêu ở lần đo đầu | Mới |
| Tỷ lệ gợi ý xuyên miền | ≥ 30% trong 5 mục đầu thuộc danh mục khác | Mới |
| Độ đúng trường của thẻ tư vấn | **100% — không trường bịa, khẳng định tự động** | Mới |
| Độ trễ đầu-cuối p95 | ≤ 8 giây | Chưa đo |
| Khả dụng | SUS 6–8 người, báo cáo định tính | Mới |

## Baseline hiện trạng đã đo (Mục 12.5)

| Thành phần | Hiện trạng |
|---|---|
| Kho ngữ liệu | 45 tài liệu / 349 đoạn; 30 Huế / 15 Đà Nẵng; di tích 22, ẩm thực 9, danh thắng 6, nghệ thuật 4, lễ hội 2, làng nghề 2 |
| Đồ thị tri thức | 510 đỉnh (235 thực thể, 222 năm, 45 tài liệu, 6 danh mục, 2 vùng) / 1135 cạnh (443 năm, 242 nhắc đến, 123 liên quan, 98 hành chính, 92 vùng, 92 danh mục, 45 nói-về); 1 thành phần liên thông; 0 tài liệu cô lập; dựng 0,23s |
| Truy hồi | Trong phạm vi 68/70; paraphrase 9/39; bằng chứng 34/34; phường/xã 18/20; ngoài phạm vi 31/38 |
| Mô hình | Qwen2.5-3B 4-bit + LoRA rank 16/16 lớp; checkpoint bước 200 (valid loss 0,414) thay vì bước 720 (0,473) — valid loss tăng dần từ ~bước 250 |
| Chất lượng trả lời | Micro-F1 0,786 (gốc 0,104); trung thực trích nguồn 0,704; độ phủ 0,741; chính xác từ chối 0,917 (gốc 0,375) |
| Chưa đo | Độ trễ p95; điểm văn phong; mọi chỉ số 3 lớp năng lực mới |
| Chưa xây | Cơ sở dữ liệu, xác thực, hồ sơ sở thích, bộ gợi ý, phân loại ý định, thẻ tư vấn, bản ghi có cấu trúc, sơ đồ bảo tàng, framework kiểm thử, CI |

## Hạn chế đã biết cần nêu trong báo cáo cuối (Mục 14.4)

- Chỉ một cặp địa bàn (Huế, Đà Nẵng) — cơ chế gợi ý độc lập vùng nhưng kho ngữ liệu không chứa Nam Bộ; bảng tương đương cấu trúc trong Mục 16.3.
- Quy mô đánh giá nhỏ: hàng chục phán đoán, không phải hàng nghìn người dùng; báo cáo định tính kèm đồng thuận.
- Nhãn thực thể máy điền trước; không nhãn vàng cho loại sự kiện — "bốn loại" thực chất là ba loại.
- Không chỉ mục vector: truy vấn thuần diễn giải lại không chia sẻ neo từ vựng/đồ thị sẽ thất bại (cổng từ chối làm thất bại an toàn nhưng vẫn là hạn chế recall).
- Trích xuất tất định = không quan hệ ngữ nghĩa: đồ thị biết hai thực thể đồng xuất hiện, không biết cái này xây nên cái kia — lời giải thích gợi ý mang tính cấu trúc, không nhân quả.
- Đồ thị trong RAM + mô hình một máy: hợp lý ở kích thước hiện tại, không phải giải pháp tổng quát.
- Bảng âm lịch thủ công chỉ phủ sự kiện thử nghiệm + khoảng thời gian trình diễn.
- Chất lượng điểm quan tâm phụ thuộc cộng đồng OSM, không đồng đều.
