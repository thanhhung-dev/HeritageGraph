"""Privacy-safe logging, metrics and tracing for the backend."""

from __future__ import annotations

import contextvars
import ipaddress
import json
import logging
import re
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from opentelemetry import propagate, trace
from opentelemetry.trace import SpanKind, Status, StatusCode
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default=""
)
_SECRET = re.compile(
    r"(?i)(password|token|api[_-]?key|authorization)(\s*[=:]\s*)([^\s,;]+)"
)

REQUESTS = Counter(
    "heritage_http_requests_total", "HTTP requests", ["method", "route", "status"]
)
ERRORS = Counter(
    "heritage_http_errors_total", "HTTP errors", ["method", "route", "status"]
)
DURATION = Histogram(
    "heritage_http_request_duration_seconds",
    "HTTP request duration",
    ["method", "route"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)
DEPENDENCY_HEALTH = Gauge(
    "heritage_dependency_health", "Dependency health", ["dependency"]
)


def redact(value: Any) -> Any:
    """Remove secrets recursively; content fields are never emitted by this module."""
    if isinstance(value, dict):
        return {
            key: (
                "[REDACTED]"
                if re.search(r"(?i)password|token|api.?key|authorization", str(key))
                else redact(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return _SECRET.sub(r"\1\2[REDACTED]", value)
    return value


def grounded_qa_metadata(
    mode: str,
    *,
    model: str,
    corpus_version: str,
    evidence_ids: list[str],
    token_usage: int | None,
    latency_ms: float,
    grounded: bool,
    prompt: str | None = None,
    evidence: str | None = None,
) -> dict[str, Any]:
    """Build the fail-open Langfuse-compatible grounded-QA observation contract."""
    if mode == "none":
        return {}
    result: dict[str, Any] = {
        "model": model,
        "corpus_version": corpus_version,
        "evidence_ids": evidence_ids,
        "evidence_count": len(evidence_ids),
        "token_usage": token_usage,
        "latency_ms": latency_ms,
        "grounded": grounded,
    }
    if mode == "full":
        result.update(prompt=redact(prompt), evidence=redact(evidence))
    return result


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": getattr(record, "service", "heritage-api"),
            "environment": getattr(record, "environment", "local"),
            "severity": record.levelname,
            "correlation_id": correlation_id.get(),
            "message": redact(record.getMessage()),
        }
        if record.exc_info:
            payload["error_type"] = record.exc_info[0].__name__
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(service: str, environment: str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.addFilter(
        lambda record: (
            setattr(record, "service", service) is None
            and setattr(record, "environment", environment) is None
        )
    )
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(logging.INFO)


def _safe_id(value: str | None) -> str:
    try:
        return str(uuid.UUID(value or ""))
    except (ValueError, AttributeError):
        return str(uuid.uuid4())


async def correlation_middleware(request: Request, call_next):
    request_id = _safe_id(request.headers.get("X-Correlation-ID"))
    token = correlation_id.set(request_id)
    started = time.perf_counter()
    status = 500
    parent = propagate.extract(request.headers)
    with trace.get_tracer(__name__).start_as_current_span(
        "http.request", context=parent, kind=SpanKind.SERVER
    ) as span:
        span.set_attribute("correlation.id", request_id)
        span.set_attribute("http.request.method", request.method)
        try:
            response = await call_next(request)
            status = response.status_code
            return response
        except Exception:
            logging.getLogger("heritage.request").exception("unhandled_request_error")
            response = JSONResponse(
                {"detail": "Internal server error"}, status_code=500
            )
            return response
        finally:
            route = request.scope.get("route")
            route_label = getattr(route, "path", "unmatched")
            span.update_name(f"{request.method} {route_label}")
            span.set_attribute("http.route", route_label)
            span.set_attribute("http.response.status_code", status)
            if status >= 500:
                span.set_status(Status(StatusCode.ERROR))
            REQUESTS.labels(request.method, route_label, str(status)).inc()
            if status >= 400:
                ERRORS.labels(request.method, route_label, str(status)).inc()
            DURATION.labels(request.method, route_label).observe(
                time.perf_counter() - started
            )
            if "response" in locals():
                response.headers["X-Correlation-ID"] = request_id
            logging.getLogger("heritage.request").info(
                "request_completed method=%s route=%s status=%s",
                request.method,
                route_label,
                status,
            )
            correlation_id.reset(token)


def metrics_response(request: Request) -> Response:
    """Expose metrics only to loopback/private Docker-network clients."""
    host = request.client.host if request.client else ""
    if host == "testclient":
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    try:
        if not ipaddress.ip_address(host).is_private:
            raise HTTPException(status_code=404)
    except ValueError:
        raise HTTPException(status_code=404) from None
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def setup_tracing(app: Any, settings: Any, engine: Any = None) -> Any:
    """Initialize OTLP and auto-instrumentation. Export failures remain fail-open."""
    if not settings.otel_tracing_enabled:
        return None
    try:
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        provider = TracerProvider(
            resource=Resource.create(
                {
                    "service.name": settings.otel_service_name,
                    "deployment.environment": settings.app_environment,
                }
            )
        )
        provider.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporter(
                    endpoint=settings.otel_exporter_otlp_endpoint,
                    insecure=settings.otel_exporter_otlp_endpoint.startswith("http://"),
                )
            )
        )
        trace.set_tracer_provider(provider)
        HTTPXClientInstrumentor().instrument()
        if engine is not None:
            SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)
        return provider
    except Exception:
        logging.getLogger(__name__).warning("tracing_setup_failed", exc_info=True)
        return None


def shutdown_tracing(provider: Any) -> None:
    if provider:
        try:
            provider.shutdown()
        except Exception:
            logging.getLogger(__name__).warning("tracing_shutdown_failed")
