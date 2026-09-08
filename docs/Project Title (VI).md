**International School**

**CAPSTONE PROJECT 1**

CMU-SE 450

**TÀI LIỆU DỰ ÁN**

**Phiên bản 2.0 — Chỉnh sửa: 05/09/2026** (v1.0: 21/08/2026)

**Trợ lý GraphRAG cá nhân hóa cho việc khám phá, tìm hiểu và lên kế hoạch trải nghiệm văn hóa địa phương**

**Thực hiện bởi: C1SE.50**

Dương Thanh Hùng – 29219043370

**Phê duyệt bởi:**

**ThS. Nguyễn Thị Thanh Tâm**

**Đại diện Hội đồng phản biện đề cương:**

Họ tên: Chữ ký: Ngày:

**Giảng viên hướng dẫn Capstone Project 1:**

Họ tên: **ThS. Nguyễn Thị Thanh Tâm** Chữ ký: Ngày:

**Đà Nẵng 9, 2026**

---

**THÔNG TIN DỰ ÁN**

| Trường | Giá trị |
| --- | --- |
| Tên dự án | Trợ lý GraphRAG cá nhân hóa cho việc khám phá, tìm hiểu và lên kế hoạch trải nghiệm văn hóa địa phương |
| Tên viết tắt | CulturalMemoryGraph / CMG — tên sản phẩm **HeritageGraph** |
| Thời gian thực hiện | 27/08/2026 – 06/12/2026 (15 tuần; còn 13 tuần tính từ lần chỉnh sửa này) |
| Địa bàn / chủ đề thử nghiệm | **Huế và Đà Nẵng** — di tích, ẩm thực, nghệ thuật diễn xướng, làng nghề, lễ hội, cổ vật bảo tàng |
| Trạng thái | Đề cương dự án capstone, bản chỉnh sửa 2.0 sau phản biện của giảng viên hướng dẫn |

**Lưu ý:** *Đây là bản chỉnh sửa phạm vi, không phải dự án mới. Bộ máy truy hồi, đồ thị tri thức, mô hình đã tinh chỉnh và hệ thống đánh giá nêu ở Mục 12.5 đã được xây dựng và đo đạc. Các Mục 6, 7, 11 và 14 được viết lại để bổ sung bốn năng lực mà giảng viên hướng dẫn yêu cầu; Mục 16 ghi rõ những gì được thêm và những gì bị loại bỏ để giữ nguyên ngân sách 15 tuần.*

---

## 1. Tên dự án

**Trợ lý GraphRAG cá nhân hóa cho việc khám phá, tìm hiểu và lên kế hoạch trải nghiệm văn hóa địa phương**

Mỗi thành phần của tên tương ứng với một năng lực đo được, không phải một khẩu hiệu:

- **Cá nhân hóa** — hệ thống xây dựng hồ sơ sở thích riêng cho từng người dùng từ lựa chọn tường minh khi khởi tạo và từ hành vi tương tác, rồi dùng hồ sơ đó để xếp hạng và mở rộng nội dung hiển thị. Hai người dùng nhập cùng một truy vấn sẽ nhận về hai tập kết quả khác nhau, mỗi kết quả đều có lý do riêng. Đây là điểm khác biệt chính được xác định trong buổi phản biện.
- **GraphRAG** — truy hồi được neo trên một đồ thị tri thức gồm thực thể, địa điểm, đơn vị hành chính, thời gian và tài liệu, không chỉ dựa vào khớp từ khóa. Chính đồ thị làm cho gợi ý xuyên miền trở nên khả thi: mỗi gợi ý đi theo một cạnh thật, có thể kiểm tra được.
- **Khám phá, tìm hiểu** — hỏi đáp tiếng Việt có trích nguồn, và từ chối tường minh khi bằng chứng không đủ.
- **Lên kế hoạch** — hệ thống không dừng ở việc giải thích một đối tượng văn hóa. Khi phát hiện người dùng đang chuẩn bị *tham dự* một hoạt động, hệ thống chủ động cung cấp bối cảnh thực tế cần thiết để thật sự đi được: lịch, địa điểm, cần mang gì, đứng ở đâu, gửi xe ở đâu.

Tên viết tắt vẫn là CulturalMemoryGraph (CMG); tên sản phẩm vẫn là HeritageGraph.

Tên được thay đổi so với v1.0 (*"An AI-Powered Platform for Preserving and Storytelling Local Cultural Memories Using GraphRAG"*) vì v1.0 gọi tên sản phẩm vật lý (một kho lưu trữ kể chuyện), trong khi đóng góp thực tế của dự án là hành vi: hướng dẫn văn hóa cá nhân hóa, giải thích được bằng đồ thị, và chủ động về bối cảnh.

## 2. Thành viên nhóm

| Họ tên | Mã sinh viên | Vai trò | Email |
| --- | --- | --- | --- |
| Dương Thanh Hùng | 29219043370 | Toàn bộ vai trò — phân tích yêu cầu, AI/GraphRAG, kỹ thuật dữ liệu, frontend, kiểm thử, tài liệu | *[điền trước khi nộp]* |

Đây là dự án một thành viên. Tất cả vai trò trong mẫu chuẩn được gộp thành một tập trách nhiệm: phân tích yêu cầu, phát triển, kiểm thử, quản lý dữ liệu, đánh giá và tài liệu. Giảng viên hướng dẫn định hướng, phản hồi và rà soát tiến độ. Vì không có người rà soát chéo bên trong nhóm, Mục 11.3 định nghĩa một bước rà soát bên ngoài cho hai chỗ mà một tác giả duy nhất về bản chất là không đáng tin: rà soát nhãn vàng và đánh giá độ liên quan của gợi ý.

## 3. Giảng viên hướng dẫn

| Họ tên | Học vị / Đơn vị | Vai trò | Email |
| --- | --- | --- | --- |
| ThS. Nguyễn Thị Thanh Tâm | International School | Giảng viên hướng dẫn | *[điền trước khi nộp]* |
| *[Cố vấn chuyên môn, nếu có]* | Bảo tàng / trung tâm văn hóa | Cố vấn chuyên môn — rà soát nội dung di sản | *[điền]* |

Với nội dung văn hóa, dự án cần thêm một đầu mối chuyên môn có hiểu biết địa phương — nhân viên Bảo tàng Điêu khắc Chăm hoặc Bảo tàng Cổ vật Cung đình Huế, đại diện Trung tâm Bảo tồn Di tích Cố đô Huế, hoặc giáo viên lịch sử — để rà soát các bản ghi lễ hội và cổ vật có cấu trúc được bổ sung ở bản chỉnh sửa này (Mục 7.1, F03).

## 4. Phát biểu vấn đề

### 4.1. Bối cảnh

Tư liệu văn hóa về Huế và Đà Nẵng thì nhiều, nhưng phẳng về mặt cấu trúc. Bài bách khoa, kỷ yếu lễ hội, nhãn hiện vật bảo tàng, địa chí và trang du lịch — mỗi nguồn mô tả một đối tượng tại một thời điểm. Người đọc bắt đầu từ một điểm quan tâm — một loại hình diễn xướng, một món ăn, một pho tượng, một lễ hội — chỉ nhận được đúng một bài viết, rồi phải tự mình tìm ra phần văn hóa liên quan.

Hai thất bại tách biệt sinh ra từ đó, và đây chính là hai thất bại dự án này giải quyết.

**Thứ nhất, việc khám phá không được cá nhân hóa.** Công cụ tìm kiếm và cổng thông tin di sản trả về cùng một danh sách xếp hạng cho mọi người. Quan tâm đến nhã nhạc cung đình Huế và quan tâm đến điêu khắc đá Chăm đều cho ra cùng một khối "liên kết liên quan" chung chung, vì độ liên quan được tính từ độ tương đồng văn bản hoặc từ biên tập viên, không tính từ người dùng. Nhưng văn hóa lại chính là miền mà sở thích vừa rất riêng vừa cắt ngang nhiều lĩnh vực: người bị hút vào một loại hình diễn xướng truyền thống thường cũng mở lòng với trang phục, nhạc cụ, không gian diễn, làng nghề làm đạo cụ, và lễ hội nơi nó được trình diễn — nhưng những thứ đó nằm ở các danh mục khác nhau, các bài viết khác nhau, nên không công cụ nào nối chúng lại cho đúng người đó.

**Thứ hai, việc hiểu không dẫn tới hành động được.** Các hệ thống thông tin văn hóa hiện có trả lời "cái này là gì?" rồi dừng. Nhu cầu thật của người dùng thường ở bước tiếp theo và thường không được nói ra. Người đọc về một cổ vật ngầm muốn biết bảo tàng nào đang giữ nó, ở đó còn gì cùng thời kỳ, và có món tương tự hay bản mô phỏng nào để xem hoặc mua. Người đọc về một lễ hội ngầm muốn biết năm nay diễn ra khi nào, đứng ở đâu để xem, hôm đó có mưa không, gửi xe ở đâu. Mọi câu hỏi đó đều trả lời được từ dữ liệu, và không câu nào được một kho ngữ liệu văn hóa đơn thuần trả lời.

### 4.2. Vấn đề cốt lõi

Dự án giải quyết **sự thiếu vắng một hệ thống thông tin văn hóa biết thích ứng với từng người dùng và biết đoán trước nhu cầu thực tế nằm phía sau một truy vấn văn hóa — mà vẫn giữ được tính kiểm chứng.**

Cụm cuối cùng là thứ làm bài toán khó, chứ không chỉ là chưa ai làm. Hai cách hiển nhiên để thêm cá nhân hóa và chủ động đều thất bại:

- **Lọc cộng tác** (recommender thương mại chuẩn) đòi hỏi một lượng người dùng lớn mà dự án này sẽ không bao giờ có, và cho ra gợi ý không giải thích được — nó có thể nói *rằng* hai thứ liên quan nhưng không bao giờ nói *vì sao*. Trong bối cảnh di sản và giáo dục, đó là một lỗi, không phải một khiếm khuyết hình thức.
- **Để một mô hình ngôn ngữ đa dụng tự ứng biến** phần bối cảnh bổ sung sẽ tái tạo đúng cái lỗi mà dự án đã đo được và đã loại bỏ. Một mô hình sẵn sàng "nhiệt tình" bịa ra chỗ gửi xe hay giá vé cũng là mô hình sẽ bịa ra một triều đại.

Bài toán vì vậy là làm cho hệ thống cá nhân hóa và chủ động **mà không** phải mua lấy một trong hai thất bại đó: gợi ý phải giải thích được từ cấu trúc đồ thị, và bối cảnh thực tế phải là dữ liệu có kiểu, có nguồn, không phải văn bản sinh ra.

Các chatbot đa dụng không giải được việc này. Không có kho ngữ liệu địa phương cụ thể, mô hình lẫn tên riêng tiếng Việt, trộn tỉnh thành, và phát biểu những thông tin không xuất hiện ở nguồn nào. Retrieval-Augmented Generation xử lý điều này bằng cách neo phần sinh vào bộ nhớ ngoài được truy hồi [1]; GraphRAG mở rộng thêm bằng cách kết hợp trích xuất văn bản, phân tích mạng và tóm tắt bằng LLM trên một cấu trúc đồ thị [2], [3]. Dự án này dùng đồ thị cho một mục đích thứ hai ngoài việc neo bằng chứng: làm nền suy luận cho gợi ý xuyên miền được cá nhân hóa.

### 4.3. Tầm quan trọng của vấn đề

UNESCO ghi nhận rằng công nghệ số có thể mở rộng khả năng tiếp cận văn hóa và hỗ trợ tư liệu hóa, bảo vệ, quảng bá và kiểm kê di sản [4]. Tuy nhiên, tiếp cận không chỉ là có sẵn — nó còn là liên quan và dùng được. Một kho ngữ liệu không ai đi qua thì không tiếp cận được theo bất kỳ nghĩa có thực nào.

Điều hướng cá nhân hóa và giải thích được đặc biệt quan trọng với việc trao truyền văn hóa: nó biến một điểm tò mò đơn lẻ thành một đường đi qua các di sản liên quan, và đó chính là cách hiểu biết văn hóa thật sự tích lũy. Còn hỗ trợ lên kế hoạch đúng đắn thì quan trọng vì đó là bước mà quan tâm văn hóa trở thành tham dự văn hóa — khác biệt giữa đọc về một lễ hội và đi dự lễ hội đó.

