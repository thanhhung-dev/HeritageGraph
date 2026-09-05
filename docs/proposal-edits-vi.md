# Đoạn sửa cho proposal-vi.md — Áp dụng bảng Tính năng cốt lõi mới

> Các đoạn dưới đây thay thế cho nội dung cũ tương ứng trong `docs/proposal-vi.md`. Bám sát bảng Tính năng cốt lõi đã chỉnh sửa (bỏ **F12 Khám phá đồ thị** và **F15 Xuất và xóa dữ liệu cá nhân**, đánh lại số F8→F11 và F13, F16→F17).

---

## 7.1. Tính năng cốt lõi (THAY THẾ TOÀN BỘ)

Tính năng được nhóm theo tác nhân: Quản trị/Biên tập F01–F06, Người dùng F07–F11 và F13, và các trao đổi AI nội bộ F16–F17. Mỗi luồng yêu cầu có một luồng phản hồi tương ứng, cho **15 cặp yêu cầu/phản hồi** trong sơ đồ ngữ cảnh (Mục 12.2).

| Mã | Tính năng | Tác nhân | Yêu cầu → Phản hồi |
| --- | --- | --- | --- |
| F01 | Đăng nhập | Quản trị | Yêu cầu đăng nhập → Phản hồi đăng nhập kèm thông tin phiên |
| F02 | Quản lý nội dung văn hóa | Quản trị | CRUD trên tài liệu, tên gọi khác, gán danh mục và vùng → Kết quả CRUD, kèm kích hoạt dựng lại đồ thị |
| F03 | Quản lý bản ghi có cấu trúc | Quản trị | CRUD trên địa điểm kèm tọa độ, sự kiện kèm lịch và các phần, cổ vật kèm niên đại, chất liệu và vị trí → Kết quả kiểm tra, từ chối mọi bản ghi có trường sự kiện thiếu nguồn |
| F04 | Rà soát kết quả trích xuất | Quản trị | Xác nhận hoặc sửa thực thể, quan hệ và tên gọi khác đã trích → Trạng thái cập nhật kèm bản ghi sổ kiểm toán |
| F05 | Bảng điều khiển quản trị | Quản trị | Yêu cầu bảng điều khiển → Dữ liệu tổng quan: số tài liệu theo danh mục, thống kê đồ thị, số trường thiếu nguồn, hàng chờ rà soát, chỉ số đánh giá mới nhất |
| F06 | Chạy bộ đánh giá | Quản trị | Yêu cầu đánh giá → Báo cáo chỉ số có ghi mô hình, checkpoint bộ điều hợp, phiên bản prompt, phiên bản kho ngữ liệu và cấu hình đánh giá |
| F07 | Đăng ký và quản lý tài khoản | Người dùng | Đăng ký hoặc cập nhật tài khoản → Xác nhận tài khoản |
| F08 | Xem và điều chỉnh hồ sơ sở thích | Người dùng | Yêu cầu xem hồ sơ sở thích đã suy ra, hoặc một điều chỉnh như bỏ hoặc tắt một sở thích suy ra sai → Hồ sơ sở thích hiện tại, trong đó mỗi mục hiển thị kèm hành vi đã sinh ra nó. Hồ sơ được dựng tự động từ chính các hành vi tìm kiếm, duyệt xem và tương tác của người dùng; không có bảng khai sở thích và không có bước thiết lập nào |
| F08 | Khám phá cá nhân hóa | Người dùng | Chọn một chủ đề, địa điểm, cổ vật, món ăn, nghề hay lễ hội → Danh sách gợi ý cá nhân hóa, mỗi mục kèm đường đi đồ thị biện minh cho nó, bao gồm các mục xuyên danh mục |
| F09 | Tìm kiếm lai theo sở thích | Người dùng | Truy vấn từ khóa hoặc ngôn ngữ tự nhiên → Kết quả xếp hạng từ Hybrid RAG hợp nhất với GraphRAG và xếp hạng lại theo hồ sơ sở thích |
| F10 | Truy vấn ngôn ngữ tự nhiên | Người dùng | Câu hỏi văn hóa tự do bằng tiếng Việt → Câu trả lời kèm trích nguồn, hoặc phát biểu tường minh rằng bằng chứng hiện có không đủ |
| F11 | Bối cảnh chủ động | Người dùng | Ý định phát hiện được ở F08a, F09 hoặc F10 → Các thẻ tư vấn có kiểu: lịch sự kiện, bản đồ địa điểm, thời tiết và danh mục cần chuẩn bị, điểm quan sát tốt nhất, chỗ gửi xe gần nhất, cổ vật tương đương, nghề liên quan — mỗi thẻ kèm nguồn gốc |
| F13 | Trang chi tiết thực thể | Người dùng | Chọn một thực thể hoặc tài liệu → Nội dung chi tiết kiểu Tapestry: ảnh lớn hoặc panorama bên trái, danh sách story bên phải có thể chọn, mỗi story kèm nội dung kể chuyện, audio, chip liên kết thực thể, dòng thời gian các năm liên quan, thực thể liên quan, địa điểm và sự kiện gắn với nó, và dải nội dung liên quan |
| F14 | Vị trí cổ vật | Người dùng | Câu hỏi về vị trí cổ vật → Sơ đồ bảo tàng với điểm nóng của cổ vật được làm nổi |
| F16 | Phân tích nội dung | Nội bộ | Văn bản tài liệu → Thực thể, quan hệ, đơn vị hành chính và năm đã trích kèm chuỗi bằng chứng, dùng để dựng đồ thị. Chạy khi F02 xảy ra |
| F17 | Sinh câu trả lời | Nội bộ | Bối cảnh đã tổ hợp và câu hỏi → Phần kể chuyện đã sinh kèm trích nguồn. Chạy khi F10 xảy ra |

