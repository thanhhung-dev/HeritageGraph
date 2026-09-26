# Observability baseline

Stack local gồm OpenTelemetry Collector → Tempo, Prometheus, Loki/Promtail, Grafana và Langfuse v4. Langfuse dùng PostgreSQL, ClickHouse, Redis và MinIO riêng. Các backend telemetry chỉ nằm trên Docker network; Grafana và Langfuse UI chỉ bind loopback. Dữ liệu Grafana demo giữ 7 ngày; dữ liệu Langfuse nằm trong named volumes cho đến khi operator chủ động xóa.

## Chạy local

```bash
cp .env.example .env                 # thay mật khẩu mẫu
# tạo secret bằng `openssl rand -hex 32`, thay mọi giá trị replace-* trong .env
# bật LANGFUSE_ENABLED=true sau khi đã đặt bootstrap public/secret key
OTEL_TRACING_ENABLED=true docker compose --profile observability up --build -d
./observability/smoke.sh local
```

Mở Grafana tại `http://127.0.0.1:3001` và dashboard **Heritage Observability Baseline**. Langfuse ở `http://127.0.0.1:3003`; đăng nhập bằng `LANGFUSE_INIT_USER_EMAIL` và `LANGFUSE_INIT_USER_PASSWORD`, project **HeritageGraph** được bootstrap tự động. Tìm log bằng `{service="heritage-api"} | json | correlation_id="<UUID>"`; correlation ID được parse lúc query thay vì làm label cardinality cao. Dùng ID này để chuyển từ response header sang log, Tempo và generation Langfuse.

Mặc định `OBSERVABILITY_CONTENT_CAPTURE=metadata`: chỉ model/version, evidence ID/count, token usage, latency và grounding result được phép đưa vào contract grounded-QA/Langfuse. `none` không capture nội dung; chỉ `full` mới cho phép nội dung, nhưng redaction luôn bắt buộc. Không log raw prompt/evidence, IP, secret hay entity ID làm label.

Langfuse là tùy chọn: `LANGFUSE_ENABLED=false` hoặc thiếu credentials làm SDK no-op; server down và lỗi SDK không thay đổi response nghiệp vụ. Tắt stack bằng `docker compose --profile observability down`. Không dùng `-v` nếu muốn giữ dữ liệu. Stack đầy đủ cần nhiều RAM/CPU hơn baseline do ClickHouse, PostgreSQL, Redis, MinIO, web và worker; cấu hình này chỉ dành cho local/demo, không phải topology HA production.

## AWS staging

Deploy backend với endpoint OTLP nội bộ trong VPC, `APP_ENVIRONMENT=staging` và `OTEL_TRACING_ENABLED=true`; giữ telemetry services sau security group/private load balancer. Không cần AWS credentials trong ứng dụng. Chạy:

```bash
BASE_URL=https://staging.example \
GRAFANA_URL=https://grafana.internal \
GRAFANA_TOKEN=replace-with-read-only-service-account-token \
./observability/smoke.sh staging
```

Smoke test gửi một correlation ID, chờ ID đó xuất hiện trong Loki và truy vấn Tempo bằng TraceQL, đồng thời kiểm tra telemetry endpoint không public. Có thể dùng `GRAFANA_AUTH=user:password` thay cho token ở môi trường demo. Public ingress phải chặn `/internal/metrics`, cổng 4317, 3100, 3200 và 9090. Chỉ đặt `ALLOW_PUBLIC_TELEMETRY=true` nếu policy staging chủ động cho phép metrics endpoint. Exporter và Langfuse là fail-open: sự cố telemetry không được làm request nghiệp vụ thất bại.
