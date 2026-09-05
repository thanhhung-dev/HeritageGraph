# Kế hoạch nâng cấp v1 → v2 — Dữ liệu thiếu, thay đổi mã, lộ trình

Tài liệu này trả lời đúng ba câu hỏi: **thiếu dữ liệu gì và lấy ở đâu**, **phải sửa/thêm mã nào**, **làm theo thứ tự nào trong 13 tuần còn lại**.

Đọc kèm: `docs/Project Title.md` (đề cương v2.0, tiếng Anh), `docs/Project Title (VI).md` (tiếng Việt), `docs/architecture.md` (kiến trúc as-built), `docs/metrics.md` (định nghĩa chỉ số).

Bốn năng lực cô yêu cầu:

| # | Năng lực | Trạng thái khả thi | Chặn chính |
| --- | --- | --- | --- |
| 1 | Cá nhân hóa theo người dùng, gợi ý xuyên miền | Khả thi cao | Chưa có DB/user; corpus lệch danh mục |
| 2 | Tư vấn viên AI chủ động | Khả thi trung bình | Thiếu toạ độ, lịch sự kiện, dữ liệu cổ vật |
| 3 | Tra cứu & hiển thị chi tiết sự kiện | Khả thi cao | Chỉ có 2 tài liệu lễ hội, không có bản ghi có cấu trúc |
| 4 | Chatbot dạng thẻ | Khả thi cao | Frontend hiện 1 trang, `components/` rỗng |

Nguyên tắc xuyên suốt, đặt trước mọi thứ khác vì nó quyết định toàn bộ thiết kế phần dưới:

> **LLM chỉ viết phần kể chuyện di sản. Mọi thẻ thực tế (thời tiết, bãi xe, lịch, cổ vật, gợi ý) được kết xuất tất định từ bản ghi có kiểu, không đi qua LLM.**

Lý do không phải khẩu hiệu. Thành tựu duy nhất bảo vệ được của dự án hiện nay là `refusal_accuracy 0.9167` và `citation_faithful_rate 0.7037` (`eval/report_lora.json`). Nếu để mô hình 3B tự nói về thời tiết và bãi xe, bạn tái tạo hallucination đúng ở chỗ vừa diệt xong, và mất luôn luận điểm chính. Nguyên tắc này cũng nhất quán với `backend/core/kg.py:1-21` (không dùng LLM lúc index vì LLM bịa entity) — sự nhất quán đó là điểm cộng khi bảo vệ.

---

## Phần 1 — DỮ LIỆU ĐANG THIẾU

Đây là phần bạn hỏi. Mỗi mục ghi rõ: hiện có gì, cần gì, **lấy ở đâu bên ngoài**, và tính năng nào chết nếu không có.

### 1.1. Tổng quan hiện trạng đã đo

Số liệu đo trực tiếp bằng `load_docs()` + `build_graph()`, không phải số trong README (README đang ghi 23 bài / 215 chunk — lạc hậu khoảng 2 lần):

```
45 tài liệu dùng được / 349 đoạn / 304.224 ký tự
Bỏ 2: 'Bánh xèo' (trùng nội dung 'Bánh khoái'), 'Đàn Nam Giao' (205 ký tự, trang định hướng)
Vùng:      Huế 30, Đà Nẵng 15
Danh mục:  Di tích 22, Ẩm thực 9, Danh thắng 6, Nghệ thuật 4, Lễ hội 2, Làng nghề 2
Đồ thị:    510 đỉnh / 1135 cạnh / 1 thành phần liên thông / 0 tài liệu cô lập / 0,23 giây
```

### 1.2. THIẾU #1 — Cân bằng danh mục corpus (chặn tính năng #1)

**Hiện có:** Nghệ thuật 4, Lễ hội 2, Làng nghề 2 tài liệu.

**Vấn đề:** Cô muốn gợi ý xuyên miền kiểu "cải lương → đàn ca tài tử → áo bà ba → nhà cổ". Với 4 tài liệu Nghệ thuật và 2 Làng nghề, bộ gợi ý chỉ có thể quay vòng trong Di tích (22 tài liệu). Cạnh `related` trong đồ thị chỉ nối được thứ đã có mặt. **Đây là chặn nghiêm trọng nhất cho tính năng #1**, và nó là chặn dữ liệu, không phải chặn thuật toán.

**Cần:** ≥ 8 tài liệu mỗi danh mục, tổng ~80 tài liệu. Tức thêm ~35 tài liệu, tập trung: Nghệ thuật +6, Lễ hội +8, Làng nghề +8, còn lại rải đều.

**Lấy ở đâu:**