**F16 và F17 là nội bộ và cục bộ.** F16 là trích xuất tất định, không gọi mô hình nào: một danh sách thực thể tuyển chọn, một từ vựng phân loại đóng và biểu thức chính quy, nên mọi tên trích ra là chuỗi con nguyên văn của nguồn và không thể bị bịa. F17 là một mô hình tinh chỉnh chạy cục bộ. Vì vậy không có dịch vụ AI bên ngoài nào trong kiến trúc, không có chi phí API, và văn bản kho ngữ liệu văn hóa không bao giờ rời khỏi máy.

**F08 là chức năng xem và điều chỉnh, không phải bước thiết lập.** Nền tảng có chủ đích **không có bảng khai sở thích khi bắt đầu**. Yêu cầu người truy cập lần đầu khai sở thích văn hóa thất bại vì ba lý do. Nó hỏi về những sở thích mà người dùng chưa hình thành — người chưa từng gặp điêu khắc Chăm thì không thể chọn nó từ một danh sách. Nó đi ngược lại chính tiền đề của nền tảng, rằng hệ thống *suy ra* điều người dùng quan tâm từ những gì họ thật sự làm, đúng như đã phát biểu ở Mục 4.2. Và nó áp một chi phí thiết lập trước khi bất kỳ giá trị nào được cung cấp, đó là lý do tiêu chuẩn khiến các bảng khai sở thích bị bỏ giữa chừng.

Vì vậy sở thích được suy ra hoàn toàn từ hành vi: người dùng tìm gì, mở thực thể nào, dừng lại bao lâu, nhấp, lưu hay bỏ qua thẻ nào. **Lần tìm kiếm đầu tiên của người dùng chính là tín hiệu** — một truy vấn về pho tượng Chăm lập tức làm điêu khắc, thời kỳ Chăm và bảo tàng đang giữ trở thành các sở thích đang hoạt động, không có bảng khai nào chen vào giữa. F08 tồn tại để việc suy ra không bị che kín: người dùng thấy được từng sở thích suy ra kèm hành động đã sinh ra nó, và có thể bỏ hoặc tắt bất kỳ mục nào sai. Cá nhân hóa nhờ đó vừa soi được vừa sửa được mà không bao giờ cần khai.

Khởi động nguội được xử lý bằng cấu trúc của hàm cho điểm thay vì bằng một bảng khai. Số hạng hạt giống của bộ gợi ý — độ gần đồ thị với đối tượng người dùng đang xem — hoạt động ngay từ tương tác đầu tiên, nên phiên đầu tiên đã hữu dụng. Số hạng hồ sơ đơn giản là không góp gì cho tới khi có hành vi để học, và tăng dần trọng số khi bằng chứng tích lũy.

**F13 là trang chi tiết theo pattern Tapestry.** Giao diện mô phỏng trải nghiệm của Tapestry by CyArk nhưng không yêu cầu mô hình 3D: một vùng hiển thị ảnh lớn hoặc panorama bên trái, danh sách các story dạng button bên phải, mỗi story tương ứng với một khía cạnh kể chuyện (lịch sử, kiến trúc, đời sống, lễ hội...), audio player tự động load khi chọn story, và bên dưới là nội dung kể chuyện kèm chip liên kết đến thực thể liên quan cùng trích nguồn. Khi model 3D hoặc panorama thật có sẵn trong tương lai, giao diện này chỉ cần thay viewer mà không phải thiết kế lại.