### 4.4. Hướng giải quyết đề xuất

Hệ thống được xây thành ba lớp trên một nền tri thức đã được kiểm chứng.

1. **Lớp trả lời có căn cứ** (đã xây và đã đo): truy hồi neo trên đồ thị, mô hình tiếng Việt tinh chỉnh theo miền, trích nguồn ở mức câu là bắt buộc, và ba cổng từ chối mang tính cấu trúc.
2. **Lớp cá nhân hóa** (mới): hồ sơ sở thích, và một bộ gợi ý cho điểm ứng viên theo độ gần đồ thị với chủ đề đang xem, độ gần đồ thị với hồ sơ, và một phần thưởng tường minh cho ứng viên thuộc danh mục văn hóa *khác* nhưng vẫn được nối bởi một đường đi thật. Mỗi gợi ý trả về kèm đường đi đã sinh ra nó.
3. **Lớp tư vấn chủ động** (mới): nhận diện ý định của truy vấn, rồi một sổ đăng ký ánh xạ ý định sang các khối bối cảnh có kiểu — lịch, địa điểm, thời tiết, danh mục cần chuẩn bị, điểm quan sát, chỗ gửi xe, cổ vật tương đương, nghề liên quan.

Biên giới giữa các lớp được bảo đảm bởi một nguyên tắc kiến trúc duy nhất, nêu ở đây vì đó là cam kết thiết kế chính của dự án và được tham chiếu suốt tài liệu này:

> **Mô hình ngôn ngữ chỉ viết phần kể chuyện di sản. Mọi phát biểu thực tế hoặc có cấu trúc — ngày, tọa độ, thời tiết, chỗ gửi xe, thuộc tính cổ vật, gợi ý — được kết xuất từ một bản ghi có kiểu mang theo nguồn gốc của chính nó, và không bao giờ đi qua bước sinh văn bản.**

Nguyên tắc này giữ nguyên độ tin cậy đã đo được của lớp trả lời trong khi thêm những năng lực mà nếu làm cách khác sẽ phá hủy nó, và nó cho ra một chỉ số mạnh chính vì mang tính cấu trúc: không một trường nào của bất kỳ thẻ thực tế nào có thể bị bịa, và điều này được khẳng định tự động trong bộ kiểm thử (Mục 14.3).

## 5. Khảo sát / Các giải pháp hiện có

### 5.1. Retrieval-Augmented Generation và GraphRAG

Lewis và cộng sự kết hợp một mô hình ngôn ngữ tham số với bộ nhớ không tham số được truy hồi từ chỉ mục ngoài, cải thiện hỏi đáp đòi hỏi nhiều tri thức và cung cấp cơ sở truy hồi để kiểm chứng [1]. GraphRAG của Microsoft Research kết hợp trích xuất văn bản, phân tích mạng và nhắc/tóm tắt bằng LLM để suy luận trên cấu trúc của tập dữ liệu thay vì trên các đoạn rời rạc [2]; Edge và cộng sự trình bày chi tiết hướng tóm tắt cục bộ-đến-toàn cục theo truy vấn [3].

Dự án này khác cách hiện thực tham chiếu của GraphRAG ở một điểm, vì một lý do đã đo được và ghi trong `docs/architecture.md`: đồ thị ở đây được xây **tất định** từ danh sách thực thể tuyển chọn, một tập từ vựng phân loại đóng và biểu thức chính quy, không phải bằng trích xuất LLM. Trích xuất bằng LLM trên kho ngữ liệu này với phần cứng cục bộ được ước lượng mất 8–12 giờ mỗi lần dựng chỉ mục, dùng prompt tiếng Anh trên văn bản tiếng Việt, và có thể đưa vào những thực thể không có trong nguồn. Đồ thị tất định dựng trong 0,23 giây và mọi đỉnh đều truy về được một chuỗi con nguyên văn của tài liệu nguồn — đó là tiền đề cho phần giải thích gợi ý ở F06.

### 5.2. Hệ gợi ý và yêu cầu giải thích được

Gợi ý thương mại bị chi phối bởi lọc cộng tác và biểu diễn nhúng học được, hai thứ cần quy mô và cho ra đầu ra không minh bạch. Dự án này dùng **gợi ý theo đường đi trên đồ thị**: ứng viên được cho điểm bằng lan truyền có trọng số trên đồ thị di sản, và đường lan truyền được trả về làm lời giải thích. Cách này khả thi với một hệ thống khởi động nguội, một địa bàn, không có nền người dùng; kiểm toán được; và trực tiếp hỗ trợ yêu cầu xuyên miền — một số hạng thưởng cho ứng viên đến được bằng đường đi thật nhưng thuộc danh mục văn hóa khác, đó chính là định nghĩa máy móc của "gợi ý văn hóa liên quan, chứ không phải thêm cái giống nữa".

### 5.3. Các nền tảng tương đương

Google Arts & Culture tổng hợp các bộ sưu tập đã số hóa và những câu chuyện theo địa điểm do bảo tàng khắp thế giới biên tập [5], [6]. Nền tảng này chia sẻ cùng mục tiêu trải nghiệm với HeritageGraph là ghép hình ảnh với bối cảnh tường thuật, nhưng độ liên quan do biên tập viên quyết định, không có đồ thị thực thể–quan hệ phơi ra cho người dùng, không có hỏi đáp mở có trích nguồn trên một kho ngữ liệu địa phương cụ thể, và không có mô hình sở thích theo từng người.

Các nền tảng du lịch (cổng đặt chỗ và điểm đến) có cung cấp thông tin hậu cần thực tế, nhưng đặt thương mại lên trước: chúng không có đồ thị tri thức văn hóa, không trích nguồn, và không có hành vi từ chối.

### 5.4. So sánh với các hướng tiếp cận hiện có

| Tiêu chí | Trang di sản tĩnh / địa chí | Chatbot LLM đa dụng | Google Arts & Culture | Cổng du lịch / đặt chỗ | **HeritageGraph v2** |
| --- | --- | --- | --- | --- | --- |
| Dữ liệu chính | Bài rời rạc và chú thích | Tri thức trong trọng số mô hình | Trưng bày bảo tàng đã biên tập | Danh sách thương mại | Kho ngữ liệu địa phương + đồ thị tri thức + bản ghi có kiểu |
| Liên kết người–nơi–sự kiện–thời gian | Thường không có | Không đáng tin | Do biên tập viên tạo | Không có | Đồ thị tất định, có nguồn gốc trên từng đỉnh |
| Cá nhân hóa | Không | Chỉ là bộ nhớ hội thoại | Rất ít | Nhắm mục tiêu theo ý định mua | Hồ sơ sở thích + cho điểm theo đường đi đồ thị |
| Giải thích được "vì sao cái này?" | Không | Không | Không | Không | **Có — trả về đường lan truyền** |
| Gợi ý xuyên miền | Không | Không kiểm chứng được | Trong phạm vi trưng bày đã biên tập | Không | **Có số hạng thưởng xuyên danh mục tường minh** |
| Trích nguồn ở mức đoạn | Thỉnh thoảng | Không bảo đảm | Chỉ ghi công ở mức trưng bày | Không | **Bắt buộc, có đo** |
| Từ chối khi thiếu bằng chứng | Không áp dụng | Hiếm | Không áp dụng | Không áp dụng | **Ba cổng cấu trúc, có đo** |
| Bối cảnh lên kế hoạch thực tế | Không | Không kiểm chứng được | Không | Có, ưu tiên thương mại | **Có, dữ liệu có kiểu và có nguồn** |
| Tính khả thi như một capstone | Cao, giá trị thấp | Cao, không kiểm soát được nguồn | Cần mạng đối tác | Cần dữ liệu thương mại | Vừa với 13 tuần còn lại |

### 5.5. Điểm khác biệt của dự án

HeritageGraph không tuyên bố thay thế các hệ thống bảo tồn chuyên nghiệp hay các nền tảng tổng hợp lớn. Đóng góp của nó là tổ hợp mà không đối tượng so sánh nào trong bốn cái trên có được: **cá nhân hóa theo từng người dùng và bối cảnh thực tế chủ động, đặt trên một bộ máy trả lời kiểm chứng được, có trích nguồn và biết từ chối — với mọi gợi ý giải thích được thành một đường đi trên đồ thị và mọi phát biểu thực tế truy về được một bản ghi nguồn có kiểu.**

## 6. Mục tiêu và Phạm vi

### 6.1. Mục tiêu tổng quát

Xây dựng và đánh giá một nguyên mẫu AI trên web cho văn hóa Huế và Đà Nẵng, có khả năng: (a) trả lời câu hỏi tiếng Việt từ kho ngữ liệu địa phương với trích nguồn ở mức câu và từ chối tường minh; (b) cá nhân hóa nội dung hiển thị cho từng người dùng bằng hồ sơ sở thích và một bộ gợi ý theo đường đi đồ thị giải thích được; (c) chủ động cung cấp bối cảnh thực tế có kiểu tương ứng với ý định của người dùng — lịch, địa điểm, thời tiết, chuẩn bị, điểm quan sát, chỗ gửi xe, cổ vật tương đương và nghề liên quan.

### 6.2. Mục tiêu cụ thể

**Nền tri thức**

- Duy trì kho ngữ liệu tối thiểu **80 tài liệu** phủ cả sáu danh mục văn hóa với tối thiểu **8 tài liệu mỗi danh mục**, để gợi ý xuyên miền có độ sâu ở mọi hướng. *(Hiện tại: 45 tài liệu / 349 đoạn, trong đó Nghệ thuật 4, Lễ hội 2, Làng nghề 2 — mất cân bằng danh mục là rủi ro dữ liệu lớn nhất đối với mục tiêu cá nhân hóa và được xếp lịch làm trước, Mục 11.2 Tuần 4.)*
- Duy trì đồ thị tri thức tất định trên tài liệu, thực thể, đơn vị hành chính, vùng, danh mục và năm, với mọi đỉnh truy về được một chuỗi nguồn nguyên văn. *(Hiện tại: 510 đỉnh / 1135 cạnh, 1 thành phần liên thông, 0 tài liệu cô lập, dựng trong 0,23 giây.)*
- Soạn ba tập bản ghi có cấu trúc mới, mỗi trường mang theo URL nguồn và câu nguồn đã đọc ra nó: **≥ 50 địa điểm kèm tọa độ**, **≥ 20 lễ hội/sự kiện kèm loại lịch, ngày, đơn vị tổ chức và các phần lễ/hội**, và **≥ 35 cổ vật bảo tàng kèm niên đại, chất liệu, bảo tàng đang giữ và vị trí trên sơ đồ**.

**Lớp trả lời (đã xây; sẽ đo lại trên kho ngữ liệu cuối)**

- Hỏi đáp tiếng Việt chỉ bằng văn bản, trích nguồn bắt buộc theo dạng `[Nguồn: <câu nguyên văn> — <url>]`, và từ chối khi bằng chứng không đủ.
- Trích xuất thực thể bốn loại (người, địa điểm, sự kiện, thời gian) dưới dạng JSON nghiêm ngặt.

**Lớp cá nhân hóa (mới)**

- Thu nhận sở thích tường minh khi khởi tạo và ngầm định từ tương tác, có suy giảm theo thời gian.
- Xếp hạng và mở rộng kết quả theo từng người; trả về kèm mỗi gợi ý đường đi đồ thị biện minh cho nó.
- Đạt được một **tỷ lệ xuyên miền** đo được — tỷ lệ gợi ý thuộc danh mục văn hóa khác với danh mục hạt giống — thay vì chỉ "thêm cái giống nữa" trong cùng danh mục.

**Lớp tư vấn (mới)**

- Phân loại ý định truy vấn thành sáu lớp (nghiên cứu, dự sự kiện, lên kế hoạch đi, tìm hiểu, so sánh, kiểm chứng).
- Kết xuất các khối bối cảnh có kiểu phù hợp ý định, với không một trường nào bị bịa, được khẳng định bằng kiểm thử tự động.

**Đánh giá**

- Báo cáo F1 thực thể, độ trung thực trích nguồn, độ chính xác từ chối, recall truy hồi, độ chính xác ý định, precision@5 và nDCG@5 của gợi ý kèm độ đồng thuận giữa người đánh giá, tỷ lệ xuyên miền, độ đúng trường của thẻ, và độ trễ p95.

### 6.3. Trong phạm vi

