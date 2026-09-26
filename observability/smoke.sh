#!/usr/bin/env bash
set -euo pipefail

mode="${1:-local}"
base_url="${BASE_URL:-http://localhost:8000}"
grafana_url="${GRAFANA_URL:-http://127.0.0.1:3001}"
cid="$(python -c 'import uuid; print(uuid.uuid4())')"
headers="$(mktemp)"
trap 'rm -f "$headers"' EXIT

curl -fsS -D "$headers" -o /dev/null -H "X-Correlation-ID: $cid" "$base_url/"
grep -qi "^x-correlation-id: $cid" "$headers"

if [[ "$mode" == "local" ]]; then
  docker compose exec -T prometheus wget -qO- http://backend:8000/internal/metrics | grep -q heritage_http_requests_total
  curl -fsS "$grafana_url/api/health" | grep -q '"database"'
  if docker compose port prometheus 9090 2>/dev/null | grep -q . || docker compose port tempo 3200 2>/dev/null | grep -q .; then
    echo "Telemetry backend unexpectedly published" >&2; exit 1
  fi
  docker compose logs backend | grep -q "$cid"
else
  [[ "${ALLOW_PUBLIC_TELEMETRY:-false}" == "true" ]] || ! curl -fsS "$base_url/internal/metrics" >/dev/null
fi

echo "Observability smoke check passed ($mode, correlation=$cid)"