| Nguồn | Nội dung | Cách lấy |
| --- | --- | --- |
| vi.wikipedia.org | Nghệ thuật, làng nghề, lễ hội, món ăn | `ingestion/crawl_wiki.py` đã chạy tốt (47/47 success), chỉ cần thêm tên vào `training/locations_hue_danang.py` |
| Cổng TTĐT TP Huế / TP Đà Nẵng | Danh mục lễ hội, làng nghề được công nhận | Trang danh mục → lấy tên → tra Wikipedia; nếu không có bài thì soạn tay kèm nguồn |
| Trung tâm Bảo tồn Di tích Cố đô Huế | Nhã nhạc, tuồng, lễ hội cung đình, di tích | Trang giới thiệu từng di tích |
| Cục Di sản văn hóa (dsvh.gov.vn) | Danh mục di sản phi vật thể quốc gia | Bộ lọc theo tỉnh → tên chính xác của lễ hội và nghề |
| UNESCO ich.unesco.org | Nhã nhạc (2003), hồ sơ di sản phi vật thể | Hồ sơ tiếng Anh/Việt, trích dẫn được |

**Gợi ý tên cụ thể để crawl** (kiểm tra tồn tại bài trước bằng `crawl_wiki.py resolve`):

- Nghệ thuật: Ca Huế, Hát bài chòi, Hò khoan, Múa Chăm, Rối cạn, Ca trù (nếu có nhánh Huế)
- Làng nghề: Làng nghề Non Nước (đá Ngũ Hành Sơn), Đúc đồng Phường Đúc, Nón lá Huế, Hoa giấy Thanh Tiên, Tranh làng Sình, Gốm Thanh Hà, Dệt Zèng A Lưới, Mộc Kim Bồng
- Lễ hội: Lễ hội Điện Huệ Nam, Lễ tế Xã Tắc, Lễ hội Quán Thế Âm, Lễ hội Đình làng Hải Châu, Lễ hội Làng Túy Loan, Lễ hội Đua thuyền Sông Hàn, Lễ hội Vía Bà, Hội đèn lồng
- Ẩm thực: Bánh ép, Chè hẻm Huế, Bún chả cá, Bánh tráng cuốn thịt heo, Ốc hút, Bánh canh Nam Phổ

**Điểm mạnh cần biết:** thêm tài liệu **không cần train lại mô hình**. LoRA dạy văn phong / trích nguồn / từ chối / NER, không dạy dữ kiện. Dữ kiện đến từ retrieval. Nên mở rộng corpus là ~1 ngày crawl + review, không phải 2,5 giờ train.

### 1.3. THIẾU #2 — Toạ độ địa lý (chặn toàn bộ tính năng #2)

**Hiện có:** không có lat/lon ở bất kỳ đâu trong repo. Đã kiểm tra `corpus/locations_index.json`, `corpus/resolve_map.json` — không có trường toạ độ.

**Vấn đề:** "Bãi gửi xe cách 200m", "điểm xem đẹp nhất", "trời có thể mưa" — cả ba đều cần một cặp toạ độ. Không có toạ độ thì tính năng #2 không tồn tại được, kể cả khi mã đã viết xong.

**Cần:** ≥ 50 bản ghi `venue` với `lat`, `lon`, `ward`, `district`.

**Lấy ở đâu:**

| Nguồn | Dùng cho | Ghi chú |
| --- | --- | --- |
| Nominatim (OSM) `https://nominatim.openstreetmap.org/search?q=...&format=json` | Mã hoá địa lý tên di tích → toạ độ | Miễn phí, không cần khoá. Giới hạn 1 req/s → chạy 1 lần rồi cache vào DB. Bắt buộc gửi User-Agent |
| Wikidata SPARQL / `wbgetclaims` | Toạ độ P625 cho di tích có bài Wikipedia | Chính xác hơn Nominatim cho di tích nổi tiếng. Đã có `pageid` trong `resolve_map.json` → tra được Wikidata QID |
| Infobox Wikipedia | Nhiều bài di tích Huế có sẵn toạ độ | Đang bị `clean_wiki_text()` bỏ đi; có thể parse riêng |
| Google Maps (xem thủ công) | Kiểm tra chéo và bù các chỗ hai nguồn trên sai | 50 điểm, ~1 giờ. Chỉ đọc toạ độ, không dùng API |

**Cách làm đề xuất:** Wikidata trước (chính xác nhất, có `pageid` sẵn) → Nominatim cho phần thiếu → mắt người kiểm 50 điểm trên bản đồ. Ghi nguồn toạ độ vào trường `source` của từng bản ghi.

### 1.4. THIẾU #3 — Bản ghi sự kiện/lễ hội có cấu trúc (chặn tính năng #3)

**Hiện có:** danh mục `Lễ hội` đúng 2 tài liệu (`Festival Huế`, `Lễ Cầu ngư`), toàn văn xuôi. Không có bảng ngày, không lịch âm, không đơn vị tổ chức, không phần lễ/phần hội.

**Vấn đề:** Ví dụ #3 của cô yêu cầu trả về chính xác: tên, thời gian (14/01–16/01 âm lịch), địa điểm (Làng chài Nam Ô, Q. Liên Chiểu), cách thức tổ chức (phần lễ: nghinh thần, cúng tế; phần hội: hát bài chòi, đua thuyền). **Không một trường nào trong số đó tồn tại dưới dạng dữ liệu hiện nay.**

**Cần:** ≥ 20 bản ghi `event` + `event_segment`, mỗi trường kèm `source_url` + `source_sentence`.

