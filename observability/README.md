# Observability baseline

Stack local gồm OpenTelemetry Collector → Tempo, Prometheus, Loki/Promtail và Grafana. Prometheus/Loki/Tempo/Collector chỉ nằm trên Docker network; Grafana chỉ bind loopback. Dữ liệu demo giữ 7 ngày.

## Chạy local

```bash
cp .env.example .env                 # thay mật khẩu mẫu
docker compose --profile observability up --build
./observability/smoke.sh local
```

Mở Grafana tại `http://127.0.0.1:3001` và dashboard **Heritage Observability Baseline**. Tìm log bằng `{service="heritage-api", correlation_id="<UUID>"}`; dùng correlation ID để chuyển từ response header sang log, rồi tìm trace trong Tempo. Dashboard có availability, request/error rate và p50/p95/p99.

Mặc định `OBSERVABILITY_CONTENT_CAPTURE=metadata`: chỉ model/version, evidence ID/count, token usage, latency và grounding result được phép đưa vào contract grounded-QA/Langfuse. `none` không capture nội dung; chỉ `full` mới cho phép nội dung, nhưng redaction luôn bắt buộc. Không log raw prompt/evidence, IP, secret hay entity ID làm label.

## AWS staging

Đặt endpoint OTLP nội bộ trong VPC, `APP_ENVIRONMENT=staging`, và giữ telemetry services sau security group/private load balancer. Không cần AWS credentials trong ứng dụng. Chạy:

```bash
BASE_URL=https://staging.example GRAFANA_URL=https://grafana.internal ./observability/smoke.sh staging
```

Public ingress phải chặn `/internal/metrics`, cổng 4317, 3100, 3200 và 9090. Chỉ đặt `ALLOW_PUBLIC_TELEMETRY=true` nếu policy staging chủ động cho phép metrics endpoint. Exporter và Langfuse là fail-open: sự cố telemetry không được làm request nghiệp vụ thất bại.
