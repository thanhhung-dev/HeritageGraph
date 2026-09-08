---
stepsCompleted:
  - step-01-validate-prerequisites
inputDocuments:
  - prds/prd-HeritageGraph-2026-09-08/prd.md
  - prds/prd-HeritageGraph-2026-09-08/addendum.md
  - ../../docs/architecture.md
  - ../../docs-output/specs/spec-heritagegraph-v2/SPEC.md
  - ../../docs-output/specs/spec-heritagegraph-v2/companions (features.md, fr-catalog.md, metrics-targets.md, architecture-principles.md, schedule.md)
---

# HeritageGraph - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for HeritageGraph, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

> **Ghi chú phạm vi:** PRD `prd-HeritageGraph-2026-09-08` là SRS chính thức (chuyển thể từ proposal-vi v2.0 + upgrade-plan, giữ nguyên mã FR/NFR để truy vết). Nó **mở rộng** so với spec `spec-heritagegraph-v2` (chuyển thể từ đề cương): thêm kênh vector pgvector (FR12), trang Tapestry + 3D + audio (FR23, FR28–FR30), hạ tane Antd. Khi xung đột, PRD thắng. Dự án brownfield — không starter template.

## Requirements Inventory

### Functional Requirements

- FR01: Đăng ký, xác thực, quản lý tài khoản — mật khẩu chỉ lưu băm argon2id; phiên qua cookie HttpOnly (JWT, SameSite=Lax); endpoint được bảo vệ từ chối yêu cầu chưa xác thực; máy chủ demo bind 127.0.0.1
- FR02: CRUD tài liệu kho ngữ liệu — chuẩn hóa, tách đoạn kèm định vị nguồn; đồ thị dựng lại với đỉnh mới liên kết về nguồn
- FR03: CRUD bản ghi có cấu trúc — venue (tọa độ), event (loại lịch, phần lễ/hội), artifact (niên đại, chất liệu, bảo tàng, phòng), media_asset (giấy phép, người đóng góp, URL gốc); thiếu `source_url`/`source_sentence` bị từ chối **ở mức DB** kèm lỗi mức trường
- FR04: Trích xuất thực thể/quan hệ/hành chính/năm — tất định, khớp lược đồ 4 loại, mọi tên là chuỗi con nguyên văn của nguồn
- FR05: Dựng + cập nhật đồ thị — đỉnh/cạnh tạo, gán kiểu, gán trọng số, liên kết về nguồn; không quan hệ nào tạo mà thiếu chuỗi nguồn
- FR06: Rà soát kết quả trích xuất — thay đổi ghi audit_log kèm giá trị trước/sau
- FR07: Suy ra hồ sơ sở thích mà không yêu cầu khai — nền tảng dùng đầy đủ trước khi có hồ sơ; sau vài tìm/xem đầu tiên hồ sơ đã có sở thích có trọng số
- FR08: Ghi tương tác ngầm định, xem/sửa được — view/dwell/click/save/dismiss kèm mốc thời gian + đỉnh đích; trọng số suy giảm theo thời gian; người dùng thấy từng sở thích kèm hành vi sinh ra nó
- FR09: Gợi ý kèm đường đi đồ thị — mỗi mục kèm `reason_path`; `GET /api/recommend?seed=<node>&k=5` → `[{node, label, category, score, reason_path}]`
- FR10: Gợi ý xuyên danh mục — ≥1 trong 5 gợi ý đầu thuộc danh mục khác; gate Sprint 2: mọi danh mục ≥8 tài liệu
- FR11: Đa dạng — 5 mục đầu ≤3 mục cùng danh mục, trừ khi số danh mục tiếp cận được ít hơn
- FR12: Truy hồi đúng đoạn bất kể biến thể ngôn ngữ — 3 kênh (BM25 từ, BM25 n-gram không dấu, vector pgvector dim 1024) hợp nhất RRF; recall@1 ≥95%; bảng tách kênh; endpoint truy vết phơi hạt giống, hạng từng kênh, các cổng
- FR13: Xếp hạng lại theo hồ sơ — hai người dùng hồ sơ khác nhau nhận thứ tự khác nhau; khác biệt truy nguyên về trọng số hồ sơ
- FR14: Chat chỉ văn bản, trả lời chỉ từ bối cảnh đã truy hồi
- FR15: Trích nguồn hoặc phát biểu thiếu bằng chứng — mỗi câu khẳng định kèm `[Nguồn: <câu nguyên văn> — <url>]`; url phải hiển thị ở frontend
- FR16: Đính chính giả định sai — giả định trái nguồn → đính chính ngay câu đầu (≥90%)
- FR17: Phân loại ý định — 6 lớp (research/attend_event/plan_trip/learn/compare/verify); regex + từ vựng, không fine-tune; macro-F1 ≥85% trên ≥100 câu gán nhãn tay
- FR18: Thẻ khớp sổ đăng ký — mọi trường thẻ = đúng trường bản ghi nguồn hoặc phản hồi API, không trường nào do sinh ra; assert tự động 100%; thẻ mang provenance + fetched_at
- FR19: Lịch sự kiện — tên, loại lịch, ngày (âm lịch quy đổi soạn tay, không thư viện), địa điểm kèm tọa độ, đơn vị tổ chức, phần lễ + phần hội
- FR20: Thời tiết + danh mục chuẩn bị — Open-Meteo theo tọa độ; checklist sinh bằng ~15 luật tường minh trong `prep_rules.yaml`; lễ xa hơn 16 ngày → khí hậu trung bình cùng kỳ, thẻ ghi rõ "khí hậu, không phải dự báo"
- FR21: POI gần địa điểm — bãi xe, điểm quan sát, cửa hàng nghề/quà; Overpass + cache vào bảng poi; kiểm độ phủ OSM đầu Tuần 8; thưa → fallback POI soạn tay
- FR22: Địa điểm & lịch mở cửa — tên, địa chỉ, giờ mở, giá vé từ bản ghi F03; cổ vật thêm bảo tàng + phòng trưng bày
- FR23: Trang chi tiết Tapestry — ảnh lớn trái, danh sách story phải; kể chuyện, audio, chip liên kết, dòng thời gian, thực thể liên quan, dải nội dung liên quan
- FR24: Endpoint truy vết — phơi hạt giống, hạng từng kênh, độ gần đồ thị, thành phần cho điểm, kết quả từng cổng từ chối
- FR25: Hồ sơ + dữ liệu cá nhân trong trang tài khoản — hồ sơ kèm hành vi sinh ra từng sở thích, bỏ/tắt được; xuất tệp máy đọc được; xóa vĩnh viễn cả hồ sơ lẫn interaction_event. Không thể bị cắt
- FR26: Dashboard sức khỏe — số tài liệu/danh mục, thống kê đồ thị, trường thiếu nguồn, hàng chờ rà soát, chỉ số mới nhất
- FR27: Toàn bộ bộ đánh giá chạy được — mọi chỉ số tính và xuất báo cáo ghi: mô hình, checkpoint bộ điều hợp, phiên bản prompt, phiên bản kho ngữ liệu, cấu hình
- FR28: 3D + audio — .glb từ R2 qua Three.js; xoay, phóng, chuyển story, chuyển ngữ; mỗi audio có transcript đầy đủ
- FR29: Nguồn gốc tài sản — media_asset lưu khóa kho, người đóng góp, ngày, giấy phép, URL nguồn gốc; thiếu → từ chối tại biên endpoint
- FR30: Script audio có bằng chứng — mỗi câu khẳng định transcript truy về được câu nguồn hoặc đánh dấu lời dẫn dắt biên tập; kiểm tra tự động chặn tổng hợp giọng nói nếu không đạt