**Lấy ở đâu:**

| Nguồn | Trường lấy được |
| --- | --- |
| Cục Di sản văn hóa — danh mục di sản phi vật thể quốc gia | Tên chính thức, địa phương, năm công nhận, mô tả nghi lễ |
| Cổng TTĐT TP Đà Nẵng / TP Huế, mục Văn hoá – Lễ hội | Thời gian âm lịch, đơn vị tổ chức, địa điểm |
| Sở Du lịch Đà Nẵng / Huế — lịch sự kiện năm | Ngày dương lịch cụ thể của năm, ban tổ chức |
| Trung tâm Bảo tồn Di tích Cố đô Huế | Lễ hội cung đình, chi tiết nghi thức |
| Báo Đà Nẵng, Báo Thừa Thiên Huế (bài tường thuật lễ hội) | Phần lễ / phần hội, hoạt động cụ thể, số người dự |
| UBND phường/xã (nếu có trang) | Lễ hội cấp làng như Cầu ngư Nam Ô, Túy Loan |

**Cảnh báo về lịch âm:** đừng dùng thư viện. `lunardate` và tương tự theo lịch Trung Quốc, lệch múi giờ UTC+7/+8 nên đôi khi lệch 1 ngày — đúng loại lỗi mà hội đồng sẽ chỉ ra. Soạn tay bảng quy đổi cho ~20 lễ hội trong 2026–2027 (30 phút, đúng 100%), ghi thư viện vào future work.

### 1.5. THIẾU #4 — Bản ghi cổ vật (chặn ví dụ cổ vật của cô)

**Hiện có:** chữ `"cổ vật"` xuất hiện trong đúng 3 tệp — `Bảo tàng Cổ vật Cung đình Huế.txt` (14 lần), `Bảo tàng Điêu khắc Chăm Đà Nẵng.txt` (4 lần), `Chùa Thiên Mụ.txt` (1 lần). Toàn văn xuôi. Không có mã hiện vật, không niên đại, không chất liệu, không phòng trưng bày, không ảnh.

**Vấn đề:** Ví dụ của cô — tra "Tượng Phật thời Champa" → gợi ý Bảo tàng Điêu khắc Chăm + cổ vật cùng thời kỳ + đồ mô phỏng — cần một bảng hiện vật. Không có bảng thì chỉ trả về được đúng bài viết về bảo tàng.

**Cần:** ≥ 35 bản ghi `artifact` với `name`, `museum`, `period`, `material`, `room`, `floorplan_x/y`, `source_url`, `source_sentence`.

**Lấy ở đâu:**

| Nguồn | Nội dung |
| --- | --- |
| chammuseum.vn (Bảo tàng Điêu khắc Chăm) | Danh sách bảo vật quốc gia, tên hiện vật, niên đại, chất liệu, phòng trưng bày. Đây là nguồn tốt nhất cho phần Chăm |
| baotangcovatcungdinh.vn / hueworldheritage.org.vn | Hiện vật cung đình Huế, ngai vàng, kim phẩm, đồ sứ ký kiểu |
| Danh mục Bảo vật quốc gia (quyết định Thủ tướng, đăng trên Cục Di sản) | Danh sách chính thức + mô tả. Nguồn trích dẫn mạnh nhất cho báo cáo |
| Wikipedia: "Bảo vật quốc gia (Việt Nam)" | Bảng tổng hợp có thể đối chiếu |
| Nhãn hiện vật chụp tại bảo tàng | Nếu bạn đến được thì đây là nguồn chính xác nhất cho `room` và vị trí sơ đồ; đồng thời có ảnh dùng được |

**Sơ đồ bảo tàng:** không có nguồn số. Cách làm: chọn **đúng 1 bảo tàng** (Điêu khắc Chăm — có bảo vật quốc gia rõ ràng, phòng trưng bày phân theo khu vực Mỹ Sơn / Trà Kiệu / Đồng Dương nên dễ vẽ), vẽ SVG tay ~12 điểm nóng. Không cố làm hai bảo tàng.

### 1.6. THIẾU #5 — Điểm quan tâm: bãi xe, điểm quan sát, cửa hàng

**Hiện có:** không có gì.

**Lấy ở đâu:**

| Nguồn | Truy vấn |
| --- | --- |
| Overpass API (OSM) | `amenity=parking`, `shop=gift`, `shop=souvenir`, `amenity=restaurant`, `tourism=viewpoint` trong bán kính quanh toạ độ địa điểm |
| OSM trực tiếp | Miễn phí, không khoá. Cache mọi phản hồi |
| Soạn tay khi OSM thiếu | Rất có thể phải làm — xem cảnh báo dưới |

**Cảnh báo:** độ phủ OSM ở Việt Nam không đều. **Việc đầu tiên của Tuần 7 là kiểm tra thật** độ phủ `amenity=parking` quanh Nam Ô và Bảo tàng Chăm. Nếu thưa thì fallback bản ghi `poi` soạn tay kèm nguồn — đừng phát hiện điều này ở Tuần 10.