Một cặp địa bàn thử nghiệm (Huế và Đà Nẵng) trên sáu danh mục văn hóa; chat tiếng Việt chỉ bằng văn bản; đồ thị tri thức tất định; truy hồi lai neo trên đồ thị; mô hình tinh chỉnh theo miền với trích nguồn và từ chối; tài khoản người dùng có xác thực; hồ sơ sở thích và bộ gợi ý giải thích được; phân loại ý định; các thẻ tư vấn có kiểu bao gồm thời tiết và điểm quan tâm từ API công khai miễn phí; **một** sơ đồ bảo tàng có điểm nóng; luồng rà soát nội dung cho người quản trị/biên tập; bộ đánh giá và báo cáo.

Người dùng cuối chỉ gửi văn bản; họ không tải ảnh hay tài liệu qua giao diện chat.

### 6.4. Ngoài phạm vi

Mô hình 3D, LiDAR, quét ảnh lập thể, bản sao số và tham quan ảo; GIS chuyên nghiệp; nhận dạng video; OCR quy mô lớn cho tài liệu scan; dịch đa ngữ và bản địa hóa giao diện; đặt vé hoặc đặt tour và mọi giao dịch thương mại; dữ liệu đám đông hoặc giao thông thời gian thực; chứng nhận lịch sử chính thức cho nội dung; gợi ý bằng lọc cộng tác đòi hỏi nền người dùng; ứng dụng di động gốc.

Cũng bị loại tường minh khỏi phạm vi v1.0 ở bản chỉnh sửa này, để đánh đổi lấy bốn nhóm năng lực mới (thống kê đầy đủ ở Mục 16): thư viện ảnh và luồng tải ảnh, câu chuyện nhiều ảnh với đường camera và mốc thời gian, luồng nạp DOCX, và chỉ mục vector riêng. Lý do cho từng mục ghi ở Mục 16.2; cả bốn được liệt vào hướng phát triển tương lai.

## 7. Tính năng chính và Yêu cầu

### 7.1. Tính năng cốt lõi

Tính năng được nhóm theo tác nhân. Quản trị/Biên tập là F01–F04, Người dùng là F05–F10, và các trao đổi nội bộ với thành phần AI là F11–F12. Mỗi luồng yêu cầu có một luồng phản hồi tương ứng, cho **12 cặp yêu cầu/phản hồi** trong sơ đồ ngữ cảnh (Mục 12.2) — v1.0 có 10 cặp; F06 được tách và F09, F10 là mới.

| Mã | Tính năng | Tác nhân | Mô tả | Trạng thái |
| --- | --- | --- | --- | --- |
| F01 | Yêu cầu đăng nhập | Quản trị | Quản trị xác thực; hệ thống trả về phản hồi đăng nhập và thông tin phiên | Mới |
| F02 | Yêu cầu quản lý nội dung văn hóa | Quản trị | CRUD trên tài liệu, tên gọi khác và gán danh mục/vùng; hệ thống trả kết quả CRUD và kích hoạt dựng lại đồ thị | Mới |
| F03 | Yêu cầu quản lý bản ghi có cấu trúc | Quản trị | CRUD trên ba tập bản ghi mới — địa điểm kèm tọa độ, sự kiện kèm lịch và các phần, cổ vật kèm niên đại/chất liệu/vị trí — mỗi trường bắt buộc có URL nguồn và câu nguồn; hệ thống trả kết quả kiểm tra và **từ chối mọi bản ghi có trường không nguồn** | Mới |
| F04 | Yêu cầu bảng điều khiển quản trị | Quản trị | Quản trị xem sức khỏe kho ngữ liệu và đồ thị; hệ thống trả dữ liệu tổng quan (số tài liệu theo danh mục, thống kê đồ thị, số trường thiếu nguồn, chỉ số đánh giá mới nhất) | Mới |
| F05 | Khởi tạo / cập nhật hồ sơ sở thích | Người dùng | Người dùng chọn danh mục văn hóa và các mục cụ thể quan tâm, hoặc sửa hồ sơ đã có; hệ thống trả về hồ sơ đã lưu. Giải quyết khởi động nguội | Mới |
| F06 | Yêu cầu khám phá cá nhân hóa | Người dùng | Người dùng mở một chủ đề, địa điểm, cổ vật, món ăn hay lễ hội; hệ thống trả về **danh sách gợi ý cá nhân hóa kèm đường đi đồ thị giải thích cho từng mục**, bao gồm các mục xuyên danh mục | Mới |
| F07 | Truy vấn tìm kiếm theo sở thích | Người dùng | Người dùng tìm theo từ khóa; hệ thống trả kết quả đã xếp hạng lại theo hồ sơ sở thích | Mới |
| F08 | Truy vấn ngôn ngữ tự nhiên (văn bản) | Người dùng | Người dùng gửi câu hỏi văn hóa tự do bằng tiếng Việt; hệ thống trả câu trả lời kèm trích nguồn, hoặc phát biểu tường minh rằng bằng chứng không đủ | **Đã xây** |
| F09 | Yêu cầu bối cảnh chủ động | Người dùng | Kích hoạt bởi ý định phát hiện được ở F06 hoặc F08; hệ thống trả về **các thẻ tư vấn có kiểu** — lịch sự kiện, bản đồ địa điểm, thời tiết và danh mục cần chuẩn bị, điểm quan sát tốt nhất, chỗ gửi xe gần nhất, cổ vật tương đương, nghề liên quan — mỗi thẻ mang theo nguồn gốc | Mới |
| F10 | Yêu cầu vị trí cổ vật | Người dùng | Người dùng hỏi cổ vật được trưng bày ở đâu; hệ thống trả sơ đồ bảo tàng với điểm nóng được làm nổi | Mới |
| F11 | Yêu cầu phân tích nội dung | Nội bộ | Hệ thống gửi văn bản tài liệu tới thành phần phân tích; trả về thực thể và quan hệ đã trích để dựng đồ thị. Chạy khi F02 xảy ra | **Đã xây** (tất định, cục bộ) |
| F12 | Yêu cầu sinh câu trả lời | Nội bộ | Hệ thống gửi bối cảnh đã tổ hợp và câu hỏi tới mô hình tinh chỉnh cục bộ; trả về phần kể chuyện đã sinh. Chạy khi F08 xảy ra | **Đã xây** (mô hình cục bộ) |

Hai điểm hội đồng phản biện sẽ hỏi.

**F11 và F12 là nội bộ và cục bộ.** v1.0 vẽ chúng thành một "Dịch vụ AI/LLM bên ngoài". Cả hai giờ chạy trong tiến trình trên phần cứng cục bộ: F11 là dựng đồ thị tất định, không gọi mô hình nào; F12 là một mô hình ba tỷ tham số chạy cục bộ với bộ điều hợp theo miền. Điều này loại bỏ rủi ro chi phí API của v1.0 và loại bỏ mọi phụ thuộc vào nhà cung cấp bên ngoài — văn bản kho ngữ liệu văn hóa không bao giờ rời khỏi máy.

**F09 là tính năng không được phép bịa.** Các thẻ của nó được kết xuất từ bản ghi có kiểu và API công khai miễn phí (thời tiết, điểm quan tâm), không bao giờ do sinh văn bản tạo ra. Yếu tố kích hoạt là nhận diện ý định, không phải một cú nhấp tường minh của người dùng — chính điều đó làm nó "chủ động" theo nghĩa được yêu cầu ở buổi phản biện: hệ thống suy ra nhu cầu chưa nói ra.

Phụ thuộc: F06, F07, F08, F09 và F10 đều phụ thuộc đồ thị do F11 dựng; F06 và F07 phụ thuộc thêm vào hồ sơ từ F05; F09 phụ thuộc thêm vào bản ghi có cấu trúc từ F03. Thẻ thời tiết và chỗ gửi xe của F09 suy giảm mềm về trạng thái "không có dữ liệu" khi không gọi được API bên ngoài, và chính sự suy giảm này là một ca kiểm thử.

### 7.2. Yêu cầu chức năng

| Mã | Yêu cầu chức năng | Tiêu chí chấp nhận |
| --- | --- | --- |
| FR01 | Người dùng có thể đăng ký và xác thực | Mật khẩu chỉ lưu dưới dạng băm argon2id; thông tin phiên phát hành qua cookie HttpOnly; các endpoint được bảo vệ từ chối yêu cầu chưa xác thực |
| FR02 | Quản trị có thể thêm hoặc sửa tài liệu kho ngữ liệu | Tài liệu được chuẩn hóa, tách thành đoạn kèm định vị nguồn, và đồ thị được dựng lại với các đỉnh mới liên kết về nguồn |
| FR03 | Quản trị có thể thêm bản ghi địa điểm, sự kiện và cổ vật | Bản ghi chỉ được lưu nếu mọi trường sự kiện đều có URL nguồn và câu nguồn; trường thiếu nguồn bị từ chối kèm lỗi ở mức trường |
| FR04 | Hệ thống trích xuất thực thể và quan hệ từ tài liệu | Đầu ra khớp lược đồ bốn loại và mọi tên trích ra là chuỗi con nguyên văn của nguồn |
| FR05 | Hệ thống dựng và cập nhật đồ thị tri thức | Đỉnh và cạnh được tạo, gán kiểu, gán trọng số và liên kết về tài liệu nguồn; thống kê đồ thị được báo cáo |
| FR06 | Người dùng có thể hoàn tất khởi tạo sở thích | Chọn được tối thiểu ba danh mục và ba mục cụ thể; hồ sơ được lưu bền và sửa được |
| FR07 | Hệ thống ghi nhận tương tác ngầm định | Sự kiện xem, thời gian dừng, nhấp thẻ, lưu và bỏ qua được ghi kèm mốc thời gian và đỉnh đích; trọng số hồ sơ cập nhật có suy giảm theo thời gian |
| FR08 | Hệ thống trả về gợi ý cá nhân hóa | Với một chủ đề và một hồ sơ, hệ thống trả danh sách xếp hạng trong đó **mỗi mục kèm đường đi đồ thị đã sinh ra nó** |
| FR09 | Gợi ý bao gồm mục xuyên danh mục | Với hạt giống có danh mục được nối trong đồ thị, tối thiểu một trong năm gợi ý đầu thuộc danh mục văn hóa khác |
| FR10 | Người dùng có thể gửi câu hỏi tiếng Việt chỉ bằng văn bản | Giao diện chat chỉ nhận văn bản; câu trả lời sinh ra chỉ từ bối cảnh đã truy hồi |
| FR11 | Câu trả lời có trích nguồn hoặc phát biểu thiếu bằng chứng | Không sinh ra câu trả lời khẳng định nào mà không có câu nguồn được trích từ tài liệu đã truy hồi |
| FR12 | Hệ thống phân loại ý định truy vấn | Truy vấn được gán vào một trong sáu lớp ý định; lớp được gán được ghi lại và kiểm tra được |
| FR13 | Hệ thống trả thẻ tư vấn phù hợp ý định | Thẻ khớp sổ đăng ký ý định–bộ sinh; **mọi trường của thẻ bằng đúng trường tương ứng của bản ghi nguồn hoặc phản hồi API, không có trường nào do sinh ra** |
| FR14 | Hệ thống cung cấp lịch sự kiện và chi tiết địa điểm | Với sự kiện có trong kho ngữ liệu, hệ thống trả tên, loại lịch và ngày, địa điểm kèm tọa độ, đơn vị tổ chức, và các phần lễ/hội |
| FR15 | Hệ thống cung cấp thời tiết và danh mục chuẩn bị cho sự kiện có ngày | Dự báo lấy từ API thời tiết công khai theo tọa độ địa điểm; danh mục chuẩn bị sinh bằng luật tường minh trên dự báo, không bằng sinh văn bản |
| FR16 | Hệ thống hiển thị vị trí cổ vật trên sơ đồ bảo tàng | Điểm nóng của cổ vật được yêu cầu được làm nổi trên sơ đồ của bảo tàng đang giữ |
| FR17 | Quản trị có thể xác nhận hoặc sửa kết quả trích xuất và dữ liệu bản ghi | Thay đổi và người thực hiện được ghi vào sổ kiểm toán |
| FR18 | Hệ thống chạy được toàn bộ bộ đánh giá | Mọi chỉ số ở Mục 14.3 được tính và xuất ra tệp báo cáo có ghi mô hình, checkpoint bộ điều hợp, phiên bản prompt, phiên bản kho ngữ liệu và cấu hình đánh giá |
| FR19 | Người dùng có thể xuất và xóa dữ liệu cá nhân của mình | Hồ sơ và lịch sử tương tác được trả về dưới dạng tệp máy đọc được và có thể xóa vĩnh viễn khi yêu cầu |

