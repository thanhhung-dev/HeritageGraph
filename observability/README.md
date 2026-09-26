# Observability baseline

Stack local gồm OpenTelemetry Collector → Tempo, Prometheus, Loki/Promtail và Grafana. Prometheus/Loki/Tempo/Collector chỉ nằm trên Docker network; Grafana chỉ bind loopback. Dữ liệu demo giữ 7 ngày.

## Chạy local

```bash
cp .env.example .env                 # thay mật khẩu mẫu
OTEL_TRACING_ENABLED=true docker compose --profile observability up --build
./observability/smoke.sh local
```

Mở Grafana tại `http://127.0.0.1:3001` và dashboard **Heritage Observability Baseline**. Tìm log bằng `{service="heritage-api"} | json | correlation_id="<UUID>"`; correlation ID được parse lúc query thay vì làm label cardinality cao. Dùng ID này để chuyển từ response header sang log, rồi tìm trace trong Tempo. Dashboard có availability, request/error rate và p50/p95/p99.

Mặc định `OBSERVABILITY_CONTENT_CAPTURE=metadata`: chỉ model/version, evidence ID/count, token usage, latency và grounding result được phép đưa vào contract grounded-QA/Langfuse. `none` không capture nội dung; chỉ `full` mới cho phép nội dung, nhưng redaction luôn bắt buộc. Không log raw prompt/evidence, IP, secret hay entity ID làm label.

## AWS staging

Deploy backend với endpoint OTLP nội bộ trong VPC, `APP_ENVIRONMENT=staging` và `OTEL_TRACING_ENABLED=true`; giữ telemetry services sau security group/private load balancer. Không cần AWS credentials trong ứng dụng. Chạy:

```bash
BASE_URL=https://staging.example \
GRAFANA_URL=https://grafana.internal \
GRAFANA_TOKEN=replace-with-read-only-service-account-token \
./observability/smoke.sh staging
```

Smoke test gửi một correlation ID, chờ ID đó xuất hiện trong Loki và truy vấn Tempo bằng TraceQL, đồng thời kiểm tra telemetry endpoint không public. Có thể dùng `GRAFANA_AUTH=user:password` thay cho token ở môi trường demo. Public ingress phải chặn `/internal/metrics`, cổng 4317, 3100, 3200 và 9090. Chỉ đặt `ALLOW_PUBLIC_TELEMETRY=true` nếu policy staging chủ động cho phép metrics endpoint. Exporter và Langfuse là fail-open: sự cố telemetry không được làm request nghiệp vụ thất bại.