### 1.7. THIẾU #6 — Thời tiết

**Hiện có:** không có.

**Lấy ở đâu:** **Open-Meteo** `https://api.open-meteo.com/v1/forecast?latitude=..&longitude=..&hourly=precipitation_probability,temperature_2m`. Miễn phí, **không cần API key**, có `precipitation_probability` theo giờ — đúng thứ cần cho ý "trời có thể mưa thì mang áo mưa". Dự báo chỉ tới ~16 ngày, nên lễ hội xa hơn thì dùng `archive-api.open-meteo.com` lấy khí hậu trung bình cùng kỳ các năm trước và **ghi rõ trên thẻ đó là số liệu khí hậu, không phải dự báo**.

Luật "mang gì" viết thành ~15 rule trong YAML, không dùng LLM: `precip>40% → áo mưa`; `temp>33 → nước, nón`; `có phần lễ → trang phục lịch sự`; `đua thuyền → chọn chỗ cao`; `lễ hội đêm → đèn pin, đi sớm`.

### 1.8. THIẾU #7 — Người dùng, hồ sơ sở thích, lịch sử tương tác

**Hiện có:** **không có cơ sở dữ liệu nào.** Không Postgres, không SQLite, không Neo4j, không vector DB. Không model user, không login, không session. Toàn bộ trạng thái là tệp trên đĩa + một `@lru_cache` (`backend/core/retriever.py:449`).

Lưu ý: `docs/architecture.md:82-321` mô tả lược đồ Postgres 15 bảng (`app_user`, `chat_session`, `scene`, `story`, `hotspot`...) — **không tồn tại trong mã**. Không có `infra/docker-compose.yml`, không `PostgresRepository`, không migration. Tài liệu đó là thiết kế mục tiêu, không phải hiện trạng; phải sửa lại kẻo hội đồng đọc rồi hỏi.

**Cần:** Postgres + các bảng ở Phần 2.2. Cá nhân hóa không thể tồn tại nếu không có lớp này.

**Kèm theo là lỗ bảo mật:** `backend/app.py` bind `0.0.0.0:8000`, `/api/chat` hoàn toàn không xác thực. Hiện tại vô hại (chưa có dữ liệu cá nhân). Khi bắt đầu lưu hành vi người dùng thì thành vấn đề thật → **xác thực phải xong TRƯỚC khi lưu dữ liệu cá nhân đầu tiên**, không phải sau.

### 1.9. Bảng tổng hợp dữ liệu thiếu

| # | Thiếu | Chặn tính năng | Nguồn ngoài | Công |
| --- | --- | --- | --- | --- |
| 1 | ~35 tài liệu để cân bằng danh mục | #1 | Wikipedia, Cục Di sản, cổng TTĐT tỉnh | 1 ngày |
| 2 | ≥50 toạ độ địa điểm | #2 | Wikidata P625, Nominatim, kiểm bằng mắt | 0,5 ngày |
| 3 | ≥20 bản ghi sự kiện + phần lễ/hội | #3 | Cục Di sản, Sở Du lịch, báo địa phương | 1,5 ngày |
| 4 | ≥35 bản ghi cổ vật | #2 | chammuseum.vn, danh mục Bảo vật quốc gia | 1 ngày |
| 5 | Bãi xe / điểm quan sát / cửa hàng | #2 | Overpass OSM + soạn tay khi thiếu | 0,5 ngày |
| 6 | Thời tiết | #2 | Open-Meteo (không cần khoá) | Chỉ code |
| 7 | User + hồ sơ + lịch sử | #1 | Không cần nguồn ngoài — cần Postgres | Xem 2.2 |
| 8 | Sơ đồ 1 bảo tàng + ~12 điểm nóng | #4 | Vẽ SVG tay | 0,5 ngày |

Tổng nhập liệu: khoảng một tuần làm việc. Đó là lý do Tuần 4 được dành trọn cho dữ liệu — nếu coi đây là việc làm kèm thì nó sẽ trượt và kéo theo cả ba lớp phía trên.

**Quy tắc không nhượng bộ:** mọi trường sự kiện/địa điểm/cổ vật bắt buộc có `source_url` + `source_sentence`. Bản ghi thiếu nguồn bị API từ chối ở mức trường. Nếu bỏ quy tắc này, bạn mất chính cái kỷ luật trích nguồn đang là xương sống của dự án — và mất luôn khả năng nói "0 trường bịa" trước hội đồng.

---

## Phần 2 — THAY ĐỔI MÃ NGUỒN

### 2.1. Giữ nguyên, không sửa

Đây là phần đã đo được và là đóng góp của dự án. Không chạm vào:

| Thành phần | Vì sao giữ |
| --- | --- |
| `backend/core/retriever.py` — BM25×2 + RRF + rerank đồ thị | recall@1 30/30 kể cả câu không dấu và alias |
| `backend/core/kg.py` — dựng đồ thị tất định, `expand_docs()`, `find_seeds()` | 0,23 giây; `expand_docs()` chính là hàm bộ gợi ý sẽ dùng lại |
| `backend/core/rag.py:89-104` — ba cổng từ chối | `refusal_accuracy 0.9167`. **Không bao giờ cắt** |
| `backend/core/prompt.py` — SYSTEM | Nguồn duy nhất của văn phong + định dạng trích nguồn, dùng chung train/serve/eval |
| `models/lora-serve/` checkpoint `0000200` | Đã chọn theo val loss 0.414 thay vì 0.473 ở bước 720 |
| `backend/core/corpus.py` — chunking | Nguồn duy nhất, dùng chung train và serve |
| `backend/core/nerlabel.py` | Có bộ chặn tên ghép, dòng họ, assertion lúc import |

### 2.2. Thêm mới — Cơ sở dữ liệu (Tuần 3)

Postgres 16 + SQLAlchemy + Alembic + `infra/docker-compose.yml`. Chọn Postgres vì `docs/Project Title.md` §10 đã ghi Postgres từ v1.0 — khớp đặc tả của chính mình tốn ~2 giờ và tránh một câu hỏi ở hội đồng.

```
app_user(id, email, password_hash /* argon2id */, created_at, consent_at)
user_interest(user_id, node_id, weight, source /* onboarding|implicit */, updated_at)
interaction_event(id, user_id, kind /* view|dwell|click|save|dismiss */,
                  target_node_id, dwell_ms, ts)
recommendation_log(id, user_id, seed_node, item_node, reason_path,
                   rank, shown_at, clicked_at)

venue(id, doc_node, lat, lon, ward, district, source_url, source_sentence)
event(id, name, doc_node, calendar /* lunar|solar */, start_date, end_date,
      organizer, venue_id, source_url, source_sentence)
event_segment(id, event_id, phase /* lễ|hội */, name, description, ord,
              source_url, source_sentence)
artifact(id, name, museum_doc, period, material, room,
         floorplan_x, floorplan_y, source_url, source_sentence)
poi(id, kind /* parking|viewpoint|shop|food */, name, lat, lon,
    venue_id, source /* osm|manual */, fetched_at)

audit_log(id, user_id, action, target, before, after, ts)
```

Ràng buộc mức DB: `venue`, `event`, `event_segment`, `artifact` có `NOT NULL` trên `source_url` và `source_sentence`. Không dựa vào tầng ứng dụng để nhớ quy tắc này.

### 2.3. Thêm mới — Xác thực (Tuần 3, TRƯỚC dữ liệu cá nhân)

- `backend/api/auth.py`: `POST /api/auth/register`, `/login`, `/logout`, `GET /api/auth/me`
- argon2id (`argon2-cffi`), JWT trong cookie HttpOnly + SameSite=Lax
- Dependency `current_user` cho mọi endpoint đọc/ghi dữ liệu cá nhân
- Sửa `backend/core/config.py:44`: `BACKEND_HOST` đổi `0.0.0.0` → `127.0.0.1` cho cấu hình demo
- `POST /api/me/export` và `DELETE /api/me/data` (FR19) — làm luôn ở Tuần 3, đừng để Tuần 14

### 2.4. Thêm mới — Bộ gợi ý (Tuần 5–6)

`backend/core/recommend.py`. Đây là phần đáng gọi là đóng góp học thuật.

```python
score(d) = α · GraphAffinity(seed, d)          # expand_docs() — đã có
         + β · ProfileAffinity(interests, d)   # cùng hàm, seed = hồ sơ
         + γ · CrossDomainBonus(seed, d)       # +bonus nếu KHÁC category NHƯNG có path thật
         − δ · Seen(d)                          # từ interaction_event
→ MMR để tránh 5 cái lăng liên tiếp
```

Ba điểm thiết kế quan trọng:

**Mỗi gợi ý mang theo đường đi sinh ra nó.** `reason_path` kiểu: `Hát tuồng → [in_category] Nghệ thuật → [in_category] Nhã nhạc cung đình Huế`. Đây là điểm khác biệt so với sản phẩm thị trường — collaborative filtering là hộp đen, không giải thích được. Trong bối cảnh di sản và giáo dục, không giải thích được là **lỗi**, không phải khiếm khuyết hình thức. Đó mới là câu trả lời mạnh cho câu hỏi "khác gì thị trường", chứ không phải bản thân chữ "cá nhân hóa".

**`CrossDomainBonus` là định nghĩa máy móc của yêu cầu của cô.** Thưởng cho ứng viên đến được bằng đường đi thật *nhưng thuộc danh mục khác*. Đây chính là "cải lương → áo bà ba" ở dạng công thức. Và nó cho ra một chỉ số đo được: **cross-domain rate** ≥ 30% trong top-5.

**Khởi động nguội:** onboarding chọn 3 danh mục + 3 mục cụ thể → seed hồ sơ. Sau đó ngầm định: view +1, dwell>20s +2, click thẻ +2, save +3, dismiss −2, suy giảm nửa chu kỳ 14 ngày. Không có hồ sơ thì β = 0, chỉ dùng độ gần với chủ đề đang xem.

