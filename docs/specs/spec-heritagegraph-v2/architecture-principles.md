# Nguyên tắc kiến trúc và quản trị phạm vi

## Nguyên tắc kiến trúc trung tâm (Mục 4.4)

> **Mô hình ngôn ngữ chỉ viết phần kể chuyện di sản. Mọi phát biểu thực tế hoặc có cấu trúc — ngày, tọa độ, thời tiết, chỗ gửi xe, thuộc tính cổ vật, gợi ý — được kết xuất từ một bản ghi có kiểu mang theo nguồn gốc của chính nó, và không bao giờ đi qua bước sinh văn bản.**

Hai cách hiển nhiên đều bị loại có chủ ý: lọc cộng tác (không có nền người dùng, không giải thích được *vì sao*) và LLM đa dụng tự ứng biến phần bối cảnh (tái tạo đúng hiện tượng bịa đã đo được và loại bỏ — mô hình chịu bịa chỗ gửi xe cũng chịu bịa triều đại). Lớp 6 (điều phối AI) sinh văn bản kể chuyện; lớp 7 (cá nhân hóa + tư vấn) sinh đối tượng thẻ có kiểu. Đối tượng thẻ không bao giờ đi qua lớp 6.

## Bảy lớp kiến trúc (Mục 12.1) — 3 lớp đậm là mới ở v2.0

1. **Trình bày** — chat có thẻ, khám phá + chi tiết, khởi tạo sở thích, bản đồ, sơ đồ bảo tàng, khung trích nguồn, rà soát quản trị.
2. **Ứng dụng / API** — xác thực, chat, khám phá cá nhân hóa, tìm kiếm, gợi ý, tư vấn, kiểm tra đồ thị, quản lý nội dung + bản ghi, đánh giá.
3. **Nạp dữ liệu** — phân giải + tải nguồn, chuẩn hóa, tách đoạn kèm định vị nguồn, trích tên gọi khác.
4. **Xử lý tri thức** — trích xuất thực thể + năm tất định với từ vựng đóng, nhận diện đơn vị hành chính, dựng đồ thị cạnh có kiểu/trọng số/nguồn gốc.
5. **Lưu trữ** — tệp kho ngữ liệu, đồ thị trong RAM, PostgreSQL cho người dùng/hồ sơ/tương tác/địa điểm/sự kiện/cổ vật/điểm quan tâm/log gợi ý/sổ kiểm toán.
6. **Điều phối AI** — phân tích truy vấn (phạm vi, ý định, chủ thể vs giả định), truy hồi lai, lan truyền đồ thị, tổ hợp bối cảnh, ba cổng từ chối, sinh văn bản, kiểm tra trích nguồn.
7. **Cá nhân hóa + tư vấn** — hồ sơ có suy giảm, gợi ý theo đường đi + thưởng xuyên danh mục + đa dạng, phân loại ý định, sổ đăng ký ý định–bộ sinh thẻ + bộ điều hợp thời tiết/điểm quan tâm.

## Ba cổng từ chối (docs/architecture.md)

Truy vấn phải (1) neo được vào một đỉnh đồ thị đã biết; (2) tên riêng được gọi có bằng chứng hỗ trợ trong đoạn đã truy hồi; (3) độ phủ từ vựng vượt ngưỡng. Cổng nào không đạt → bối cảnh để rỗng → mô hình trả lời từ chối tường minh (hành vi được tinh chỉnh vào trọng số, không chỉ là câu điều kiện).

## Hai quyết định chệch có chủ ý so với GraphRAG tham chiếu

- **Không trích xuất LLM khi dựng đồ thị** — đồ thị tất định từ danh sách thực thể tuyển chọn + từ vựng đóng + regex; trích xuất LLM trên kho này ước lượng 8–12 giờ/lần (prompt tiếng Anh trên văn bản tiếng Việt, thực thể không có trong nguồn); tất định dựng 0,23s, mọi đỉnh truy về được chuỗi con nguyên văn.
- **Không vector DB, không Neo4j** — BM25 từ + BM25 n-gram không dấu hợp nhất RRF đạt recall@1 30/30 kể cả câu không dấu/tên gọi khác → không có khiếm khuyết đo được để thêm chỉ mục vector; đồ thị 510 đỉnh dựng lại trong RAM 0,23s → cơ sở dữ liệu đồ thị thêm phụ thuộc vận hành không thêm năng lực.

## Thay đổi phạm vi v1.0 → v2.0 (Mục 16)

**Thêm** (4 năng lực yêu cầu ở phản biện): cá nhân hóa + gợi ý xuyên miền (F05–F07, FR06–FR09, NFR07); AI tư vấn chủ động (F09, FR12–FR15, NFR06); tra cứu chi tiết sự kiện kèm thời gian/địa điểm/đơn vị/cách tổ chức (F03, F14); chatbot dạng thẻ thay tìm kiếm (F09, F10).

**Loại** (để giữ ngân sách 15 tuần): thư viện ảnh + luồng tải ảnh (thẻ vẫn hiển thị 1 ảnh tiêu biểu/định danh); câu chuyện nhiều ảnh với đường camera + mốc thời gian (bị thay chức năng bởi đường khám phá cá nhân hóa F06); nạp DOCX (không có nguồn DOCX nào đang dùng); chỉ mục vector riêng + mô hình embedding (không khiếm khuyết đo được để khắc phục); phụ thuộc API LLM/embedding ngoài (phân tích + sinh đều cục bộ); bảng điều khiển quản trị trình bày đầy đủ (giữ chức năng biên tập, thu gọn phạm vi trình bày).

## Thứ tự cắt cố định khi áp lực tiến độ (Mục 13.1)

Quyết trước để không ứng biến. Cắt theo thứ tự: (1) điểm nóng sơ đồ bảo tàng (giữ ảnh sơ đồ tĩnh); (2) điểm quan tâm cửa hàng + quà (giữ bãi xe + điểm quan sát); (3) giảm nghiên cứu người dùng 8 → 4 người; (4) thay giao diện quản trị bằng CLI + trang thống kê chỉ đọc; (5) giảm kho ngữ liệu 80 → 65 tài liệu nhưng giữ mức tối thiểu mỗi danh mục.

**Không bao giờ cắt:** ba cổng từ chối, trích nguồn bắt buộc, phép khẳng định không-bịa-trường, bộ đánh giá. Thiếu chúng thì chỉ là bản trình diễn không kiểm chứng được.

## Rủi ro lớn nhất và biện pháp (Mục 13, trích những cái cao)

- Phạm vi vượt 13 tuần → Mục 16 đánh đổi + chốt văn bản Tuần 2 + thứ tự cắt quyết trước.
- Mất cân bằng danh mục kho ngữ liệu → mở rộng 8/danh mục ở Tuần 4, điều kiện để bắt đầu Tuần 5.
- Bản ghi có cấu trúc soạn thủ công → giới hạn 20/50/35 + 1 sơ đồ, mọi trường có nguồn, dành trọn một tuần.
- Thẻ tư vấn hồi sinh bịa đặt → nguyên tắc kiến trúc + phép khẳng định NFR06 — cam kết an toàn trung tâm.
- Gợi ý không đo được với 1 người → 2 người đánh giá + đồng thuận; xuyên miền + đa dạng tính khách quan không cần phán đoán người.
- Độ trễ p95 vượt 8s → đo từ Tuần 3, chồng API ngoài lên bước sinh, giới hạn token, phát trực tiếp nếu cần.
- Dữ liệu cá nhân → đồng ý trước, tối giản dữ liệu, xuất/xóa FR19, xác thực trước khi lưu, rà soát riêng tư Tuần 14.
