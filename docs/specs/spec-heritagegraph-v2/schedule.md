# Lịch 13 tuần còn lại (Mục 11.2)

Agile, vòng 1 tuần, demo giảng viên mỗi vòng. Hai quy tắc trình tự: **rủi ro trước** (3 hạng mục rủi ro cao nhất xếp sớm nhất) và **không tính năng nào được xây trên baseline chưa đo** (Tuần 2 trả hết nợ đo lường trước khi thêm năng lực mới).

| Tuần | Giai đoạn | Nội dung chính | Kết quả |
|---|---|---|---|
| 2 | Phạm vi + nợ đo lường | Chốt phạm vi v2.0 + 4 hạng mục loại bỏ bằng văn bản với giảng viên; sửa số liệu lạc hậu; **sửa lỗi rò rỉ truy hồi đã biết**; chạy lại mô hình gốc trên tập đánh giá hiện tại để so sánh trước/sau có giá trị; ghi checkpoint vào tệp báo cáo | Phạm vi chốt; tài liệu sửa; bộ kiểm thử truy hồi đạt; baseline so sánh được |
| 3 | Nền tảng | PostgreSQL + Docker Compose + migration; mô hình dữ liệu; đăng ký/đăng nhập argon2id + cookie HttpOnly; ghi sự kiện tương tác có đồng ý; Tailwind; mở rộng lược đồ phản hồi chat; **đo độ trễ lần đầu** | Tài khoản, lưu bền, log sự kiện, baseline độ trễ |
| 4 | Dữ liệu miền | Kho ngữ liệu → 80 tài liệu, ≥ 8/danh mục; soạn địa điểm + tọa độ, sự kiện + lịch + phần lễ/hội, cổ vật + niên đại/chất liệu/vị trí — mọi trường có nguồn; dựng lại đồ thị; sinh lại tập đánh giá; chạy lại đánh giá truy hồi | Kho cân bằng, 3 tập bản ghi, tập đánh giá làm mới — **hoàn thành F03, F14** |
| 5–6 | Cá nhân hóa | Hồ sơ có suy giảm; khởi tạo sở thích; độ gần đồ thị + độ gần hồ sơ + thưởng xuyên danh mục + xếp hạng đa dạng; endpoint gợi ý trả đường đi; log gợi ý; giao diện khám phá + chi tiết có dải nội dung liên quan | **Hoàn thành F05, F06, F07** |
| 7–8 | Tư vấn chủ động | Phân loại ý định 6 lớp + tập câu gán nhãn; sổ đăng ký ý định–thẻ; tích hợp thời tiết; tích hợp điểm quan tâm có đệm; luật danh mục chuẩn bị; API ngoài song song chồng bước sinh; suy giảm mềm | **Hoàn thành F09** |
| 9–10 | Giao diện thẻ + sơ đồ | Sổ đăng ký bộ kết xuất thẻ; bản đồ; 1 sơ đồ bảo tàng SVG + điểm nóng; tương tác vị trí cổ vật; rà soát tiếp cận chat + thẻ | **Hoàn thành F04, F10** |
| 11 | Hành trình + đệm | Hành trình nghiên cứu (cổ vật → bảo tàng → cùng thời kỳ → làng nghề) + hành trình tham dự (lễ hội → lịch → địa điểm → thời tiết → chuẩn bị → điểm quan sát → chỗ gửi xe); hấp thụ trượt tiến độ | Hai hành trình trình diễn hoàn chỉnh |
| 12–13 | Kiểm thử + đánh giá | pytest + Playwright + CI; phép khẳng định không-bịa-trường; toàn bộ chỉ số gồm ý định + precision gợi ý với người đánh giá thứ hai; nghiên cứu người dùng quy mô nhỏ; khắc phục độ trễ nếu NFR01 không đạt | Báo cáo kiểm thử + báo cáo đánh giá |
| 14–15 | Kết thúc | Tài liệu kiến trúc/API/lược đồ; rà soát riêng tư + đạo đức (đồng ý, tối giản dữ liệu, xuất/xóa); video + slide + hướng dẫn; báo cáo cuối | Bản chấp nhận cuối cùng |

Chú ý kiến trúc trình tự: xác thực (Tuần 3) xuất hiện **trước khi** lưu dữ liệu cá nhân; mở rộng kho ngữ liệu (Tuần 4) là **điều kiện** để bắt đầu cá nhân hóa (Tuần 5); đo độ trễ (Tuần 3) không đợi kiểm thử cuối kỳ (Tuần 12); Tuần 11 là đệm tường minh.