API: `GET /api/recommend?seed=<node>&k=5` → `[{node, label, category, score, reason_path}]`

### 2.5. Thêm mới — Nhận diện ý định (Tuần 7)

Mở rộng `query_intent()` (`backend/core/retriever.py:113`, hiện trả `{location, time, verify, ward}`) thành 6 lớp: `research | attend_event | plan_trip | learn | compare | verify`.

**Dùng regex + từ vựng, KHÔNG fine-tune.** Sáu lớp, tiếng Việt, regex đạt >90% và kiểm toán được — quan trọng hơn là giải thích được ở hội đồng. Fine-tune cho việc này là thêm một biến số không đo được vào một dự án đã đủ biến số.

Đo bằng 100 câu gán nhãn tay, báo cáo macro-F1 + confusion matrix.

### 2.6. Thêm mới — Lớp tư vấn (Tuần 7–8)

`backend/core/advisor.py` — sổ đăng ký `intent → [card_generator]`:

| Ý định | Thẻ kết xuất |
| --- | --- |
| `research` | `ArtifactCard`, `MuseumCard`, `SamePeriodCard`, `RelatedCraftCard` |
| `attend_event` | `ScheduleCard`, `VenueMapCard`, `WeatherCard`, `PrepChecklistCard`, `ViewpointCard`, `ParkingCard` |
| `plan_trip` | `VenueMapCard`, `NearbyCard`, `FoodCard`, `WeatherCard` |
| `learn` | `NarrationBlock` + `RelatedCard` |
| `compare` | `ComparisonTableCard` |
| `verify` | `CorrectionBlock` (đã có sẵn qua fine-tune) |

Bộ điều hợp ngoài: `backend/adapters/weather.py` (Open-Meteo), `backend/adapters/osm.py` (Overpass + Nominatim, cache vào bảng `poi`), `backend/core/prep_rules.yaml` (~15 luật).

**Kỹ thuật ẩn độ trễ:** `asyncio.gather` để gọi API ngoài **song song** với `generate_response()`. Mô hình 3B sinh 768 token mất vài giây; API thời tiết mất ~300ms. Chồng lên nhau thì độ trễ ngoài biến mất hoàn toàn khỏi p95.

**Suy giảm mềm:** API chết → thẻ ghi "không có dữ liệu dự báo", **không bao giờ đoán**. Đây là một ca kiểm thử, không phải một nhánh xử lý lỗi.

Mỗi thẻ mang `provenance`: `corpus | db | graph | external:open-meteo | external:osm` + `fetched_at`.

### 2.7. Sửa — Response schema `/api/chat` (Tuần 3)

`backend/api/chat.py:20-22` hiện là `{answer, sources}`. Thành:

```python
class ChatResponse(BaseModel):
    answer: str                    # giữ nguyên — không phá frontend cũ
    sources: list[dict] = []       # giữ nguyên
    blocks: list[Block] = []       # MỚI: các thẻ có kiểu
    intent: str | None = None      # MỚI
    recommendations: list[Rec] = []# MỚI
```

Cộng thêm chứ không thay thế → frontend hiện tại vẫn chạy trong khi bạn xây cái mới.

### 2.8. Frontend (Tuần 9–10)

Hiện trạng: `frontend/app/page.tsx` **88 dòng là toàn bộ ứng dụng**. `components/`, `lib/`, `public/` rỗng hoàn toàn. Không Tailwind, không state library, không HTTP client.

Ba lỗi lệch phải sửa luôn:
- `frontend/app/page.tsx:48` quảng cáo "Qwen2.5-7B" — thực tế là **3B**
- Hardcode `http://localhost:8000` thay vì dùng `NEXT_PUBLIC_API_URL` đã khai báo trong `.env.local.example`
- Type `Source` khai `{text, score?, entity?}` nhưng backend trả `{text, score, doc, heading, url, chunk_id, graph, graph_hits, used_in_context}` → `url` và `doc` đang bị bỏ im lặng

Cần thêm: Tailwind; `components/blocks/` với registry `type → component`; trang `/onboarding`; trang `/explore/[node]` có rail "liên quan" kèm lý do; Leaflet cho bản đồ; SVG sơ đồ bảo tàng; `aria-live` trên khung hội thoại (hiện không có gì cho accessibility).

### 2.9. Kiểm thử (Tuần 12–13)

Hiện tại: **không có framework kiểm thử nào, không CI.** Cần pytest + Playwright + GitHub Actions.

Ca kiểm thử quan trọng nhất của cả dự án:

```python
def test_no_fabricated_card_fields():
    """Mọi trường của mọi thẻ phải khớp bản ghi nguồn hoặc phản hồi API."""
    for card in all_generated_cards(TEST_QUERIES):
        for field, value in card.data.items():
            assert value == source_record_of(card)[field], \
                f"Trường bịa: {card.type}.{field}"
```

Đây là thứ biến nguyên tắc kiến trúc thành bằng chứng. Không có nó thì "0 trường bịa" chỉ là một lời tuyên bố.

---

## Phần 3 — LỘ TRÌNH 13 TUẦN