### NonFunctional Requirements

- NFR01: p95 đầu-cuối ≤8 giây (câu hỏi tiêu chuẩn, môi trường demo), đo liên tục từ Sprint 1
- NFR02: Gợi ý + thẻ trong 2 giây (không tính sinh mô hình); API ngoài chạy song song
- NFR03: Trang chi tiết ≤3 giây (đệm đồ thị, ảnh thu nhỏ)
- NFR04: recall@1 ≥95% kể cả không dấu/tên khác/diễn giải; recall riêng tập diễn giải báo cáo tách
- NFR05: Trung thực trích nguồn ≥85%; độ phủ trích nguồn ≥90%
- NFR06: 0 trường bịa trong thẻ tư vấn — assert tự động
- NFR07: Từ chối ≥90%; trả lời bịa ngoài phạm vi = lỗi; báo cáo cùng NFR04
- NFR08: Mọi gợi ý phơi đường đi qua tooltip; mọi truy hồi kiểm tra qua endpoint
- NFR09: Lần đầu hỏi + nhận gợi ý ngay lập tức — không onboarding, không bảng khai
- NFR10: WCAG 2.1 AA phần áp dụng được: alt-text, tương phản, bàn phím, transcript cho audio, mô tả 3D
- NFR11: Xác thực mọi endpoint cá nhân; kiểm tra đầu vào; không đường ghi không xác thực; không mở mạng công khai
- NFR12: Đồng ý trước khi ghi; chỉ lưu tối thiểu; xuất + xóa (không thể cắt)
- NFR13: Mọi phát biểu truy về nguồn: câu kho ngữ liệu, trường bản ghi, hoặc API có tên + mốc thời gian
- NFR14: Bản ghi thiếu nguồn không lưu được — ràng buộc mức DB, không phải app
- NFR15: Nạp/graph/truy hồi/sinh/gợi ý/tư vấn/UI = mô-đun giao diện tách biệt
- NFR16: Model, checkpoint adapter, phiên bản prompt, phiên bản kho, cấu hình ghi trong mọi report
- NFR17: Thêm vùng/danh mục/bản ghi không sửa mã; thẻ mới chỉ cần đăng ký bộ sinh
- NFR18: Một máy, không dịch vụ AI ngoài, không khóa API
- NFR19: .glb tải ≤3 giây trên 4G, ≤30 MB (Draco/Meshopt); audio phát ≤1 giây; không tính thời gian tổng hợp (sinh trước)
- NFR20: Mất R2/Azure → trang chi tiết vẫn đầy đủ văn bản/transcript/chip; 3D+audio hiện "tạm thời không khả dụng", không trang trắng

