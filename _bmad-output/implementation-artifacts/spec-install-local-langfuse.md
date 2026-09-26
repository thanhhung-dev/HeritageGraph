---
title: 'Cài đặt và tích hợp Langfuse local cho HeritageGraph'
type: 'feature'
created: '2026-09-26'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '4cd0ce538b52fd58b46710a2550936dd2c0f52a5'
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** HeritageGraph đã có contract metadata cho grounded QA nhưng chưa có Langfuse runtime, SDK hoặc call site thực tế. Operator chưa thể xem và so sánh model, corpus, evidence, token usage, độ trễ và grounding của các lượt hỏi đáp AI.

**Approach:** Bổ sung Langfuse self-hosted vào profile observability, tự khởi tạo project local, và gửi observation từ luồng grounded-QA bằng Python SDK theo chế độ fail-open. Mặc định chỉ lưu metadata; raw prompt/evidence chỉ được gửi khi privacy policy chọn `full`.

## Boundaries & Constraints

**Always:** Langfuse là thành phần tùy chọn; lỗi hoặc tắt Langfuse không được làm request nghiệp vụ thất bại. Web UI chỉ bind vào loopback. Secret local nằm trong `.env` bị ignore, không commit. Web và worker dùng cùng phiên bản; dữ liệu PostgreSQL, ClickHouse, Redis và MinIO có volume bền vững. Trace phải có model, corpus version, evidence IDs, token usage khi nguồn cung cấp được, latency, grounding result và correlation ID.

**Never:** Không thay Grafana/Tempo/Loki bằng Langfuse; không làm Langfuse thành dependency bắt buộc của backend; không lưu raw prompt/evidence ở mode `metadata` hoặc `none`; không public database, ClickHouse, Redis, MinIO hoặc ingestion endpoint ra host; không sửa hai thay đổi đang dở ngoài phạm vi ở `apps/backend/core/kg.py` và spec Jenkins.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Langfuse bật | Grounded-QA hoàn tất | Generation có metadata an toàn, model, usage và latency xuất hiện trong project local | Gửi bất đồng bộ |
| Langfuse tắt/mất kết nối | Thiếu credentials hoặc server down | Câu trả lời API không đổi | Warning đã redaction, không ném lỗi telemetry |
| Privacy metadata | Có prompt và evidence | Chỉ ID/count/version được lưu | Không serialize nội dung raw |
| Privacy full | Operator chủ động bật | Prompt/evidence đã redaction được lưu | Secret/PII vẫn bị che |

</frozen-after-approval>

## Code Map

- `docker-compose.yml` -- profile observability hiện có; thêm Langfuse web/worker và các dependency nội bộ, port UI 3003 loopback.
- `.env.example` -- mô tả biến bật SDK, host, bootstrap keys/secrets và privacy mode; không chứa secret thật.
- `apps/backend/requirements.txt`, `apps/backend/requirements.docker.txt` -- pin Langfuse Python SDK v4 tương thích server v4.
- `apps/backend/core/observability.py:87-127` -- tái sử dụng contract privacy/fail-open; thêm adapter SDK được cache và no-op khi tắt.
- `apps/backend/api/chat.py:252-424` -- call site retrieval + generation cần phát observation sau khi có response/evidence.
- `apps/backend/core/llm.py:24-51` -- hiện chỉ trả text; lấy usage/model từ llama response mà không phá contract caller.
- `apps/backend/tests/test_observability.py` -- kiểm tra privacy, no-op và SDK failure.
- `apps/backend/tests/test_chat_api.py` -- kiểm tra grounded-QA phát đúng metadata mà không đổi response.
- `observability/README.md`, `observability/smoke.sh` -- hướng dẫn khởi động/login và health check Langfuse nội bộ/local.

## Tasks & Acceptance

**Execution:**
- [x] `docker-compose.yml`, `.env.example` -- thêm stack Langfuse v4 gồm web, worker, PostgreSQL riêng, ClickHouse, Redis và MinIO với healthcheck, named volume, bootstrap project và port loopback 3003.
- [x] `apps/backend/requirements*.txt`, `apps/backend/core/observability.py` -- thêm SDK adapter lazy/fail-open, privacy-safe generation payload và correlation metadata.
- [x] `apps/backend/core/llm.py`, `apps/backend/api/chat.py` -- truyền model/usage khi có và phát một grounded-QA generation tại boundary hoàn tất request.
- [x] `apps/backend/tests/` -- chứng minh metadata/full/none, server down, thiếu credentials và SDK exception không ảnh hưởng business response.
- [x] `observability/README.md`, `observability/smoke.sh` -- tài liệu hóa chi phí tài nguyên, cách chạy/tắt, login, kiểm tra health và giới hạn local/demo.

