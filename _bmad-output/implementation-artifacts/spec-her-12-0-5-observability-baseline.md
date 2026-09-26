---
title: 'HER-12-0-5 Thiết lập observability baseline'
type: 'feature'
created: '2026-09-26'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '094267faa3fec5153d3a224b43598f9043faa398'
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** HeritageGraph chưa có telemetry xuyên suốt để operator liên kết request frontend/FastAPI với log, metric và trace; log hiện tại còn có thể ghi nguyên câu hỏi người dùng. Các dependency observability mới chỉ được thêm dở, chưa có runtime, collector, dashboard, alert hay kiểm thử bảo mật.

**Approach:** Tạo module instrumentation tối thiểu trong backend và thư mục `observability/` chứa OpenTelemetry Collector, Prometheus, Loki, Tempo và Grafana đã provision sẵn. Truyền correlation ID từ frontend, xuất telemetry theo cấu hình, mặc định chỉ lưu metadata an toàn, và cung cấp smoke test/tài liệu vận hành cho local/demo và AWS staging.

## Boundaries & Constraints

**Always:** Correlation ID hợp lệ được truyền hoặc sinh mới và trả qua `X-Correlation-ID`; log JSON có timestamp, service, environment, severity và correlation ID; redaction áp dụng trước khi xuất log/span; metric chỉ dùng label hữu hạn như method, route template, status; histogram có bucket để tính p50/p95/p99; lỗi exporter/Langfuse không được làm hỏng business request; endpoint telemetry không được expose qua public frontend hoặc port host mặc định.

**Never:** Không ghi password/token/API key, raw IP, raw prompt/evidence hay arbitrary entity ID vào telemetry mặc định; không dùng raw URL làm metric label; không đổi semantics của API/chat, retrieval trace hiện có hoặc schema database; không yêu cầu AWS credentials để chạy local baseline.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Request bình thường | Có hoặc không có `X-Correlation-ID`/`traceparent` | ID hợp lệ được giữ hoặc sinh; response, log và trace liên kết được | Header không hợp lệ bị thay bằng UUID an toàn |
| API lỗi | Handler trả 4xx/5xx hoặc ném exception | Request/error counter và duration được ghi; span có status lỗi và metadata route an toàn | Không log body, secret, raw IP hoặc exception text chưa lọc |
| Dependency | DB hoặc llama HTTP được gọi | Span con thể hiện adapter phù hợp; dependency health metric cập nhật | Exporter hỏng chỉ sinh cảnh báo an toàn, business flow tiếp tục |
| Privacy | Policy `none`/`metadata`/`full` | `none` không capture nội dung; `metadata` chỉ lưu model/version/evidence IDs/count/token/latency/grounding; `full` mới cho phép nội dung | Mặc định `metadata`; redaction vẫn bắt buộc ở mọi mode |
| Metrics scrape | Prometheus gọi endpoint nội bộ | Có request count, error count, duration histogram và dependency health | Không chứa label cardinality không giới hạn |

</frozen-after-approval>

## Code Map

- `apps/backend/app.py` -- điểm gắn middleware, logging, metrics, FastAPI/HTTPX/SQLAlchemy tracing và lifecycle exporter.
- `apps/backend/core/config.py` -- hoàn thiện validation cho các field observability đang được thêm dở; không làm lộ `DATABASE_URL`.
- `apps/backend/core/observability.py` -- module mới sở hữu correlation context, JSON logging/redaction, Prometheus và OpenTelemetry setup/teardown.
- `apps/backend/api/chat.py` và `apps/backend/core/llm.py` -- bỏ raw user text khỏi log, đặt span dependency/LLM metadata an toàn và Langfuse-compatible contract.
- `apps/backend/db/base.py` -- giữ `echo=False`, instrument SQLAlchemy engine sau khi cấu hình.
- `apps/frontend/app/chat/page.tsx` -- gửi correlation ID cho request chat, không log response nhạy cảm.
- `docker-compose.yml` -- nối backend với collector; thêm observability profile và network-only telemetry endpoints.
- `observability/` -- source-of-truth versioned cho collector, Prometheus, Loki, Tempo, Grafana provisioning/dashboard/alerts, smoke script và runbook.
- `apps/backend/tests/` -- regression tests cho header propagation, log schema/redaction, metric labels/histogram và exporter fail-open.

## Tasks & Acceptance