### 7.3. Yêu cầu phi chức năng

| Mã | Nhóm | Yêu cầu |
| --- | --- | --- |
| NFR01 | Hiệu năng | Độ trễ đầu-cuối p95 cho câu hỏi tiêu chuẩn không vượt 8 giây trong môi trường demo; đo liên tục từ Tuần 3, không đo ở cuối kỳ |
| NFR02 | Hiệu năng | Phản hồi gợi ý và thẻ tư vấn trong 2 giây không tính thời gian sinh của mô hình; các lệnh gọi API bên ngoài chạy song song với bước sinh |
| NFR03 | Độ chính xác | recall@1 truy hồi trên tập câu hỏi trong phạm vi đạt tối thiểu 95% |
| NFR04 | Độ tin cậy | Độ trung thực trích nguồn tối thiểu 85% và độ phủ trích nguồn trên các câu trả lời được tối thiểu 90% |
| NFR05 | An toàn | Độ chính xác từ chối tối thiểu 90%; một câu trả lời khẳng định bịa đặt trên câu hỏi ngoài phạm vi tính là lỗi |
| NFR06 | An toàn | **Không một trường bịa nào trong thẻ tư vấn**, được khẳng định tự động trên toàn bộ tập kiểm thử thẻ |
| NFR07 | Giải thích được | Mọi gợi ý phơi ra một đường đi đồ thị đọc được; gợi ý không có đường đi là một lỗi |
| NFR08 | Khả dụng | Người dùng mới hoàn tất khởi tạo và đặt được câu hỏi mà không cần hướng dẫn viết |
| NFR09 | Tiếp cận | Có văn bản thay thế cho mọi nội dung không phải chữ; độ tương phản đủ; chat và thẻ điều hướng được bằng bàn phím; bản ghi hội thoại được công nghệ trợ giúp đọc ra |
| NFR10 | Bảo mật | Xác thực trên mọi endpoint đọc hoặc ghi dữ liệu cá nhân; kiểm tra đầu vào; không có đường ghi nào không xác thực; máy chủ không mở ra giao diện mạng công khai trong cấu hình demo |
| NFR11 | Riêng tư | Ghi nhận tương tác cần sự đồng ý có thông báo; chỉ lưu dữ liệu cần cho gợi ý; hỗ trợ xuất và xóa (FR19) |
| NFR12 | Nguồn gốc | Mọi phát biểu thực tế hiển thị đều truy về được một nguồn — câu trong kho ngữ liệu, trường bản ghi có cấu trúc kèm nguồn của nó, hoặc một API bên ngoài có tên kèm mốc thời gian lấy dữ liệu |
| NFR13 | Bảo trì | Nạp dữ liệu, đồ thị, truy hồi, sinh, gợi ý, tư vấn và giao diện vẫn là các mô-đun có giao diện tách biệt |
| NFR14 | Tái lập | Định danh mô hình, checkpoint bộ điều hợp, phiên bản prompt, phiên bản kho ngữ liệu, thống kê đồ thị và cấu hình đánh giá được ghi trong mọi tệp báo cáo |
| NFR15 | Mở rộng | Thêm một vùng, danh mục, sự kiện, địa điểm hay cổ vật mới không cần sửa mã; thêm một loại thẻ tư vấn mới chỉ cần đăng ký một bộ sinh |

## 8. Ràng buộc và Giả định

### 8.1. Ràng buộc

| Nhóm ràng buộc | Mô tả |
| --- | --- |
| Thời gian | Còn 13 trong 15 tuần ban đầu tính từ bản chỉnh sửa này. Đây là ràng buộc quyết định và là lý do Mục 16.2 loại bỏ bốn nhóm tính năng của v1.0 thay vì thêm bốn nhóm mới lên trên |
| Nhân lực | Một người phát triển. Không có luồng công việc song song; không có rà soát mã nội bộ; đánh giá độ liên quan và rà soát nhãn vàng cần người đánh giá thứ hai từ bên ngoài (Mục 11.3) |
| Phần cứng | Phát triển và trình diễn trên một máy tính Apple Silicon. Điều này cố định mô hình ở lớp ba tỷ tham số lượng tử hóa 4-bit và làm độ trễ sinh văn bản trở thành số hạng chi phối trong NFR01 |
| Kho ngữ liệu | Nguồn bách khoa không đều theo danh mục: di tích thì sâu, nghệ thuật diễn xướng và làng nghề thì mỏng, lễ hội gần như không có. Dữ liệu sự kiện, địa điểm và cổ vật có cấu trúc hoàn toàn không tồn tại trong nguồn và phải soạn thủ công kèm trích nguồn |
| Ngôn ngữ | Tên riêng, tên gọi khác, dấu và cách gõ không dấu tiếng Việt không nhất quán; tên đơn vị hành chính đã đổi trong các lần sắp xếp gần đây |
| Dữ liệu ngoài | API thời tiết và điểm quan tâm miễn phí, không cần khóa, nhưng có giới hạn tần suất; và độ phủ điểm quan tâm của bản đồ mở tại Việt Nam không đồng đều — dữ liệu bãi xe và cửa hàng có thể thiếu ở một địa điểm cụ thể |
| Lịch | Ngày lễ hội Việt Nam cho theo âm lịch; các thư viện âm lịch đa dụng theo lịch Trung Quốc và có thể lệch một ngày ở ranh giới UTC+7 |
| Đánh giá | Với một người phát triển và không có nền người dùng, độ liên quan của gợi ý và văn phong kể chuyện không thể đo ở quy mô thống kê; chúng được báo cáo dưới dạng đánh giá mẫu nhỏ kèm chỉ số đồng thuận, và được ghi rõ là như vậy |

### 8.2. Giả định

- Các nguồn bách khoa và nguồn chính thống về văn hóa Huế và Đà Nẵng vẫn truy cập công khai được tại thời điểm mở rộng kho ngữ liệu ở Tuần 4, và việc sử dụng lại cho một nguyên mẫu học thuật phi thương mại là được phép kèm ghi công.
- Các dữ kiện về sự kiện, địa điểm và cổ vật có thể lấy từ ấn phẩm của trung tâm bảo tồn, bảo tàng và cơ quan quản lý đô thị, mỗi dữ kiện ghi kèm URL và câu nguồn trích dẫn được.
- Các API thời tiết và bản đồ công khai miễn phí vẫn dùng được không cần khóa ở lưu lượng của một buổi trình diễn.
- Máy trình diễn đủ tài nguyên để chạy đồng thời truy hồi, đồ thị, cơ sở dữ liệu và mô hình cục bộ ở quy mô nhỏ.
- Người dùng có trình duyệt và kết nối mạng; họ chỉ gõ văn bản và không bao giờ tải tệp lên.
- Mục tiêu là chứng minh tính khả thi của luồng xử lý và độ tin cậy đo được, không phải triển khai một hệ thống lưu trữ chính thức.
- Phần kể chuyện của AI được coi là gợi ý cần biên tập viên xác nhận; bản ghi có cấu trúc chỉ được coi là có căn cứ trong giới hạn nguồn đã trích của nó.
- Việc ghi nhận tương tác có sự đồng ý; người dùng có thể khám phá mà không cần hồ sơ, khi đó gợi ý chỉ dựa vào độ gần đồ thị với chủ đề đang xem.

## 9. Đối tượng người dùng / Các bên liên quan

| Nhóm | Nhu cầu | Hệ thống giúp thế nào |
| --- | --- | --- |
| Học sinh, sinh viên, người trẻ | Tìm hiểu văn hóa nhanh, trực quan, theo tò mò của chính mình | Hồ sơ sở thích, gợi ý xuyên miền kèm lý do nhìn thấy được, câu trả lời có trích nguồn |
| Khách du lịch trong nước và khách quan tâm văn hóa | Quyết định xem gì và làm sao để thật sự đi dự được | Lịch sự kiện, bản đồ địa điểm, thẻ thời tiết và chuẩn bị, thẻ điểm quan sát và chỗ gửi xe |
| Giáo viên | Tư liệu trực quan, có nguồn cho bài học | Duyệt theo danh mục và vùng, trích nguồn dùng được làm tài liệu tham khảo, trích xuất thực thể trên đoạn được cung cấp |
| Bảo tàng, thư viện, trung tâm văn hóa | Giới thiệu bộ sưu tập và nối nó với bối cảnh rộng hơn | Bản ghi cổ vật có cấu trúc kèm vị trí trên sơ đồ; liên kết đồ thị từ cổ vật tới niên đại, địa điểm và nghề |
| Nhà nghiên cứu | Tìm quan hệ, đối chiếu nguồn, phát hiện khoảng trống | Đồ thị kiểm tra được, vết truy hồi ở mức đoạn, tên gọi khác, nguồn gốc trên từng đỉnh |
| Nghệ nhân và cộng đồng địa phương | Tri thức của mình được ghi lại chính xác và ghi công đúng | URL nguồn và câu nguồn trên mọi trường có cấu trúc; rà soát của biên tập viên; giới hạn phạm vi được nói rõ |
| Người phát triển | Một bài toán AI và công nghệ phần mềm kiểm thử được | Kiến trúc mô-đun, API có kiểu, bộ đánh giá, mục tiêu đo được |
| Giảng viên hướng dẫn / hội đồng | Đánh giá tính khả thi, độ chặt chẽ và đóng góp | Thống kê thay đổi phạm vi v1.0→v2.0 tường minh (Mục 16), baseline đã đo, báo cáo hạn chế trung thực (Mục 14.4) |

## 10. Công nghệ sử dụng

| Thành phần | Công nghệ | Mục đích | Trạng thái |
| --- | --- | --- | --- |
| Frontend | Next.js (App Router), React, TypeScript, Tailwind CSS | Chat có thẻ, khám phá, khởi tạo sở thích, bản đồ, sơ đồ bảo tàng, quản trị | Chat hiện là một trang tối giản; Tailwind và hệ thẻ là mới |
| Backend | Python, FastAPI, Pydantic | REST API, truy hồi, điều phối, gợi ý, đánh giá | Đã xây; mở rộng thêm |
| Cơ sở dữ liệu quan hệ | PostgreSQL với SQLAlchemy và Alembic | Người dùng, hồ sơ sở thích, sự kiện tương tác, địa điểm, sự kiện, cổ vật, điểm quan tâm, log gợi ý, sổ kiểm toán | **Mới — hiện dự án không có cơ sở dữ liệu nào; toàn bộ trạng thái là tệp cộng một bộ đệm trong RAM** |
| Đồ thị tri thức | NetworkX, dựng tất định trong RAM khi khởi động | Thực thể, tài liệu, vùng, danh mục, đơn vị hành chính, năm, nguồn gốc | Đã xây |
| Truy hồi | Hai chỉ mục BM25 tự hiện thực (token từ và n-gram ký tự đã bỏ dấu) hợp nhất bằng reciprocal rank fusion, rồi xếp hạng lại bằng lan truyền đồ thị | Chịu được gõ không dấu; neo trên thực thể đồ thị | Đã xây |
| Mô hình ngôn ngữ | Qwen2.5-3B-Instruct lượng tử hóa 4-bit chạy cục bộ với bộ điều hợp LoRA, phục vụ qua MLX | Kể chuyện di sản tiếng Việt, định dạng trích nguồn, từ chối, JSON thực thể | Đã xây |
| Tinh chỉnh | MLX LoRA, rank 16 trên 16 lớp cuối, che mất mát ở phần prompt | Dạy văn phong, định dạng trích nguồn, từ chối và đính chính giả định sai — không dạy dữ kiện | Đã xây |
| Phân loại ý định | Dựa trên luật và từ vựng, sáu lớp, trên văn bản đã bỏ dấu | Chọn thẻ tư vấn nào để kết xuất; kiểm toán được và rẻ | Mới; mở rộng hàm nhận diện bốn tín hiệu đang có |
| Gợi ý | Lan truyền đồ thị với độ gần hồ sơ, thưởng xuyên danh mục và xếp hạng lại theo đa dạng | Gợi ý cá nhân hóa, giải thích được | Mới |
| Thời tiết | Open-Meteo (không cần khóa) | Xác suất mưa và nhiệt độ theo giờ cho danh mục chuẩn bị | Mới |
| Bản đồ và điểm quan tâm | OpenStreetMap qua Overpass; Nominatim để mã hóa địa lý một lần có đệm; Leaflet để hiển thị | Bãi xe, điểm quan sát, cửa hàng nghề và quà, bản đồ địa điểm | Mới |
| Sơ đồ bảo tàng | SVG soạn thủ công kèm tọa độ điểm nóng | Hiển thị vị trí cổ vật | Mới |
| Kiểm thử | pytest, Playwright, GitHub Actions | Đơn vị, tích hợp, API, đầu-cuối, và phép khẳng định không-bịa-trường | **Mới — hiện dự án không có framework kiểm thử và không có CI** |
| Triển khai | Docker Compose cho cơ sở dữ liệu; máy chủ cục bộ cho trình diễn | Môi trường tái lập được | Mới |
| Tài liệu | Markdown, Mermaid, OpenAPI | Yêu cầu, kiến trúc, API, báo cáo đánh giá | Một phần |