### Additional Requirements

*Nguồn: docs/architecture.md (as-built + thiết kế mục tiêu) + addendum §1 (chi tiết kỹ thuật)*

- **Brownfield, không starter template.** Mã GIỮ NGUYÊN (không sửa): `retriever.py` (BM25×2 + RRF + graph), `kg.py` (0.23s, expand_docs, find_seeds), `rag.py:89-104` (3 cổng), `prompt.py` SYSTEM, `corpus.py`, `nerlabel.py`, checkpoint LoRA 0000200 (val loss 0.414)
- **Mã PHẢI SỞA:** `config.py:44` (0.0.0.0→127.0.0.1), `app.py` (auth + CORS), `api/chat.py:20-22` (schema v2 `{answer, sources, blocks, intent, recommendations}`), `page.tsx` (NEXT_PUBLIC_API_URL), type `Source` (thêm doc/url/heading/chunk_id), `backend/tests/` (rỗng — cần pytest + Playwright + CI)
- **Lỗi đang mở Tuần 2:** kg.py giữ đỉnh entity của tài liệu bị loại → rò rỉ "Đàn Nam Giao" 1193 ký tự, eval exit 1 — sửa trước khi dùng số liệu
- **Infra Sprint 1:** Postgres 16 + pgvector 0.8.6 + Alembic + docker-compose (pgvector/pgvector:pg16); 15 bảng: app_user (argon2id), user_interest, interaction_event, recommendation_log, venue, event (calendar: lunar|solar), event_segment (phase: lễ|hội), artifact, poi (source: osm|manual), media_asset, story, passage_embedding (vector(1024), khóa chunk_id `<tên bài>#<i>`), audit_log; ràng buộc NOT NULL nguồn ở mức DB
- **Quy ước DB:** id TEXT `<PREFIX>-<NNNNNN>` sequence cấp, không max+1; mọi CHECK ngữ nghĩa ở DB không phải app; TIMESTAMPTZ; PQ password từ .env không commit
- **Phân tách đường truy vấn:** /api/chat giữ index trong RAM (p95 <50ms, không RTT mạng); /api/graph đọc PG (persist giữa restart); mất PG → 503 với message hướng dẫn, không silent degradation
- **Kênh vector Sprint 3 — hai chỗ bắt buộc sửa:** `retriever.py:372` (thêm `and not dense` — câu diễn giải không bị chặn trước khi vector nói) + `rag.py:95` (`coverage ≥ MIN_COVERAGE` **hoặc** `cosine ≥ θ`); θ hiệu chỉnh trên OUT_OF_DOMAIN, đánh đổi NFR04↔NFR07 báo cáo cùng bảng; nhúng bằng mlx-embeddings (không torch)
- **Công thức gợi ý Sprint 4:** `score(d) = α·GraphAffinity + β·ProfileAffinity + γ·CrossDomainBonus − δ·Seen` → MMR; trọng số ngầm định: view +1, dwell>20s +2, click +2, save +3, dismiss −2, suy giảm nửa chu kỳ 14 ngày; β=0 khi chưa có hồ sơ
- **Sổ ý định → thẻ Sprint 5:** research → Artifact/Museum/SamePeriod/RelatedCraft; attend_event → Schedule/VenueMap/Weather/PrepChecklist/Viewpoint/Parking; plan_trip → VenueMap/Nearby/Food/Weather; learn → NarrationBlock+Related; compare → ComparisonTable; verify → CorrectionBlock; mở rộng query_intent() (retriever.py:113) từ 4 → 6 lớp
- **API ngoài song song:** asyncio.gather chồng lên bước sinh để ẩn độ trễ; suy giảm tường minh khi API chết (ca kiểm thử)
- **Embedding model:** Qwen/Qwen2.5-Embedding local, dim 1024, không tinh chỉnh v1
- **Bảng đối chiếu Nam Bộ** (trả lời ghi chú mentor): cải lương ↔ Nhã nhạc/Hát tuồng; đàn ca tài tử ↔ tài liệu cùng danh mục; áo bà ba ↔ bản ghi làng nghề + cổ vật; Nhà cổ Huỳnh Thủy Lê ↔ di tích cùng phường qua in_ward — demo bằng Huế, cơ chế độc lập vùng
- **Nguồn dữ liệu Sprint 2:** Wikidata P625 → Nominatim (1 req/s, User-Agent, cache) → kiểm mắt 50 điểm; sự kiện: Cục Di sản (dsvh.gov.vn), cổng TTĐT, Sở Du lịch; cổ vật: chammuseum.vn, baotangcovatcungdinh.vn, danh mục Bảo vật quốc gia

### UX Design Requirements

Không có tài liệu UX spine riêng (DESIGN.md/EXPERIENCE.md chưa tạo). Yêu cầu UI/UX nằm trong FR23 (Tapestry), FR28 (3D + audio), NFR09 (không onboarding), NFR10 (WCAG 2.1 AA) — được đưa vào stories như acceptance criteria thay vì UX-DR riêng.

### FR Coverage Map

{{requirements_coverage_map}}

## Epic List

{{epics_list}}