**Acceptance Criteria:**
- Given profile observability và cấu hình local hợp lệ, when Docker Compose khởi động, then Langfuse UI healthy tại `127.0.0.1:3003`, project HeritageGraph được bootstrap và các datastore phụ không public ra host.
- Given grounded-QA hoàn tất, when Langfuse bật, then generation chứa model, corpus version, evidence IDs, token usage nếu có, latency, grounding result và correlation ID theo privacy mode.
- Given Langfuse tắt hoặc lỗi, when grounded-QA xử lý, then status/body nghiệp vụ không đổi và lỗi telemetry chỉ được ghi an toàn.
- Given mode `metadata`, when trace được gửi, then raw prompt/evidence và secret/PII không xuất hiện trong payload.

## Implementation Notes

- SDK Langfuse được khởi tạo lazy và cache theo process; thiếu credentials hoặc SDK/server lỗi đều no-op/fail-open.
- Contract trả về hiện có của `generate_response()` được giữ nguyên; model và token usage đi qua `ContextVar` theo execution context.
- Runtime smoke dùng Langfuse server `4.46.0`; web/worker được pin cùng phiên bản, chỉ UI bind `127.0.0.1:3003`.

## Spec Change Log

## Review Triage Log

- `medium / patch` — Smoke local từng bắt buộc Langfuse dù `LANGFUSE_ENABLED=false`; đã gate health/port checks theo cờ bật và xác minh shell syntax.
- `medium / patch` — `usage` malformed có thể biến generation thành lỗi; đã chuẩn hóa kiểu mapping/int cho cả llama server và embedded backend, kèm test backend.
- `low / patch` — Chưa kiểm tra full-mode tại SDK boundary và embedded llama.cpp metadata; đã thêm test cho redacted SDK input và model/token usage.
- `false` — Langfuse SDK exception không thoát ra request vì toàn bộ callback `send_grounded_qa` đã nằm trong `emit_grounded_qa` `try/except`; test API xác nhận response không đổi.
- `false` — Các thay đổi Jenkins/KG là worktree có trước và được giữ nguyên, không phát sinh từ triển khai này.
- `low / rejected` — Cache client yêu cầu restart khi đổi env; đây là hành vi chấp nhận được vì cấu hình process/container không hot-reload.
- `low / rejected` — Runtime ingestion end-to-end chưa tự động hóa; runtime health, port isolation và hai boundary chat/SDK đã được kiểm tra riêng, thêm API polling cần auth/query contract ngoài phạm vi tối thiểu.

## Design Notes

Langfuse self-host hiện đại không phải một container đơn: web/worker cần PostgreSQL cho cấu hình, ClickHouse cho observations, Redis cho queue và MinIO cho event storage. Stack chỉ nằm trong profile observability và phù hợp local/demo; production nên dùng dịch vụ managed hoặc deployment HA chính thức. Langfuse bổ sung LLM observability, còn Grafana/Tempo/Loki tiếp tục sở hữu health, metrics, distributed traces và logs toàn hệ thống.

## Verification

**Commands:**
- `pytest apps/backend/tests/test_observability.py apps/backend/tests/test_chat_api.py -q` -- adapter, privacy và fail-open đều pass.
- `ruff check` trên các file Python thay đổi -- không có lỗi lint.
- `POSTGRES_PASSWORD=test docker compose --profile observability config --quiet` -- Compose hợp lệ và secret không bị hard-code.
- `docker compose --profile observability up -d ...` cùng smoke test -- Langfuse healthy, UI local truy cập được, backend lỗi Langfuse vẫn trả response bình thường.

**Manual checks (if no CLI):**
- Mở Langfuse UI, xác nhận project HeritageGraph và một generation chỉ có metadata ở policy mặc định.

**Kết quả 2026-09-27:**
- `pytest apps/backend/tests/test_observability.py apps/backend/tests/test_chat_api.py -q`: 17 passed.
- `ruff check` trên các file Python thay đổi: pass.
- `POSTGRES_PASSWORD=test docker compose --profile observability config --quiet`: pass, không cần secret thật để parse khi profile không được khởi động.
- Runtime Docker: Langfuse web healthy, `/api/public/health` trả `{"status":"OK","version":"4.46.0"}`; chỉ web publish `127.0.0.1:3003`, các datastore và worker không publish port.
- Sau review: 18 test observability/chat và 2 test generation backend pass; runtime được khởi động lại với secret local trong `.env`, web/worker cùng toàn bộ datastore healthy.