Hai điểm chệch có chủ ý so với bảng công nghệ v1.0, cả hai đã được kiểm chứng bằng đo đạc và ghi trong `docs/architecture.md`:

**Không có cơ sở dữ liệu vector riêng và không có mô hình embedding.** v1.0 đề xuất Qdrant hoặc pgvector. Cách lai đã hiện thực — BM25 theo từ cộng BM25 theo n-gram không dấu, hợp nhất rồi xếp hạng lại bằng lan truyền đồ thị — đạt recall@1 30/30 trên tập câu hỏi trong phạm vi, kể cả câu không dấu và câu dùng tên gọi khác. Điều đó khiến một chỉ mục vector không còn khiếm khuyết đo được nào để khắc phục. Nó được ghi là hướng phát triển tương lai chứ không bị bỏ im lặng.

**Không có Neo4j.** Đồ thị gồm 510 đỉnh và 1135 cạnh, dựng lại trong RAM mất 0,23 giây. Một cơ sở dữ liệu đồ thị ở quy mô này thêm một phụ thuộc vận hành mà không thêm năng lực nào; PostgreSQL giữ trạng thái ứng dụng bền vững thay thế. Cả hai quyết định được xem lại ở Mục 14.4 như giới hạn về khả năng mở rộng.

## 11. Phương pháp và Kế hoạch phát triển

### 11.1. Phương pháp phát triển

Agile với vòng lặp một tuần và một buổi trình diễn cho giảng viên hướng dẫn mỗi vòng. Vòng ngắn là phù hợp vì chất lượng gợi ý, độ chính xác ý định và tính hữu dụng của tư vấn chỉ có thể đánh giá trên dữ liệu thật và tương tác thật, không đặc tả trước được.

Hai quy tắc trình tự chi phối các tuần còn lại.

**Rủi ro trước.** Ba hạng mục rủi ro cao nhất được xếp sớm nhất: chốt phạm vi với giảng viên hướng dẫn (Tuần 2), mất cân bằng danh mục kho ngữ liệu cùng các bản ghi có cấu trúc soạn thủ công mà mọi thẻ tư vấn phụ thuộc vào (Tuần 4), và đo độ trễ liên tục ngay từ khi cơ sở dữ liệu và xác thực xuất hiện (Tuần 3) chứ không phải trong giai đoạn kiểm thử.

**Không tính năng nào được xây trên một baseline chưa đo.** Tuần 2 trả hết nợ đo lường trong hệ thống hiện có trước khi thêm bất kỳ năng lực mới nào, vì một kết quả cá nhân hóa trình bày trên một lớp trả lời chưa kiểm chứng thì không bảo vệ được ở hội đồng.

### 11.2. Kế hoạch phát triển

Còn mười ba tuần. Số tuần tiếp tục theo kế hoạch ban đầu.

| Tuần | Giai đoạn | Nội dung chính | Kết quả |
| --- | --- | --- | --- |
| 2 | Phạm vi và nợ đo lường | Chốt phạm vi v2.0 và bốn hạng mục loại bỏ với giảng viên hướng dẫn bằng văn bản; sửa mọi số liệu lạc hậu trong tài liệu; sửa lỗi rò rỉ truy hồi đã biết; đo lại mô hình gốc trên tập đánh giá hiện tại để phép so sánh trước/sau có giá trị; ghi checkpoint bộ điều hợp vào tệp báo cáo | Phạm vi đã chốt; tài liệu đã sửa; bộ kiểm thử truy hồi đạt; baseline so sánh được |
| 3 | Nền tảng | PostgreSQL với Docker Compose và migration; mô hình dữ liệu; đăng ký và đăng nhập với argon2id và cookie phiên HttpOnly; ghi sự kiện tương tác có đồng ý; Tailwind; mở rộng lược đồ phản hồi chat; **đo độ trễ lần đầu** | Tài khoản, lưu bền, log sự kiện, baseline độ trễ |
| 4 | Dữ liệu miền | Mở rộng kho ngữ liệu tới 80 tài liệu với tối thiểu 8 mỗi danh mục; soạn địa điểm kèm tọa độ, sự kiện kèm lịch và các phần, cổ vật kèm niên đại, chất liệu và vị trí — mọi trường có nguồn; dựng lại đồ thị; sinh lại tập đánh giá; chạy lại đánh giá truy hồi | Kho ngữ liệu cân bằng, ba tập bản ghi có cấu trúc, tập đánh giá đã làm mới — **hoàn thành F03 và F14** |
| 5–6 | Cá nhân hóa | Hồ sơ sở thích có suy giảm; khởi tạo sở thích; độ gần đồ thị, độ gần hồ sơ, thưởng xuyên danh mục, xếp hạng lại theo đa dạng; endpoint gợi ý trả về đường đi giải thích; ghi log gợi ý; giao diện khám phá và chi tiết có dải nội dung liên quan | **Hoàn thành F05, F06, F07** |
| 7–8 | Tư vấn chủ động | Bộ phân loại ý định sáu lớp và tập câu hỏi gán nhãn; sổ đăng ký ý định–thẻ; tích hợp thời tiết; tích hợp điểm quan tâm có đệm; luật danh mục chuẩn bị; gọi API bên ngoài song song chồng lên bước sinh; suy giảm mềm khi API không sẵn sàng | **Hoàn thành F09** |
| 9–10 | Giao diện thẻ và sơ đồ | Sổ đăng ký bộ kết xuất thẻ; hiển thị bản đồ; một sơ đồ bảo tàng dạng SVG soạn thủ công kèm điểm nóng; tương tác vị trí cổ vật; rà soát khả năng tiếp cận cho chat và thẻ | **Hoàn thành F04, F10** |
| 11 | Hành trình cổ vật và lễ hội, đệm | Hoàn thiện hành trình nghiên cứu đầu-cuối (cổ vật → bảo tàng đang giữ → cổ vật cùng thời kỳ → làng nghề liên quan) và hành trình tham dự (lễ hội → lịch → địa điểm → thời tiết → chuẩn bị → điểm quan sát → chỗ gửi xe); hấp thụ trượt tiến độ | Hai hành trình trình diễn hoàn chỉnh |
| 12–13 | Kiểm thử và đánh giá | Bộ pytest và Playwright cùng CI; phép khẳng định không-bịa-trường; toàn bộ chỉ số gồm độ chính xác ý định và precision gợi ý với người đánh giá thứ hai; nghiên cứu người dùng quy mô nhỏ; khắc phục độ trễ nếu NFR01 không đạt | Báo cáo kiểm thử và báo cáo đánh giá |
| 14–15 | Kết thúc | Tài liệu kiến trúc, API và lược đồ; rà soát riêng tư và đạo đức gồm đồng ý, tối giản dữ liệu, xuất và xóa; video trình diễn, slide và hướng dẫn sử dụng; báo cáo cuối | Bản chấp nhận cuối cùng |

### 11.3. Chất lượng, Rà soát và Quản lý phiên bản

Mã nguồn quản lý bằng Git. Mọi thay đổi về luật dựng đồ thị, prompt, mô hình, checkpoint bộ điều hợp, kho ngữ liệu hoặc lược đồ cơ sở dữ liệu đều được ghi vào changelog, vì mỗi thay đổi đó làm mất hiệu lực các chỉ số đã báo cáo trước đó. CI chạy lint và bộ kiểm thử trước khi hợp nhất.

Vì không có người phát triển thứ hai, hai chỗ mà tác giả duy nhất về bản chất không đáng tin sẽ dùng người đánh giá bên ngoài:

- **Nhãn vàng thực thể** hiện được máy điền trước từ đồ thị tất định và được đánh dấu như vậy. Ở trạng thái đó chúng đo được việc mô hình có học được tập luật trích xuất hay không, không đo được việc trích xuất có đúng hay không. Chúng cần người rà soát trước báo cáo cuối, và báo cáo phải nói rõ phần nào đã được rà soát.
- **Độ liên quan của gợi ý** được hai người đánh giá trên cùng một tập hạt giống, và độ đồng thuận giữa hai người được báo cáo cùng với precision. Một con số độ liên quan do chính người viết bộ gợi ý tự đánh giá thì không phải bằng chứng.

Với nội dung văn hóa, mọi trường có cấu trúc đều ghi URL nguồn và câu nguồn, và trạng thái rà soát của biên tập viên được lưu lại. Với các thành phần AI, mọi tệp báo cáo ghi định danh mô hình, checkpoint bộ điều hợp, phiên bản prompt, phiên bản kho ngữ liệu và cấu hình đánh giá (NFR14).

## 12. Tổng quan kiến trúc hệ thống

### 12.1. Mô tả kiến trúc

Bảy lớp. Ba lớp in đậm là mới ở v2.0.

1. **Trình bày** — chat có thẻ có kiểu, trang khám phá và trang chi tiết, khởi tạo sở thích, bản đồ, sơ đồ bảo tàng, khung trích nguồn, rà soát của quản trị.
2. **Ứng dụng / API** — xác thực, chat, khám phá cá nhân hóa, tìm kiếm, gợi ý, tư vấn, kiểm tra đồ thị, quản lý nội dung và bản ghi, đánh giá.
3. **Nạp dữ liệu** — phân giải và tải nguồn, chuẩn hóa, tách đoạn kèm định vị nguồn, trích tên gọi khác.
4. **Xử lý tri thức** — trích xuất thực thể và năm tất định với từ vựng phân loại đóng, nhận diện đơn vị hành chính, dựng đồ thị với cạnh có kiểu, có trọng số và có nguồn gốc.
5. **Lưu trữ** — tệp kho ngữ liệu, đồ thị trong RAM, và PostgreSQL cho người dùng, hồ sơ sở thích, sự kiện tương tác, địa điểm, sự kiện, cổ vật, điểm quan tâm, log gợi ý và sổ kiểm toán.
6. **Điều phối AI** — phân tích truy vấn (phạm vi, ý định, chủ thể so với giả định), truy hồi lai, lan truyền đồ thị, tổ hợp bối cảnh, ba cổng từ chối, sinh văn bản, kiểm tra trích nguồn.
7. **Cá nhân hóa và tư vấn** — duy trì hồ sơ có suy giảm, gợi ý theo đường đi đồ thị với thưởng xuyên danh mục và đa dạng, phân loại ý định, và sổ đăng ký ý định–bộ sinh thẻ kèm bộ điều hợp bên ngoài cho thời tiết và điểm quan tâm.

Nguyên tắc kiến trúc ở Mục 4.4 được bảo đảm ngay tại biên giữa các lớp: lớp 6 sinh ra văn bản kể chuyện; lớp 7 sinh ra đối tượng thẻ có kiểu. Đối tượng thẻ không bao giờ đi qua lớp 6.

### 12.2. Sơ đồ ngữ cảnh hệ thống

*Hình 1. Sơ đồ ngữ cảnh hệ thống (Mức 0)*

HeritageGraph được thể hiện là một tiến trình trao đổi dữ liệu với ba thực thể ngoài: **Quản trị/Biên tập**, **Người dùng**, và **Dịch vụ dữ liệu ngoài** (nhà cung cấp thời tiết và bản đồ/điểm quan tâm). Các kho nội bộ — cơ sở dữ liệu quan hệ và đồ thị tri thức — nằm bên trong biên hệ thống và chỉ xuất hiện ở phân rã Mức 1. Mỗi yêu cầu có một phản hồi tương ứng, cho 12 cặp yêu cầu/phản hồi (Mục 7.1).