**Execution:**
- [x] `apps/backend/core/config.py`, `.env.example` -- validate endpoint, booleans, environment và privacy mode với default an toàn.
- [x] `apps/backend/core/observability.py`, `apps/backend/app.py` -- triển khai correlation middleware, structured logging/redaction, metrics endpoint nội bộ và OTel lifecycle fail-open.
- [x] `apps/backend/core/llm.py`, `apps/backend/api/chat.py`, `apps/backend/db/base.py` -- instrument dependency adapters và contract grounded-QA/Langfuse không chứa raw content mặc định.
- [x] `apps/frontend/app/chat/page.tsx` -- propagate correlation ID mà không thay đổi UX.
- [x] `observability/**`, `docker-compose.yml` -- dựng local stack, retention demo, dashboard, alerts và giới hạn public exposure.
- [x] `apps/backend/tests/test_observability.py`, `apps/backend/tests/test_startup_config.py` -- kiểm thử các biên bảo mật/cardinality và fail-open.
- [x] `observability/README.md`, `observability/smoke.sh` -- hướng dẫn local/AWS staging correlation workflow và kiểm tra telemetry endpoint không public.

**Acceptance Criteria:**
- Given request đi qua frontend và FastAPI, when thành công hoặc lỗi, then response/log/trace dùng cùng correlation ID và telemetry không lộ secret, raw IP hoặc PII/prompt.
- Given Prometheus scrape backend, when có request thành công/lỗi và dependency đổi trạng thái, then counter, error counter, duration histogram và dependency health có dữ liệu với label hữu hạn, cho phép `histogram_quantile` p50/p95/p99.
- Given tracing bật, when API gọi DB hoặc llama adapter, then Tempo nhận parent/child spans có route/dependency/error metadata an toàn; exporter lỗi không làm request thất bại.
- Given Loki/Grafana stack chạy, when operator lọc theo service/environment/severity/correlation ID, then tìm được log liên quan và retention demo được ghi rõ.
- Given grounded QA/Langfuse contract được gọi, when privacy mode mặc định, then model, corpus version, evidence IDs, token usage, latency và grounding result được hỗ trợ nhưng raw prompt/evidence không được lưu.
- Given Grafana mở, when baseline có telemetry, then dashboard và versioned alerts thể hiện availability, request/error rate, p50/p95/p99 latency.
- Given smoke request ở staging, when hoàn tất, then script xác minh correlation qua response/log/trace và xác nhận endpoint telemetry không public ngoài policy.

## Implementation Notes

- Backend dùng middleware tự quản lý server span vì FastAPI instrumentor không thể gắn an toàn sau khi lifespan đã bắt đầu; HTTPX và SQLAlchemy vẫn được instrument và uninstrument theo lifecycle.
- Correlation ID được truyền từ helper frontend có test, trả qua response/CORS, gắn vào log và span. Metric labels chỉ dùng method đã chuẩn hóa, route template và status.
- Loki index service/environment/severity; correlation ID được parse lúc query để tránh cardinality cao. Prometheus, Loki và Tempo dùng volume cùng retention demo 7 ngày.
- `emit_grounded_qa` là boundary fail-open cho Langfuse ở các story grounded-QA sau; baseline không yêu cầu credentials hoặc SDK SaaS.
- Smoke script truy vấn thực tế Loki và Tempo qua Grafana, đồng thời xác nhận các cổng telemetry không được publish.

## Spec Change Log

## Review Triage Log

