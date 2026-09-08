# Catalog yêu cầu chức năng FR01–FR19 và phi chức năng NFR01–NFR15

## Yêu cầu chức năng

| Mã | Yêu cầu | Tiêu chí chấp nhận |
|---|---|---|
| FR01 | Đăng ký + xác thực | Mật khẩu băm argon2id; phiên qua cookie HttpOnly; endpoint bảo vệ từ chối yêu cầu chưa xác thực |
| FR02 | Thêm/sửa tài liệu kho ngữ liệu | Chuẩn hóa, tách đoạn kèm định vị nguồn, đồ thị dựng lại với đỉnh mới liên kết về nguồn |
| FR03 | Thêm bản ghi địa điểm/sự kiện/cổ vật | Chỉ lưu khi mọi trường có URL nguồn + câu nguồn; trường thiếu bị từ chối kèm lỗi ở mức trường |
| FR04 | Trích xuất thực thể + quan hệ | Khớp lược đồ 4 loại; mọi tên là chuỗi con nguyên văn của nguồn |
| FR05 | Dựng + cập nhật đồ thị | Đỉnh/cạnh tạo, gán kiểu, gán trọng số, liên kết về nguồn; thống kê báo cáo |
| FR06 | Hoàn tất khởi tạo sở thích | Chọn tối thiểu 3 danh mục + 3 mục cụ thể; hồ sơ lưu bền, sửa được |
| FR07 | Ghi nhận tương tác ngầm định | Xem/dừng/nhấp/lưu/bỏ qua kèm timestamp + đỉnh đích; trọng số có suy giảm |
| FR08 | Gợi ý cá nhân hóa | Mỗi mục kèm đường đi đồ thị đã sinh ra nó |
| FR09 | Gợi ý xuyên danh mục | Tối thiểu 1/5 gợi ý đầu thuộc danh mục khác khi hạt giống được nối trong đồ thị |
| FR10 | Gửi câu hỏi tiếng Việt văn bản | Giao diện chỉ nhận văn bản; câu trả lời chỉ từ bối cảnh đã truy hồi |
| FR11 | Trích nguồn hoặc phát biểu thiếu bằng chứng | Không câu khẳng định nào không có câu nguồn trích từ tài liệu đã truy hồi |
| FR12 | Phân loại ý định | Gán 1/6 lớp; lớp được ghi lại, kiểm tra được |
| FR13 | Thẻ tư vấn phù hợp ý định | Thẻ khớp sổ đăng ký ý định–bộ sinh; **mọi trường bằng đúng bản ghi nguồn hoặc phản hồi API, không trường nào do sinh ra** |
| FR14 | Lịch sự kiện + chi tiết địa điểm | Tên, loại lịch, ngày, địa điểm + tọa độ, đơn vị tổ chức, các phần lễ/hội |
| FR15 | Thời tiết + danh mục chuẩn bị | Dự báo từ API công khai theo tọa độ; danh mục sinh bằng luật tường minh trên dự báo |
| FR16 | Vị trí cổ vật trên sơ đồ | Điểm nóng cổ vật được làm nổi trên sơ đồ bảo tàng đang giữ |
| FR17 | Quản trị xác nhận/sửa trích xuất + bản ghi | Thay đổi + người thực hiện ghi sổ kiểm toán |
| FR18 | Chạy toàn bộ bộ đánh giá | Mọi chỉ số được tính, xuất tệp báo cáo ghi model, checkpoint, prompt version, corpus version, cấu hình |
| FR19 | Xuất + xóa dữ liệu cá nhân | Hồ sơ + lịch sử trả dạng tệp máy đọc được; xóa vĩnh viễn khi yêu cầu |

## Yêu cầu phi chức năng

| Mã | Nhóm | Yêu cầu |
|---|---|---|
| NFR01 | Hiệu năng | p95 đầu-cuối ≤ 8s câu hỏi tiêu chuẩn môi trường demo; đo liên tục từ Tuần 3 |
| NFR02 | Hiệu năng | Gợi ý + thẻ trong 2s không tính thời gian sinh; API ngoài chạy song song với bước sinh |
| NFR03 | Độ chính xác | recall@1 ≥ 95% trong phạm vi |
| NFR04 | Độ tin cậy | Trung thực trích nguồn ≥ 85%; độ phủ trích nguồn ≥ 90% |
| NFR05 | An toàn | Độ chính xác từ chối ≥ 90%; câu khẳng định bịa trên câu ngoài phạm vi là lỗi |
| NFR06 | An toàn | **Không một trường bịa nào trong thẻ tư vấn** — khẳng định tự động trên toàn bộ tập kiểm thử thẻ |
| NFR07 | Giải thích được | Mọi gợi ý phơi đường đi đồ thị đọc được; gợi ý không đường đi là lỗi |
| NFR08 | Khả dụng | Người dùng mới hoàn tất khởi tạo + đặt câu hỏi không cần hướng dẫn viết |
| NFR09 | Tiếp cận | Văn bản thay thế cho nội dung không phải chữ; tương phản đủ; bàn phím cho chat/thẻ; hội thoại đọc được bằng công nghệ trợ giúp |
| NFR10 | Bảo mật | Xác thực mọi endpoint dữ liệu cá nhân; kiểm tra đầu vào; không đường ghi không xác thực; không mở mạng công khai ở demo |
| NFR11 | Riêng tư | Ghi nhận có đồng ý thông báo; chỉ lưu dữ liệu bộ gợi ý cần; hỗ trợ xuất + xóa |
| NFR12 | Nguồn gốc | Mọi phát biểu thực tế truy về được nguồn: câu kho ngữ liệu, trường bản ghi kèm nguồn, hoặc API có tên kèm mốc thời gian lấy |
| NFR13 | Bảo trì | Nạp dữ liệu, đồ thị, truy hồi, sinh, gợi ý, tư vấn, giao diện là mô-đun giao diện tách biệt |
| NFR14 | Tái lập | Model id, checkpoint bộ điều hợp, prompt version, corpus version, thống kê đồ thị, cấu hình đánh giá ghi trong mọi tệp báo cáo |
| NFR15 | Mở rộng | Thêm vùng/danh mục/sự kiện/địa điểm/cổ vật không sửa mã; thêm loại thẻ chỉ cần đăng ký bộ sinh |