Quản trị/Biên tập gửi yêu cầu đăng nhập, yêu cầu quản lý nội dung văn hóa, yêu cầu quản lý bản ghi có cấu trúc và yêu cầu bảng điều khiển, nhận về phản hồi đăng nhập, kết quả CRUD, kết quả kiểm tra và dữ liệu tổng quan.

Người dùng gửi khởi tạo/cập nhật hồ sơ sở thích, yêu cầu khám phá cá nhân hóa, truy vấn tìm kiếm theo sở thích, truy vấn ngôn ngữ tự nhiên, yêu cầu bối cảnh chủ động và yêu cầu vị trí cổ vật, nhận về hồ sơ sở thích đã lưu, danh sách gợi ý cá nhân hóa kèm đường đi giải thích, kết quả đã xếp hạng cá nhân hóa, câu trả lời kèm trích nguồn hoặc phát biểu thiếu bằng chứng, các thẻ tư vấn có kiểu kèm nguồn gốc, và sơ đồ có điểm nóng cổ vật được làm nổi.

Hệ thống gửi yêu cầu dự báo thời tiết và yêu cầu điểm quan tâm tới Dịch vụ dữ liệu ngoài và nhận về phản hồi dự báo và phản hồi điểm quan tâm.

Hai thay đổi so với sơ đồ v1.0 cần nêu rõ ở hội đồng. **Thực thể "Dịch vụ AI/LLM bên ngoài" đã biến mất**: phân tích nội dung và sinh câu trả lời giờ lần lượt là nội bộ tất định và cục bộ, nên cả hai luồng chuyển vào trong biên. **Một thực thể "Dịch vụ dữ liệu ngoài" mới xuất hiện**, chỉ mang dữ liệu hậu cần không phải văn hóa. Chiều của thay đổi này mới là điều quan trọng: nội dung văn hóa không còn rời khỏi hệ thống, còn các lệnh gọi ra ngoài duy nhất chỉ mang theo một tọa độ và một ngày.

Cá nhân hóa là tường minh trong sơ đồ này thay vì bị ẩn: hồ sơ sở thích là một thực thể mà Người dùng vừa ghi vào (F05) vừa đọc lại qua đầu ra đã xếp hạng (F06, F07), nên sự thích ứng theo từng người nhìn thấy được ngay ở Mức 0 chứ không bị chôn trong một bước xếp hạng nội bộ.

### 12.3. Luồng xử lý chính

**Nạp nội dung.** Biên tập viên thêm một tài liệu; hệ thống chuẩn hóa, tách thành đoạn kèm định vị nguồn, trích xuất thực thể và năm một cách tất định, nhận diện đơn vị hành chính, và dựng lại đồ thị với các đỉnh mới liên kết về nguồn. Biên tập viên thêm một bản ghi địa điểm, sự kiện hoặc cổ vật; hệ thống kiểm tra rằng mọi trường sự kiện đều có URL nguồn và câu nguồn, từ chối bản ghi nếu không, ghi vào cơ sở dữ liệu, và liên kết nó với đỉnh đồ thị tương ứng.

**Hỏi đáp.** Truy vấn được phân tích về phạm vi vùng và danh mục, về ý định, và về sự phân biệt giữa chủ thể của câu hỏi với giả định mà nó chứa. Hai bảng xếp hạng BM25 được tính rồi hợp nhất; hạt giống đồ thị được khớp từ nhãn thực thể và tên gọi khác; lan truyền trên đồ thị cho ra độ gần của từng tài liệu; ứng viên được cho điểm cộng thêm độ gần đồ thị và thưởng gọi đúng tên bài; các đoạn tốt nhất được tổ hợp thành bối cảnh. Sau đó ba cổng quyết định có trả lời hay không: truy vấn phải neo được vào một đỉnh đồ thị đã biết, một tên riêng được gọi phải có bằng chứng hỗ trợ trong đoạn đã truy hồi, và độ phủ từ vựng phải vượt ngưỡng. Nếu một cổng nào không đạt, bối cảnh để rỗng và mô hình trả lời bằng một lời từ chối tường minh — một hành vi nó đã được tinh chỉnh để sinh ra, nên lời từ chối nằm trong trọng số chứ không chỉ nằm trong một câu điều kiện.

**Cá nhân hóa.** Song song với việc trả lời, chủ thể được dùng làm hạt giống gợi ý. Ứng viên được cho điểm theo độ gần đồ thị với hạt giống, độ gần đồ thị với hồ sơ sở thích, một phần thưởng cho việc thuộc danh mục văn hóa khác nhưng vẫn được nối bởi đường đi thật, và một phần trừ cho các mục đã xem; danh sách xếp hạng được đa dạng hóa để không trả về năm ví dụ cùng một loại di tích. Mỗi mục trả về mang theo đường đi đã sinh ra nó.

**Tư vấn chủ động.** Ý định phát hiện được chọn ra các bộ sinh thẻ từ sổ đăng ký. Bộ sinh đọc bản ghi có kiểu và, khi cần, gọi dịch vụ ngoài với tọa độ địa điểm và ngày sự kiện. Lệnh gọi thời tiết và điểm quan tâm được phát song song với bước sinh của mô hình để độ trễ của chúng ẩn vào trong thời gian sinh. Lời khuyên chuẩn bị được sinh bằng luật tường minh trên dự báo. Mọi thẻ trả về kèm nguồn gốc và thời điểm lấy dữ liệu; một dịch vụ không sẵn sàng cho ra trạng thái không-có-dữ-liệu tường minh chứ không phải một giá trị bịa.

### 12.4. Ví dụ tình huống người dùng

Hai tình huống dưới đây là hai hành trình trình diễn được xây ở Tuần 11, và chúng tương ứng trực tiếp với hai ví dụ được nêu trong buổi phản biện. Cả hai được trình bày với điểm vào *không phải một di tích*, vì trọng điểm của lớp cá nhân hóa là điểm vào có thể là bất kỳ loại đối tượng văn hóa nào — một cổ vật, một món ăn, một loại hình diễn xướng, một nghề thủ công, hay một lễ hội.

**Tình huống A — nghiên cứu một cổ vật.** Người dùng đọc về một tác phẩm điêu khắc đá thời Champa. Lớp trả lời giải thích đối tượng từ kho ngữ liệu kèm một câu trích nguồn. Ý định được phân loại là nghiên cứu, nên lớp tư vấn bổ sung: bảo tàng đang giữ nó kèm vị trí trên sơ đồ, các cổ vật cùng thời kỳ khác trong cùng bộ sưu tập, và những làng nghề mà kỹ thuật còn lưu giữ có liên hệ với nó. Lớp cá nhân hóa, thấy sự quan tâm tới điêu khắc và văn hóa vật chất Chăm, gợi ý xuyên danh mục — một di tích liên quan, một làng nghề, và một loại hình diễn xướng được nối qua đồ thị — mỗi mục kèm đường đi biện minh cho nó. Không có gì trong khối thực tế là do sinh ra: bảo tàng, niên đại, chất liệu và vị trí đều là trường bản ghi có nguồn.

**Tình huống B — đi dự một lễ hội.** Người dùng hỏi về một lễ hội của làng chài. Lớp trả lời giải thích ý nghĩa và cấu trúc nghi lễ từ kho ngữ liệu kèm trích nguồn. Ý định được phân loại là dự sự kiện, nên lớp tư vấn trả về loại lịch và ngày của năm nay, địa điểm kèm tọa độ và bản đồ, các phần lễ và phần hội, dự báo cho ngày đó kèm danh mục chuẩn bị suy ra bằng luật từ xác suất mưa, một điểm quan sát được đề xuất, và chỗ gửi xe gần nhất. Lớp cá nhân hóa gợi ý văn hóa liên quan — món ăn địa phương gắn với làng, một di tích gần đó, loại hình diễn xướng dân gian được trình diễn trong phần hội. Nếu dịch vụ thời tiết không gọi được, thẻ ghi rằng dự báo không có; nó không bao giờ đoán.

### 12.5. Hiện trạng đã đo (baseline)

Vì đây là bản chỉnh sửa chứ không phải đề cương cho công việc chưa bắt đầu, hiện trạng đã đo được ghi lại ở đây để hội đồng phân biệt được cái gì đã có với cái gì còn là kế hoạch, và để các kết quả sau này so được với một baseline đã phát biểu.

| Thành phần | Hiện trạng đã đo |
| --- | --- |
| Kho ngữ liệu | 45 tài liệu dùng được, 349 đoạn; 30 Huế / 15 Đà Nẵng; theo danh mục — di tích 22, ẩm thực 9, danh thắng 6, nghệ thuật 4, lễ hội 2, làng nghề 2 |
| Đồ thị tri thức | 510 đỉnh, 1135 cạnh, 1 thành phần liên thông, 0 tài liệu cô lập, dựng trong 0,23 giây. Đỉnh: 235 thực thể, 222 năm, 45 tài liệu, 6 danh mục, 2 vùng. Cạnh: 443 năm, 242 nhắc đến, 123 liên quan, 98 hành chính, 92 vùng, 92 danh mục, 45 nói-về |
| Truy hồi | Trong phạm vi 68/70; paraphrase 9/39; bằng chứng trong đoạn 34/34; phường/xã 18/20; ngoài phạm vi 31/38. Paraphrase là nút thắt chính |
| Mô hình | Qwen2.5-3B-Instruct 4-bit với bộ điều hợp LoRA rank 16 trên 16 lớp cuối; checkpoint chọn ở bước 200 với mất mát kiểm định 0,414 thay vì bước cuối 720 với 0,473, vì mất mát kiểm định tăng dần từ khoảng bước 250 |
| Chất lượng trả lời | Micro-F1 thực thể 0,786 so với 0,104 của mô hình gốc; độ trung thực trích nguồn 0,704 và độ phủ 0,741; độ chính xác từ chối 0,917 so với 0,375 của mô hình gốc |
| Chưa đo | Độ trễ p95; điểm văn phong; mọi chỉ số thuộc ba lớp năng lực mới |
| Chưa xây | Cơ sở dữ liệu, xác thực, hồ sơ sở thích, bộ gợi ý, bộ phân loại ý định, thẻ tư vấn, bản ghi có cấu trúc, sơ đồ bảo tàng, framework kiểm thử, CI |

Hai ghi chú trung thực được chuyển tiếp vào báo cáo cuối. Base và LoRA đã được đo có kiểm soát trên cùng 76 mẫu, prompt và corpus ngày 08/09/2026. Tuy nhiên, loại thực thể sự kiện có **không** nhãn vàng nào, nên tuyên bố bốn loại thực thể trên thực tế là kết quả ba loại. Nhãn vàng thực thể do máy điền trước và đang chờ người rà soát.

## 13. Rủi ro tiềm ẩn và Biện pháp giảm thiểu