Hôm nay 05/09/2026, deadline 06/12/2026.

### Tuần 2 (tuần này, 4 ngày) — Chốt phạm vi + trả nợ đo lường

**Đây là bước quan trọng nhất. Đừng code trước bước này.**

1. **Sửa số liệu lạc hậu** trong `README.md` và `docs/architecture.md`: 23 tài liệu/215 chunk → **45/349**; 331 đỉnh/563 cạnh → **510/1135**; train 169/38 → **480/137**; `frontend/app/page.tsx:48` 7B → **3B**. Cả hai tài liệu đều tự tuyên bố "số liệu ĐO ĐƯỢC" nên sai số này là lỗi đáng bị hỏi.

2. **Sửa lỗi rò rỉ.** `eval/eval_retrieval.py` **hiện exit 1**: câu "Đàn Nam Giao thờ ai?" rò rỉ 1193 ký tự bối cảnh sai, vì đồ thị có đỉnh entity cho một tài liệu đã bị `corpus.py` loại (205 ký tự, trang định hướng). Sửa: bỏ đỉnh đồ thị của tài liệu không usable.

3. **Chạy lại mô hình gốc** trên `eval/gold.jsonl` 76 mẫu hiện tại. Hiện `report_base.json` đo trên **32 mẫu / corpus 23 bài**, `report_lora.json` trên **76 mẫu / corpus 45 bài** → trình bày 0.08 → 0.7861 như một phép so sánh có kiểm soát là **không bảo vệ được**. Hội đồng sẽ hỏi đúng chỗ này.

4. **Ghi checkpoint bộ điều hợp vào `report_*.json`.** `training/score_gold.py` chỉ ghi `args.model`, nên tệp báo cáo không cho biết nó đo `0000200` — vi phạm NFR14 (tái lập).

5. **Trình cô `docs/Project Title (VI).md` §16** — bảng thêm/bớt và bảng đối chiếu cải lương→Huế. **Lấy xác nhận bằng văn bản về phần cắt.** Đây là hạng mục chặn: không có nó thì mọi tuần sau đều rủi ro.

### Tuần 3 — Nền tảng
Postgres + docker-compose + Alembic; SQLAlchemy models; auth argon2id + JWT cookie; middleware ghi `interaction_event` (có consent); Tailwind; response schema v2; `/api/me/export` + `/api/me/data`. **Đo p95 latency ngay tuần này** — NFR01 ≤ 8s với 3B cục bộ + `MAX_TOKENS=768` là sát, đừng để Tuần 12 mới biết.

### Tuần 4 — Dữ liệu miền (xem Phần 1)
Crawl ~35 tài liệu cân bằng danh mục; nhập 50 venue + toạ độ, 20 event + segment, 35 artifact; dựng lại đồ thị; sinh lại gold set; chạy lại eval retrieval. **Cổng vào Tuần 5:** mọi danh mục ≥ 8 tài liệu. → **Xong tính năng #3**

### Tuần 5–6 — Cá nhân hóa
Hồ sơ + onboarding + decay; `recommend.py`; `/api/recommend` trả `reason_path`; `recommendation_log`; trang onboarding + trang chi tiết có rail liên quan. → **Xong tính năng #1**

### Tuần 7–8 — Tư vấn chủ động
**Việc đầu tiên Tuần 7: kiểm tra độ phủ OSM** quanh Nam Ô và Bảo tàng Chăm — nếu thưa thì fallback POI soạn tay ngay, đừng để phát hiện ở Tuần 10. Rồi: intent classifier + 100 câu gán nhãn; NBA registry; Open-Meteo; Overpass + cache; `prep_rules.yaml`; `asyncio.gather`. → **Xong tính năng #2**

### Tuần 9–10 — Giao diện thẻ + sơ đồ
Block renderer registry; Leaflet; **đúng 1 bảo tàng**, SVG tay + ~12 điểm nóng; action "xem vị trí trong sơ đồ"; rà soát accessibility. → **Xong tính năng #4**

### Tuần 11 — Hai hành trình + đệm
Hành trình nghiên cứu (cổ vật → bảo tàng → cùng thời kỳ → làng nghề) và hành trình tham dự (lễ hội → lịch → địa điểm → thời tiết → chuẩn bị → điểm quan sát → bãi xe). Hấp thụ trượt tiến độ.

### Tuần 12–13 — Kiểm thử + đo
pytest + Playwright + CI; test không-bịa-trường; toàn bộ chỉ số; **precision@5 với 2 người đánh giá + Cohen's κ**; user study 6–8 người (SUS); streaming nếu p95 fail.

### Tuần 14–15 — Tài liệu, video, slide, báo cáo, rà soát riêng tư
Khi đã lưu hành vi người dùng thì consent + tối giản dữ liệu + endpoint xoá trở thành **bắt buộc**, không còn optional như trong đề cương v1.0.

---

## Phần 4 — ĐO LƯỜNG

Giữ 4 chỉ số cũ (`docs/metrics.md`), thêm:

| Chỉ số | Cách đo | Vì sao cần |
| --- | --- | --- |
| Intent macro-F1 | 100 câu gán nhãn + confusion matrix | Chứng minh lớp tư vấn kích hoạt đúng |
| Recommendation P@5 / nDCG@5 | 25 seed × 5 gợi ý, **2 người đánh giá, báo cáo Cohen's κ** | Không có κ thì hội đồng bắt bài ngay: một người tự đánh giá recommender của chính mình không phải bằng chứng |
| Cross-domain rate | % top-5 khác category seed, mục tiêu ≥30% | Số chứng minh "không phải gợi ý thêm cái tương tự" — đây là ý cô |
| Intra-list diversity | Entropy danh mục trong top-5 | Chống thoái hoá về 5 cái lăng |
| Card field correctness | Assert tự động, mục tiêu **100%** | Biến nguyên tắc kiến trúc thành bằng chứng |
| p95 latency | Đo từ Tuần 3 | NFR01, hiện chưa đo |
| SUS | 6–8 người | Ghi rõ là định tính, không phải kết quả thống kê |

---

## Phần 5 — RỦI RO & THỨ TỰ CẮT

Rủi ro lớn nhất **không phải kỹ thuật, là phạm vi**. Đề cương v1.0 đã có 14 sản phẩm giao, xong ~4, và rủi ro #15 trong chính đề cương của bạn là "phạm vi vượt 15 tuần". Giờ thêm 4 nhóm tính năng với 1 người. Cách duy nhất là chốt phần cắt với cô ngay tuần này (§16.2 của đề cương v2.0 đã viết sẵn lý do cho từng mục cắt).

**Thứ tự cắt khi trượt tiến độ** (quyết trước để không phải phán đoán dưới áp lực):
1. Điểm nóng sơ đồ bảo tàng → giữ ảnh sơ đồ tĩnh
2. POI cửa hàng/quà → giữ bãi xe + điểm quan sát
3. User study 8 → 4 người
4. Giao diện quản trị → CLI + 1 trang thống kê chỉ đọc
5. Corpus 80 → 65 tài liệu, **giữ nguyên mức tối thiểu mỗi danh mục**

**Không bao giờ cắt:** ba cổng từ chối, trích nguồn bắt buộc, assert không-bịa-trường, bộ đánh giá. Đó là đóng góp của dự án; thiếu chúng thì đây chỉ là một bản demo không kiểm chứng được.

---

## Phần 6 — VỀ VÍ DỤ CẢI LƯƠNG CỦA CÔ

Phải nói lại với cô, và §16.3 của đề cương v2.0 đã viết sẵn phần này để bạn trình bày.

**Cải lương không thuộc corpus.** Cải lương và đàn ca tài tử là Nam Bộ; Nhà cổ Huỳnh Thủy Lê ở Đồng Tháp. Corpus hiện tại là Huế + Đà Nẵng (30/15).

**Cơ chế thì chuyển được, dữ liệu thì không.** Không có gì trong `recommend.py` phụ thuộc vào vùng — nó lan truyền trên `in_category`, `mentions`, `in_ward`, `year`, `related`. Mở sang Nam Bộ = crawl lại, gán lại danh mục, sinh lại gold set, chạy lại toàn bộ eval — vài tuần, mà **không thêm một cơ chế mới nào**.

**Đề xuất:** giữ 1 cặp địa bàn (đúng in-scope "one locality/theme" của đề cương v1.0), demo *cơ chế* bằng ví dụ Huế, và đưa cô bảng đối chiếu chứng minh ví dụ của cô chạy được về mặt cấu trúc:

| Vai trò trong ví dụ của cô | Tương đương trong corpus |
| --- | --- |
| Cải lương (loại hình diễn xướng làm điểm vào) | Nhã nhạc cung đình Huế, Hát tuồng |
| Đàn ca tài tử (âm nhạc gắn liền) | Tài liệu diễn xướng cùng danh mục Nghệ thuật |
| Áo bà ba (trang phục / văn hoá vật chất) | Bản ghi làng nghề (nón lá, dệt Zèng) + cổ vật |
| Nhà cổ Huỳnh Thủy Lê (di tích để thăm) | Di tích cùng đơn vị hành chính, qua cạnh `in_ward` |
| Điểm diễn cải lương gần đó | Bản ghi `venue` + `event` có phần hội gồm loại hình đó |

Điểm quan trọng khi trình bày: cô yêu cầu **cơ chế** (input → suy luận sở thích → gợi ý xuyên miền), và cơ chế đó được hiện thực đầy đủ. Việc corpus là Huế thay vì Nam Bộ là một hạn chế về phạm vi dữ liệu, được nêu tường minh ở §14.4 của đề cương thay vì để hội đồng tự phát hiện. "Hát tuồng" chỉ là một ví dụ minh hoạ — điểm vào có thể là cổ vật, món ăn, làng nghề hay lễ hội, và §12.4 của đề cương v2.0 cố tình chọn cổ vật và lễ hội làm hai hành trình demo chính, đúng như cô nói: văn hoá thì nhiều thứ, không chỉ diễn xướng.