**F11 là tính năng không được phép bịa.** Các thẻ của nó được kết xuất từ bản ghi có kiểu và API công khai miễn phí, không bao giờ do sinh văn bản tạo ra. Yếu tố kích hoạt là nhận diện ý định thay vì một cú nhấp tường minh của người dùng — chính điều đó làm nó chủ động: hệ thống suy ra nhu cầu mà người dùng chưa nói.

**Phụ thuộc.** F08 đến F11 phụ thuộc đồ thị do F16 dựng. F08, F09 và F13 phụ thuộc thêm vào hồ sơ từ chính F08 (hồ sơ được F08 dựng nên và là đầu vào cho các tính năng này). F11 và F14 phụ thuộc thêm vào bản ghi có cấu trúc từ F03. Thẻ thời tiết và chỗ gửi xe của F11 suy giảm về trạng thái không-có-dữ-liệu tường minh khi không gọi được dịch vụ ngoài, và sự suy giảm đó chính là một ca kiểm thử.

**Bỏ các tính năng sau so với bản gốc.** F12 cũ (Khám phá đồ thị) và F15 cũ (Xuất và xóa dữ liệu cá nhân) được lược bỏ để giữ phạm vi dự án khả thi trong 15 tuần với một người phát triển: F12 vì quan hệ giữa các thực thể đã được diễn đạt đầy đủ qua chip liên kết trong story F13 và qua đường đi đồ thị trả về kèm mỗi gợi ý (xem chi tiết tại F08); F15 vì chức năng xuất và xóa dữ liệu cá nhân được chuyển vào bảng điều khiển tài khoản F07 dưới dạng hai nút hành động đơn giản mà không yêu cầu một tính năng độc lập.

---

## 7.2. Yêu cầu chức năng (THAY THẾ CÁC DÒNG LIÊN QUAN)

Xóa dòng FR24 cũ ("Người dùng có thể khám phá đồ thị tri thức"). Đánh lại số FR25–FR28 thành FR24–FR27.

| Mã | Yêu cầu | Tiêu chí chấp nhận |
| --- | --- | --- |
| FR24 | Người dùng có thể kiểm tra vì sao một đoạn được truy hồi | Vết truy hồi phơi ra hạt giống đồ thị, hạng theo từng kênh, độ gần đồ thị, các thành phần cho điểm, và liệu hệ thống có từ chối hay không |
| FR25 | Quản trị có thể xem sức khỏe kho ngữ liệu và đồ thị | Số tài liệu theo danh mục, thống kê đồ thị, số trường thiếu nguồn, hàng chờ rà soát và chỉ số mới nhất được hiển thị |
| FR26 | Hệ thống chạy được toàn bộ bộ đánh giá | Mọi chỉ số ở Mục 15.3 được tính và xuất ra báo cáo có ghi mô hình, checkpoint bộ điều hợp, phiên bản prompt, phiên bản kho ngữ liệu và cấu hình đánh giá |
| FR27 | Người dùng có thể xuất và xóa dữ liệu cá nhân của mình | Trong trang quản lý tài khoản F07, hồ sơ và lịch sử tương tác được trả về dưới dạng tệp máy đọc được và có thể xóa vĩnh viễn khi yêu cầu |

> **Ghi chú:** FR27 được giữ nhưng đưa vào phạm vi F07 (quản lý tài khoản) thay vì là một tính năng độc lập, vì thực chất nó là hai nút hành động trên giao diện tài khoản người dùng, không phải một luồng nghiệp vụ mới.

---

## 7.3. Yêu cầu phi chức năng (SỬA NFR08)

| Mã | Nhóm | Yêu cầu |
| --- | --- | --- |
| NFR08 | Giải thích được | Mọi gợi ý phơi ra **đường đi đồ thị dạng text hoặc JSON qua tooltip** khi người dùng di chuột vào, và mọi quyết định truy hồi kiểm tra được qua endpoint truy vết |

---

## 9. Đối tượng người dùng / Các bên liên quan (SỬA DÒNG "Nhà nghiên cứu")