| Rủi ro | Loại | Tác động | Biện pháp giảm thiểu |
| --- | --- | --- | --- |
| Phạm vi vượt quá 13 tuần còn lại | Tiến độ | **Cao nhất** | Mục 16 loại bỏ bốn nhóm tính năng của v1.0 để đánh đổi; chốt thay đổi phạm vi bằng văn bản với giảng viên hướng dẫn ở Tuần 2; Mục 13.1 định nghĩa thứ tự cắt cố định |
| Mất cân bằng danh mục kho ngữ liệu làm hạn chế gợi ý xuyên miền | Dữ liệu / AI | Cao | Mở rộng kho ngữ liệu lên tối thiểu 8 tài liệu mỗi danh mục được xếp ở Tuần 4, trước khi xây bộ gợi ý, và là điều kiện để bắt đầu Tuần 5 |
| Dữ liệu sự kiện, địa điểm và cổ vật phải soạn thủ công | Dữ liệu / Tiến độ | Cao | Giới hạn phạm vi ở 20 sự kiện, 50 địa điểm, 35 cổ vật, một sơ đồ bảo tàng; mọi trường bắt buộc có nguồn; việc soạn được dành trọn một tuần theo lịch, không phải làm kèm |
| Thẻ tư vấn làm hồi sinh hiện tượng bịa đặt | AI / Tin cậy | **Cao** | Nguyên tắc kiến trúc: thẻ được kết xuất từ bản ghi có kiểu và không bao giờ do sinh ra. Được bảo đảm bằng phép khẳng định tự động không-bịa-trường (NFR06). Đây là cam kết an toàn trung tâm của dự án |
| Chất lượng gợi ý không đo được với một người phát triển và không có người dùng | Đánh giá | Cao | Đánh giá độ liên quan bằng hai người kèm báo cáo độ đồng thuận; tỷ lệ xuyên miền và độ đa dạng được tính khách quan không cần phán đoán của người |
| Khởi động nguội — người dùng mới không có hồ sơ | AI / UX | Trung bình | Khởi tạo sở thích tường minh (F05); quay về chỉ dùng độ gần đồ thị với chủ đề đang xem khi chưa có hồ sơ |
| Độ phủ điểm quan tâm ở địa bàn thử nghiệm thưa | Dữ liệu / Ngoài | Trung bình | Kiểm tra độ phủ cho các địa điểm trình diễn ngay đầu Tuần 7; quay về dùng điểm quan tâm soạn thủ công kèm nguồn ở nơi thiếu độ phủ |
| Dịch vụ thời tiết hoặc bản đồ không sẵn sàng lúc trình diễn | Ngoài | Trung bình | Đệm mọi phản hồi bên ngoài; thẻ suy giảm về trạng thái không-có-dữ-liệu tường minh; sự suy giảm này là một ca kiểm thử |
| Quy đổi âm lịch sang dương lịch lệch một ngày | Dữ liệu | Trung bình | Soạn thủ công bảng quy đổi cho các sự kiện thử nghiệm trong khoảng thời gian trình diễn thay vì dựa vào thư viện âm lịch đa dụng; ghi rõ hạn chế |
| Độ trễ p95 vượt 8 giây sau khi thêm thẻ | Hiệu năng | Cao | Đo từ Tuần 3 chứ không phải Tuần 12; chồng lệnh gọi ngoài lên bước sinh; giới hạn số token sinh ra; thêm phát trực tiếp phản hồi làm biện pháp khắc phục nếu không đạt |
| Xử lý dữ liệu cá nhân trở thành nghĩa vụ thật khi bắt đầu ghi tương tác | Đạo đức / Pháp lý | Cao | Xin đồng ý trước khi ghi; chỉ lưu những gì bộ gợi ý cần; xuất và xóa (FR19); rà soát riêng tư xếp ở Tuần 14 |
| Endpoint không xác thực trong khi đã có dữ liệu cá nhân | Bảo mật | Cao | Xác thực xuất hiện ở Tuần 3, **trước** khi lưu bất kỳ dữ liệu cá nhân nào; không có đường ghi nào không xác thực; máy chủ không mở giao diện mạng công khai trong cấu hình demo |
| Trích xuất tên riêng tiếng Việt sai | Kỹ thuật | Cao | Danh sách thực thể tuyển chọn, từ vựng phân loại đóng, từ điển tên gọi khác, ngưỡng số lần nhắc tối thiểu, bộ chặn tên ghép, và ràng buộc mọi tên trích ra là chuỗi con nguyên văn của nguồn |
| Tên hành chính trùng hoặc đã đổi | Kỹ thuật | Trung bình | Tệp tên gọi khác; ghi lại các lần đổi tên; bộ kiểm thử quan hệ hành chính |
| Đồ thị tạo ra quan hệ không có bằng chứng | Tin cậy / AI | Cao | Chỉ tạo quan hệ cấu trúc — thành viên, nhắc đến, hành chính, thời gian, đồng xuất hiện — và không suy ra quan hệ ngữ nghĩa nào; mọi đỉnh truy về được một chuỗi nguồn |
| Nội dung văn hóa nhạy cảm hoặc ghi công sai | Đạo đức | Cao | Nguồn và câu nguồn trên mọi trường có cấu trúc; rà soát của biên tập viên; tuyên bố phạm vi tường minh; cố vấn chuyên môn rà soát bản ghi lễ hội và cổ vật |
| Nguyên mẫu bị nhầm là nguồn sử liệu có thẩm quyền | Truyền thông | Trung bình | Nguồn và nguồn gốc hiển thị trên mọi phát biểu; tuyên bố phạm vi và trạng thái tường minh trong giao diện |
| Người phát triển duy nhất không làm việc được vì lý do sức khỏe | Tiến độ | Cao | Tuần 11 là đệm tường minh; thứ tự cắt ở Mục 13.1 được quyết trước để việc phân loại ưu tiên dưới áp lực không cần phán đoán mới |

### 13.1. Thứ tự cắt cố định khi bị áp lực tiến độ

Quyết trước để việc xử lý ưu tiên không trở thành ứng biến. Cắt theo thứ tự: điểm nóng trên sơ đồ bảo tàng (giữ ảnh sơ đồ tĩnh); điểm quan tâm cửa hàng và quà (giữ bãi xe và điểm quan sát); giảm nghiên cứu người dùng từ tám xuống bốn người; thay giao diện quản trị bằng công cụ dòng lệnh cộng một trang thống kê chỉ đọc; giảm mục tiêu kho ngữ liệu từ 80 xuống 65 tài liệu nhưng giữ nguyên mức tối thiểu mỗi danh mục.

**Không bao giờ cắt, ở bất kỳ mức áp lực tiến độ nào:** ba cổng từ chối, trích nguồn bắt buộc, phép khẳng định không-bịa-trường trên thẻ, và bộ đánh giá. Đó là đóng góp của dự án; thiếu chúng thì đây chỉ là một bản trình diễn không kiểm chứng được.

## 14. Kết quả kỳ vọng / Sản phẩm giao

### 14.1. Kết quả kỳ vọng

Một nguyên mẫu hoạt động được, trong đó sở thích văn hóa của người dùng — với một cổ vật, một món ăn, một loại hình diễn xướng, một nghề thủ công hay một lễ hội — được biến thành một đường đi cá nhân hóa, có giải thích, qua các phần văn hóa liên quan; và trong đó những yêu cầu thực tế để thật sự tham dự được cung cấp tự động, đồng thời mọi phát biểu hiển thị vẫn truy về được nguồn.

Về mặt kỹ thuật, dự án giao một luồng xử lý đầu-cuối đo được, từ nạp dữ liệu qua dựng đồ thị tất định, truy hồi lai, tinh chỉnh theo miền, sinh văn bản có kiểm tra trích nguồn, gợi ý theo đường đi đồ thị, tới kết xuất tư vấn theo ý định.

Về mặt học thuật, dự án đóng góp ba điều ngoài một ứng dụng. Thứ nhất, bằng chứng rằng một đồ thị tri thức tất định, bảo toàn nguồn gốc là đủ cho truy hồi tăng cường bằng đồ thị trong bối cảnh tiếng Việt ít tài nguyên, không cần trích xuất bằng LLM và không cần chỉ mục vector, với chi phí dựng chỉ mục chỉ bằng một phần nhỏ. Thứ hai, một bộ gợi ý khởi động nguội giải thích được cho việc khám phá văn hóa xuyên miền, trong đó tỷ lệ xuyên miền được báo cáo như một chỉ số hạng nhất thay vì coi là tác dụng phụ. Thứ ba, một minh chứng rằng năng lực tư vấn chủ động có thể được thêm vào một hệ hỏi đáp có căn cứ **mà không** làm suy giảm đo được về độ tin cậy, bằng cách tách phần kể chuyện khỏi dữ liệu có kiểu — được hỗ trợ bởi phép đo trước và sau khi tính năng tư vấn xuất hiện, trên độ trung thực trích nguồn và độ chính xác từ chối.

### 14.2. Sản phẩm giao

| STT | Sản phẩm | Mô tả | Trạng thái |
| --- | --- | --- | --- |
| 1 | Nguyên mẫu web | HeritageGraph chạy trong môi trường trình diễn | Một phần |
| 2 | Kho ngữ liệu và đồ thị tri thức | Tối thiểu 80 tài liệu trên sáu danh mục; đồ thị tất định có nguồn gốc; từ điển tên gọi khác | Một phần |
| 3 | Các tập bản ghi có cấu trúc | Địa điểm kèm tọa độ, sự kiện kèm lịch và các phần, cổ vật kèm niên đại, chất liệu và vị trí — mọi trường có nguồn | Mới |
| 4 | Bộ máy truy hồi | BM25 lai với reciprocal rank fusion, xếp hạng lại bằng lan truyền đồ thị, ba cổng từ chối | Đã xây |
| 5 | Mô hình đã tinh chỉnh và bộ điều hợp | Bộ điều hợp theo miền kèm cấu hình huấn luyện, luồng sinh dữ liệu và lý giải việc chọn checkpoint | Đã xây |
| 6 | Hỏi đáp có trích nguồn và từ chối | Chat tiếng Việt chỉ văn bản, tổ hợp bối cảnh, kiểm tra trích nguồn | Đã xây |
| 7 | Mô-đun cá nhân hóa | Hồ sơ sở thích có suy giảm, bộ gợi ý theo đường đi đồ thị với thưởng xuyên danh mục và đa dạng, đường đi giải thích | Mới |
| 8 | Mô-đun tư vấn chủ động | Bộ phân loại ý định sáu lớp, sổ đăng ký bộ sinh thẻ, bộ điều hợp thời tiết và điểm quan tâm, lời khuyên chuẩn bị theo luật | Mới |
| 9 | Giao diện dạng thẻ | Chat có thẻ có kiểu, trang khám phá và chi tiết, khởi tạo sở thích, bản đồ, sơ đồ bảo tàng | Mới |
| 10 | Công cụ quản trị và biên tập | Quản lý nội dung và bản ghi có kiểm tra nguồn, trạng thái rà soát, sổ kiểm toán, trang thống kê | Mới |
| 11 | Tập dữ liệu và bộ đánh giá | Tập câu hỏi cho truy hồi, trích xuất thực thể, trích nguồn, từ chối, ý định và độ liên quan gợi ý | Một phần |
| 12 | Báo cáo đánh giá | Toàn bộ chỉ số ở Mục 14.3 kèm phân tích lỗi và hạn chế đã nêu | Một phần |
| 13 | Bộ kiểm thử và CI | Kiểm thử đơn vị, tích hợp, API và đầu-cuối gồm phép khẳng định không-bịa-trường | Mới |
| 14 | Tài liệu kỹ thuật | Yêu cầu, kiến trúc, đặc tả API, lược đồ dữ liệu, hướng dẫn triển khai | Một phần |
| 15 | Báo cáo cuối và tài liệu trình diễn | Báo cáo, video, slide, hướng dẫn sử dụng, rà soát riêng tư và đạo đức | Kế hoạch |

### 14.3. Tiêu chí thành công và Chỉ số

Dự án thành công khi cả hai hành trình trình diễn ở Mục 12.4 hoàn tất đầu-cuối cho một người dùng đã xác thực có hồ sơ, và các chỉ số dưới đây được đo và báo cáo — bất kể có đạt mọi mục tiêu hay không. Một mục tiêu không đạt nhưng được đo và giải thích là một kết quả capstone chấp nhận được; một mục tiêu không được đo thì không.

| Chỉ số | Mục tiêu | Baseline / hiện tại |
| --- | --- | --- |
| recall@1 truy hồi, trong phạm vi | ≥ 95% | 68/70 |
| Từ chối ngoài phạm vi | ≥ 95% | 31/38 |
| Micro-F1 trích xuất thực thể | ≥ 0,75 | 0,786 (nhãn đang chờ người rà soát) |
| Độ trung thực trích nguồn | ≥ 85% | 0,704 — kỳ vọng cải thiện nhờ mở rộng kho ngữ liệu |
| Độ phủ trích nguồn trên câu trả lời được | ≥ 90% | 0,741 |
| Độ chính xác từ chối | ≥ 90% | 0,917 |
| Macro-F1 phân loại ý định | ≥ 85% trên 100 câu gán nhãn | Mới |
| Precision@5 của gợi ý | ≥ 70%, hai người đánh giá, báo cáo độ đồng thuận | Mới |
| nDCG@5 của gợi ý | Báo cáo, chưa đặt mục tiêu ở lần đo đầu | Mới |
| Tỷ lệ gợi ý xuyên miền | ≥ 30% trong năm mục đầu thuộc danh mục khác | Mới |
| Độ đúng trường của thẻ tư vấn | **100% — không trường nào bị bịa, khẳng định tự động** | Mới |
| Độ trễ đầu-cuối p95 | ≤ 8 giây | Chưa đo |
| Khả dụng | Thang SUS trên 6–8 người tham gia, báo cáo dạng định tính | Mới |

