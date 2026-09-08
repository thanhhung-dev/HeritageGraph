# Bảng 12 tính năng F01–F12

12 cặp yêu cầu/phản hồi trong sơ đồ ngữ cảnh Mức 0 (v1.0 có 10; F06 tách, F09/F10 mới). Tác nhân: Quản trị/Biên tập F01–F04, Người dùng F05–F10, nội bộ F11–F12.

| Mã | Tính năng | Tác nhân | Mô tả | Trạng thái |
|---|---|---|---|---|
| F01 | Yêu cầu đăng nhập | Quản trị | Xác thực; trả phản hồi đăng nhập + thông tin phiên | Mới |
| F02 | Yêu cầu quản lý nội dung văn hóa | Quản trị | CRUD tài liệu, tên gọi khác, gán danh mục/vùng; kích hoạt dựng lại đồ thị | Mới |
| F03 | Yêu cầu quản lý bản ghi có cấu trúc | Quản trị | CRUD 3 tập bản ghi (địa điểm/sự kiện/cổ vật); từ chối mọi bản ghi có trường không nguồn | Mới |
| F04 | Yêu cầu bảng điều khiển quản trị | Quản trị | Sức khỏe kho ngữ liệu + đồ thị: số tài liệu theo danh mục, thống kê đồ thị, số trường thiếu nguồn, chỉ số mới nhất | Mới |
| F05 | Khởi tạo / cập nhật hồ sơ sở thích | Người dùng | Chọn danh mục + mục cụ thể quan tâm, sửa hồ sơ; giải quyết khởi động nguội | Mới |
| F06 | Yêu cầu khám phá cá nhân hóa | Người dùng | Mở chủ đề/địa điểm/cổ vật/món ăn/lễ hội → danh sách gợi ý kèm đường đi đồ thị giải thích từng mục, gồm xuyên danh mục | Mới |
| F07 | Truy vấn tìm kiếm theo sở thích | Người dùng | Tìm từ khóa → kết quả xếp hạng lại theo hồ sơ | Mới |
| F08 | Truy vấn ngôn ngữ tự nhiên (văn bản) | Người dùng | Câu hỏi tự do tiếng Việt → trả lời trích nguồn hoặc phát biểu thiếu bằng chứng | **Đã xây** |
| F09 | Yêu cầu bối cảnh chủ động | Người dùng | Kích hoạt bởi ý định ở F06/F08 → thẻ tư vấn có kiểu (lịch, bản đồ, thời tiết + chuẩn bị, điểm quan sát, chỗ gửi xe, cổ vật tương đương, nghề liên quan), mỗi thẻ mang nguồn gốc | Mới |
| F10 | Yêu cầu vị trí cổ vật | Người dùng | Hỏi cổ vật trưng bày ở đâu → sơ đồ bảo tàng với điểm nóng làm nổi | Mới |
| F11 | Yêu cầu phân tích nội dung | Nội bộ | Gửi văn bản tài liệu → thực thể + quan hệ trích ra để dựng đồ thị; chạy khi F02 xảy ra | **Đã xây** (tất định, cục bộ) |
| F12 | Yêu cầu sinh câu trả lời | Nội bộ | Gửi bối cảnh tổ hợp + câu hỏi → mô hình tinh chỉnh cục bộ sinh phần kể chuyện; chạy khi F08 xảy ra | **Đã xây** (mô hình cục bộ) |

Phụ thuộc: F06, F07, F08, F09, F10 phụ thuộc đồ thị của F11; F06, F07 phụ thuộc thêm hồ sơ của F05; F09 phụ thuộc thêm bản ghi của F03. Thẻ thời tiết/chỗ gửi xe của F09 suy giảm mềm khi API ngoài không gọi được — chính sự suy giảm là ca kiểm thử.