- `high` — OTel FastAPI instrumentation ban đầu được khởi tạo trong lifespan sau khi middleware stack đã đóng băng, khiến tracing luôn fail-open thay vì xuất trace; đã thay bằng server span trong correlation middleware và giữ HTTPX/SQLAlchemy instrumentation trong lifecycle.
- `medium` — backend port ban đầu bind mọi interface nên metrics route có thể bị truy cập từ LAN; đã bind port local mặc định vào `127.0.0.1` và giữ các telemetry backend hoàn toàn network-only.
- `medium` — exception chưa xử lý có thể không nhận response correlation header; middleware nay trả 500 an toàn, gắn cùng correlation ID và không lộ exception text.
- `medium` — matrix dependency chưa có kiểm thử health transition; đã thêm test llama success/failure cập nhật gauge hữu hạn.
- `medium` — tracing mặc định trỏ tới collector thuộc profile tùy chọn; đã đổi mặc định thành tắt và runbook bật rõ ràng khi chạy profile observability.
- `false` — privacy mode chưa được gọi trong chat hiện tại là đúng boundary “following stories”; contract metadata/full/none và emitter fail-open đã có test để story Langfuse gọi sau này.
- `false` — baseline không cài Langfuse SaaS client theo thiết kế không yêu cầu credentials; `emit_grounded_qa` cung cấp adapter callback fail-open và payload contract đầy đủ.
- `medium` — `PROMETHEUS_PORT` không có consumer vì metrics dùng port FastAPI; đã xóa field và validation gây hiểu nhầm.
- `high` — correlation ID từng là Loki label UUID cardinality cao; đã bỏ khỏi labels và đổi LogQL/smoke sang parse JSON tại query time.
- `medium` — retention 7 ngày không bền qua recreate; đã thêm named volumes cho Prometheus, Loki và Tempo.
- `low` — cấu hình logging thay toàn bộ root handlers và không idempotent; đã giữ non-stream handlers và nhận diện handler JSON đã cài.
- `medium` — HTTPX/SQLAlchemy instrumentation không được tháo khi shutdown; runtime tracing nay giữ instrumentor và uninstrument trước khi đóng provider.
- `false` — lỗi LLM vẫn có `error.type=llama_dependency_error`, span status và log phân loại dependency; raw exception bị loại có chủ ý để đáp ứng privacy.
- `false` — acceptance yêu cầu dependency-health tối thiểu, không yêu cầu gauge riêng cho mọi dependency; llama gauge có success/failure test và SQLAlchemy có dependency spans.
- `medium` — response correlation header chưa được browser đọc qua CORS; đã thêm `expose_headers` và test origin được phép.
- `medium` — smoke có thể chạy trước khi Grafana sẵn sàng; đã thêm polling readiness trước truy vấn datasource.
- `medium` — IPv6 chưa được redaction; đã thêm IPv6 pattern và regression test.
- `medium` — HTTP method tùy ý có thể tăng cardinality; method ngoài allowlist nay gộp thành `OTHER` và có test.
- `false` — server span chỉ đánh lỗi từ 5xx phù hợp OpenTelemetry HTTP server semantics; 4xx vẫn được error counter ghi nhận.
- `false` — metrics access qua private reverse proxy phụ thuộc ingress policy đã được runbook quy định và staging smoke kiểm tra; local backend chỉ bind loopback.
- `high` — OTel tự record exception event có thể chứa secret từ llama; dependency span nay tắt automatic exception recording và chỉ giữ error code/status an toàn.
- `medium` — repeated lifespan có thể giữ global instrumentation; shutdown nay uninstrument HTTPX/SQLAlchemy và enabled-path test xác nhận lifecycle.
- `medium` — smoke chỉ kiểm tra Prometheus/Tempo ports; nay kiểm tra cả Collector, Prometheus, Loki và Tempo.
- `medium` — tracing enabled path trước đây chỉ có fail-open test; đã thêm test exporter/provider/instrumentor startup và shutdown.
- `high` — sanitized chat 500 response chưa có regression test; đã thêm endpoint test với exception chứa secret.
- `medium` — frontend header propagation trước đây chỉ được build-check; đã tách transport helper dùng thật và thêm Node test kiểm tra UUID header/body.

## Design Notes

Metrics endpoint được đặt trên FastAPI để Prometheus scrape qua Docker network nhưng không publish port riêng. Collector nhận OTLP và fan-out trace sang Tempo; logs được thu từ stdout container qua cấu hình Loki/Promtail phù hợp stack demo. Langfuse được biểu diễn qua adapter/contract fail-open để các story Qwen/grounded QA sau tích hợp mà không buộc thêm SaaS credentials trong baseline này.

## Verification

**Commands:**
- `uv run --no-cache --with pytest --with-requirements apps/backend/requirements.txt python -m pytest -q apps/backend/tests/test_observability.py apps/backend/tests/test_startup_config.py` -- các contract telemetry, privacy và startup pass.
- `docker compose --profile observability config` -- toàn bộ stack và biến môi trường hợp lệ.
- `docker compose --profile observability up --build` rồi `observability/smoke.sh local` -- scrape, correlation, trace/log query và endpoint exposure checks pass trong môi trường khả dụng.
- `npm test --prefix apps/frontend && npm run build --prefix apps/frontend` -- frontend propagation test và compile thành công.