### 14.4. Các hạn chế đã biết cần nêu trong báo cáo cuối

Liệt kê ở đây thay vì để phát hiện tại buổi bảo vệ.

- **Chỉ một cặp địa bàn.** Mọi kết quả là cho Huế và Đà Nẵng. Ví dụ về một loại hình diễn xướng Nam Bộ mà giảng viên hướng dẫn nêu là *về mặt cấu trúc* được hỗ trợ — không có gì trong bộ gợi ý phụ thuộc vào vùng — nhưng *không trình diễn được*, vì kho ngữ liệu không chứa văn hóa Nam Bộ. Mục 16.3 ghi bảng đối chiếu cho thấy cơ chế chuyển được, và việc mở rộng vùng là hướng phát triển tương lai.
- **Quy mô đánh giá nhỏ.** Độ liên quan của gợi ý và khả dụng dựa trên hàng chục phán đoán, không phải hàng nghìn người dùng. Được báo cáo dạng định tính, kèm chỉ số đồng thuận.
- **Nhãn thực thể do máy điền trước**, và không có nhãn vàng nào cho loại sự kiện — tuyên bố bốn loại trên thực tế là ba loại.
- **Không có chỉ mục vector**, nên các truy vấn thuần diễn giải lại, không chia sẻ neo từ vựng hay neo đồ thị nào với kho ngữ liệu, sẽ thất bại. Các cổng từ chối làm cho thất bại này an toàn (hệ thống từ chối) nhưng đó vẫn là một hạn chế về recall.
- **Trích xuất tất định nghĩa là không có quan hệ ngữ nghĩa.** Đồ thị biết hai thực thể được nhắc cùng nhau, chứ không biết thực thể này xây nên thực thể kia. Vì vậy lời giải thích của gợi ý mang tính cấu trúc, không mang tính nhân quả.
- **Đồ thị trong RAM và mô hình trên một máy** giới hạn quy mô; cả hai là lựa chọn kiến trúc hợp lý ở kích thước hiện tại, không phải giải pháp tổng quát.
- **Bảng quy đổi âm lịch soạn thủ công** chỉ phủ các sự kiện thử nghiệm và khoảng thời gian trình diễn.
- **Chất lượng dữ liệu điểm quan tâm** phụ thuộc vào cộng đồng bản đồ tình nguyện và không đồng đều.

## 15. Tài liệu tham khảo

[1] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," NeurIPS 2020, arXiv:2005.11401. https://arxiv.org/abs/2005.11401

[2] Microsoft Research, "Project GraphRAG: LLM-Derived Knowledge Graphs." https://www.microsoft.com/en-us/research/project/graphrag/

[3] D. Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization," arXiv:2404.16130. https://arxiv.org/abs/2404.16130

[4] UNESCO, "Digital technologies in the culture sector," MONDIACULT. https://www.unesco.org/en/mondiacult/digital-technologies-culture-sector

[5] Google Arts & Culture, "About the project." https://artsandculture.google.com/

[6] Google Arts & Culture, "Explore collections and stories." https://artsandculture.google.com/explore

[7] E. J. Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models," ICLR 2022, arXiv:2106.09685. https://arxiv.org/abs/2106.09685

[8] S. Robertson và H. Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," Foundations and Trends in Information Retrieval, 2009. https://dl.acm.org/doi/10.1561/1500000019

[9] G. V. Cormack, C. L. A. Clarke và S. Buettcher, "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods," SIGIR 2009. https://dl.acm.org/doi/10.1145/1571941.1572114

[10] J. Carbonell và J. Goldstein, "The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries," SIGIR 1998. https://dl.acm.org/doi/10.1145/290941.291025

[11] Y. Zhang và X. Chen, "Explainable Recommendation: A Survey and New Perspectives," Foundations and Trends in Information Retrieval, 2020, arXiv:1804.11192. https://arxiv.org/abs/1804.11192

[12] Open-Meteo, "Free Weather API Documentation." https://open-meteo.com/en/docs

[13] OpenStreetMap Foundation, "Overpass API Documentation." https://wiki.openstreetmap.org/wiki/Overpass_API

[14] Scrum.org, "The 2020 Scrum Guide." https://scrumguides.org/scrum-guide.html

## 16. Bản ghi thay đổi phạm vi (v1.0 → v2.0)

Ghi tường minh để hội đồng kiểm chứng được rằng bốn năng lực được yêu cầu ở buổi phản biện được thêm vào bằng **đánh đổi**, không phải bằng cách phình thêm một kế hoạch 15 tuần vốn đã chặt.

### 16.1. Phần được thêm

| # | Năng lực được yêu cầu ở buổi phản biện | Giờ nằm ở đâu |
| --- | --- | --- |
| 1 | Cá nhân hóa theo từng người dùng; gợi ý xuyên miền suy ra từ sở thích | F05, F06, F07; FR06–FR09; NFR07; các chỉ số gợi ý ở 14.3 |
| 2 | AI như một tư vấn viên chủ động, đoán được nhu cầu thực tế chưa nói ra | F09; FR12–FR15; NFR06; các chỉ số ý định và thẻ ở 14.3 |
| 3 | Tra cứu và hiển thị chi tiết sự kiện văn hóa kèm thời gian, địa điểm, đơn vị tổ chức và cách thức tổ chức | F03, F14; các tập bản ghi sự kiện và địa điểm trong sản phẩm giao số 3 |
| 4 | Chatbot tương tác dạng thẻ thay cho tìm kiếm truyền thống | F09, F10; sản phẩm giao số 9; Tình huống A và B ở 12.4 |

### 16.2. Phần bị loại bỏ, kèm lý do

| Loại bỏ khỏi v1.0 | Lý do |
| --- | --- |
| Thư viện ảnh và luồng tải ảnh kèm ảnh thu nhỏ và metadata cho từng ảnh | Bốn năng lực được yêu cầu đều dựa trên văn bản và cấu trúc. Giữ lại một luồng CRUD ảnh sẽ tiêu tốn khoảng hai tuần mà lớp gợi ý và lớp tư vấn đang cần, trong khi không thêm gì cho bất kỳ lớp nào trong số đó. Thẻ hiển thị một ảnh tiêu biểu cho mỗi thực thể, nên điểm vào trực quan vẫn còn mà không cần luồng quản lý |
| Câu chuyện nhiều ảnh với mốc thời gian và đường camera | Bị thay thế về mặt chức năng bởi đường khám phá cá nhân hóa của F06 — thứ được sinh theo từng người thay vì soạn theo từng câu chuyện, và cũng chính là điểm khác biệt thật. Câu chuyện tuyến tính soạn tay sẽ tranh chấp cùng một khoảng giao diện với nó |
| Nạp DOCX | Kho ngữ liệu là văn bản bách khoa; không có nguồn DOCX nào đang dùng. Giữ làm hướng phát triển tương lai, không mất gì cho mục tiêu đo được nào |
| Chỉ mục vector riêng và mô hình embedding | Truy hồi lai đã hiện thực đạt recall@1 30/30 trong phạm vi, kể cả câu không dấu và câu dùng tên gọi khác. Thêm một chỉ mục mà không có khiếm khuyết đo được nào để khắc phục là không có cơ sở ở quy mô này. Ghi làm hướng phát triển tương lai và làm hạn chế đã nêu ở 14.4 |
| Phụ thuộc API LLM/embedding bên ngoài | Cả phân tích và sinh văn bản đều cục bộ. Loại bỏ rủi ro chi phí API của v1.0 và giữ văn bản kho ngữ liệu văn hóa ở lại trên máy |
| Bảng điều khiển quản trị đầy đủ như đặc tả ban đầu | Thu về quản lý nội dung và bản ghi có kiểm tra nguồn, trạng thái rà soát, sổ kiểm toán và một trang thống kê. Chức năng biên tập được giữ; phạm vi trình bày thì không |

Tác động thực lên ngân sách 15 tuần: thêm bốn nhóm năng lực, loại bỏ hoặc thu gọn sáu hạng mục phạm vi, và hạng mục rủi ro cao nhất — soạn thủ công các bản ghi có cấu trúc kèm nguồn — được dành một tuần riêng thay vì bị hấp thụ ngầm.

### 16.3. Ghi chú về miền ví dụ của giảng viên hướng dẫn

Ví dụ được thảo luận ở buổi phản biện dùng một loại hình diễn xướng Nam Bộ, với các gợi ý trải qua loại hình âm nhạc gắn với nó, trang phục truyền thống, và một ngôi nhà cổ — một minh họa cho gợi ý xuyên miền dẫn dắt bởi sở thích.

Cơ chế mà điều này đòi hỏi là độc lập với vùng: lan truyền trên quan hệ thành viên danh mục, đồng xuất hiện, và bối cảnh hành chính hoặc thời gian chung. Không có gì trong bộ gợi ý là riêng cho Huế hay Đà Nẵng. Tuy nhiên, kho ngữ liệu không chứa văn hóa Nam Bộ, và việc mở rộng sang vùng thứ ba sẽ đòi hỏi crawl lại, gán lại danh mục, sinh lại tập đánh giá và chạy lại mọi phép đo truy hồi — mất vài tuần, mà không thêm cơ chế mới nào.

Vì vậy cặp địa bàn thử nghiệm được giữ nguyên, nhất quán với quy tắc phạm vi một địa bàn, và cấu trúc tương đương được trình diễn ngay trong đó:

| Vai trò cấu trúc trong ví dụ của giảng viên | Tương đương trong kho ngữ liệu thử nghiệm |
| --- | --- |
| Một loại hình diễn xướng truyền thống làm điểm vào | Nhã nhạc cung đình, hát tuồng |
| Một loại hình âm nhạc hoặc nhạc cụ gắn liền | Các tài liệu diễn xướng liên quan trong cùng danh mục |
| Trang phục truyền thống hoặc văn hóa vật chất gắn liền | Bản ghi làng nghề và cổ vật |
| Một ngôi nhà cổ hoặc di tích để đến thăm | Các tài liệu di tích trong cùng đơn vị hành chính |
| Một nơi loại hình đó được trình diễn | Bản ghi địa điểm kèm tọa độ, và các sự kiện lễ hội có phần hội bao gồm loại hình đó |

Mở rộng vùng được liệt là hạng mục đầu tiên của hướng phát triển tương lai, và hạn chế này được nêu tường minh ở Mục 14.4 thay vì để hội đồng tự phát hiện.

## Danh mục kiểm tra trước khi nộp

| Hạng mục | Trạng thái |
| --- | --- |
| Tên dự án, thành viên và mã sinh viên đã điền | ☑ |
| Giảng viên hướng dẫn và đơn vị đã điền; email cần bổ sung | ☐ |
| Địa bàn/chủ đề thử nghiệm đã chọn — Huế và Đà Nẵng, sáu danh mục | ☑ |
| Quyền sử dụng nguồn và cách ghi công đã xác nhận | ☐ |
| Cơ sở dữ liệu, mô hình và công nghệ truy hồi đã chốt — PostgreSQL, Qwen2.5-3B cục bộ với LoRA, BM25 lai với xếp hạng lại bằng đồ thị, không dùng cơ sở dữ liệu vector | ☑ |
| Kho ngữ liệu mẫu và tập câu hỏi đánh giá đã tạo — 45 tài liệu, 349 đoạn, 76 mẫu vàng; mở rộng lên 80 tài liệu xếp ở Tuần 4 | ☑ một phần |
| Sơ đồ ngữ cảnh đã cập nhật thành 12 cặp yêu cầu/phản hồi, bỏ thực thể AI/LLM bên ngoài | ☑ |
| 3D đã xác nhận là hướng tương lai, không phải hạng mục bắt buộc của MVP | ☑ |
| Mục tiêu và tiêu chí chấp nhận đã rà soát đối chiếu baseline đã đo | ☑ |
| **Thay đổi phạm vi v2.0 đã chốt bằng văn bản với giảng viên hướng dẫn (Mục 16)** | ☐ **— hạng mục chặn ở Tuần 2** |
| Cách tiếp cận riêng tư và đồng ý cho việc ghi tương tác đã rà soát | ☐ |
| Định dạng cuối đã kiểm tra trước khi nộp | ☐ |