| Nhóm | Nhu cầu | Nền tảng giúp thế nào |
| --- | --- | --- |
| Nhà nghiên cứu | Tìm quan hệ, đối chiếu nguồn, và phát hiện khoảng trống | Đồ thị tri thức kiểm tra được, vết truy hồi, từ điển tên gọi khác, nguồn gốc trên từng đỉnh, endpoint truy vết trả về JSON đầy đủ cấu trúc đồ thị cho đoạn quan tâm |

---

## 10. Công nghệ sử dụng (XÓA DÒNG "Trực quan hóa đồ thị")

Xóa dòng sau trong bảng Mục 10:

| Frontend | Trực quan hóa đồ thị | D3 với bố cục lực | Khám phá đồ thị con tương tác |

> **Ghi chú:** Không còn frontend cho trang khám phá đồ thị. Đường đi đồ thị được trả về qua endpoint truy vết dưới dạng JSON và hiển thị trong tooltip tại mỗi gợi ý hoặc kết quả truy hồi.

---

## 11.3. Kế hoạch phát triển (SỬA SPRINT 6)

| Sprint 6 — Giao diện | 10 | Sổ đăng ký bộ kết xuất thẻ; trang chi tiết thực thể kiểu Tapestry (ảnh lớn / panorama, danh sách story, audio player, chip liên kết); dòng thời gian; khung bản đồ; sơ đồ bảo tàng có điểm nóng cổ vật; bảng điều khiển và giao diện rà soát cho quản trị; rà soát khả năng tiếp cận | Giao diện thẻ tương tác hoàn chỉnh |

---

## 12.1. Mô tả kiến trúc (SỬA LỚP 1)

**1. Lớp trình bày.** Chat dạng thẻ, khám phá cá nhân hóa, trang chi tiết thực thể kiểu Tapestry (ảnh lớn / panorama, danh sách story, audio, chip liên kết), dòng thời gian, khung bản đồ, sơ đồ bảo tàng, khung trích nguồn, tooltip đường đi đồ thị cho gợi ý, trang xem hồ sơ sở thích, và giao diện quản lý nội dung và rà soát cho người quản trị.

---

## 12.2. Sơ đồ ngữ cảnh hệ thống (THAY THẾ ĐOẠN LIỆT KÊ F13–F15)

Trong sơ đồ Mức 0, thay các dòng liệt kê F13–F15 bằng:

```
│ F13 Yêu cầu chi tiết thực thể │
│     → Chi tiết Tapestry + story + liên quan       │
│ F14 Vị trí cổ vật              │
│     → Sơ đồ + điểm nóng                           │
│ F15 Xuất / xóa dữ liệu cá nhân│
│     → Tệp dữ liệu / xác nhận                      │
```

Và sửa câu cuối đoạn:

> Mỗi luồng yêu cầu có một luồng phản hồi tương ứng, tạo thành tổng cộng **15 cặp yêu cầu/phản hồi**, tương ứng F01–F14, F16–F17 ở Mục 7.1.

---

## 13. Mô hình dữ liệu (GIỮ NGUYÊN)

Không thay đổi. Đồ thị vẫn được dựng và sử dụng cho truy hồi, xếp hạng lại và giải thích gợi ý, chỉ không có giao diện trực quan hóa đồ thị.

---

## Tóm tắt thay đổi

| Mục | Thay đổi |
| --- | --- |
| 7.1 | Viết lại toàn bộ bảng 15 tính năng. Bỏ F12 (Khám phá đồ thị) và F15 (Xuất và xóa) độc lập; F15 được đưa vào F07 dưới dạng hai nút hành động. Đánh lại số F8–F11 và F13, F16–F17. |
| 7.2 | Xóa FR24 cũ; đánh lại số FR25–FR28 thành FR24–FR27; thêm FR27 cho xuất/xóa dữ liệu cá nhân (trong F07). |
| 7.3 | Sửa NFR08: dùng tooltip thay vì trang đồ thị. |
| 9 | Sửa dòng Nhà nghiên cứu: bỏ "xuất đồ thị con", giữ endpoint truy vết JSON. |
| 10 | Xóa dòng "Trực quan hóa đồ thị | D3". |
| 11.3 | Sửa Sprint 6: bỏ "khám phá đồ thị", bổ sung chi tiết Tapestry. |
| 12.1 | Lớp 1: bỏ "công cụ khám phá đồ thị", thêm tooltip đường đi đồ thị. |
| 12.2 | Sơ đồ: cập nhật mô tả F13–F15; sửa "15 cặp" và đánh lại số. |