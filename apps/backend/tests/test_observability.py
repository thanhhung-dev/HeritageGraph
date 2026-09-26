import json
import logging
import unittest
import uuid
from unittest.mock import Mock, patch

import httpx
from fastapi.testclient import TestClient

from apps.backend.app import app
from apps.backend.core.observability import (
    DEPENDENCY_HEALTH,
    JsonFormatter,
    grounded_qa_metadata,
    redact,
    setup_tracing,
)
from apps.backend.core.llm import _llama_server_generate


class ObservabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_correlation_header_is_preserved_or_replaced(self) -> None:
        supplied = str(uuid.uuid4())
        response = self.client.get("/", headers={"X-Correlation-ID": supplied})
        self.assertEqual(response.headers["X-Correlation-ID"], supplied)

        replaced = self.client.get("/", headers={"X-Correlation-ID": "raw-user-value"})
        uuid.UUID(replaced.headers["X-Correlation-ID"])
        self.assertNotEqual(replaced.headers["X-Correlation-ID"], "raw-user-value")

    def test_error_is_counted_with_route_template_not_raw_url(self) -> None:
        self.client.get("/not-a-real-route?token=secret")
        metrics = self.client.get("/internal/metrics").text
        self.assertIn(
            'heritage_http_errors_total{method="GET",route="unmatched",status="404"}',
            metrics,
        )
        self.assertNotIn("not-a-real-route", metrics)
        self.assertIn("heritage_http_request_duration_seconds_bucket", metrics)

    def test_json_log_schema_and_redaction(self) -> None:
        record = logging.LogRecord(
            "test", logging.ERROR, "", 1, "token=abc prompt omitted", (), None
        )
        payload = json.loads(JsonFormatter().format(record))
        self.assertEqual(payload["severity"], "ERROR")
        self.assertIn("timestamp", payload)
        self.assertIn("service", payload)
        self.assertIn("environment", payload)
        self.assertNotIn("abc", payload["message"])
        self.assertEqual(redact({"password": "secret"}), {"password": "[REDACTED]"})

    def test_privacy_modes_do_not_capture_content_by_default(self) -> None:
        arguments = dict(
            model="qwen",
            corpus_version="v1",
            evidence_ids=["safe-id"],
            token_usage=10,
            latency_ms=2.5,
            grounded=True,
            prompt="private prompt",
            evidence="private evidence",
        )
        self.assertEqual(grounded_qa_metadata("none", **arguments), {})
        metadata = grounded_qa_metadata("metadata", **arguments)
        self.assertNotIn("prompt", metadata)
        self.assertNotIn("evidence", metadata)
        self.assertEqual(metadata["evidence_count"], 1)
        self.assertIn("prompt", grounded_qa_metadata("full", **arguments))

    @patch("apps.backend.core.llm.httpx.post")
    def test_llama_dependency_health_changes_without_content_labels(
        self, post: Mock
    ) -> None:
        post.return_value.json.return_value = {
            "choices": [{"message": {"content": "ok"}}]
        }
        _llama_server_generate([], 10)
        self.assertEqual(DEPENDENCY_HEALTH.labels("llama")._value.get(), 1)

        post.side_effect = httpx.ConnectError("private dependency detail")
        with self.assertRaises(httpx.ConnectError):
            _llama_server_generate([], 10)
        self.assertEqual(DEPENDENCY_HEALTH.labels("llama")._value.get(), 0)

    @patch(
        "opentelemetry.exporter.otlp.proto.grpc.trace_exporter.OTLPSpanExporter",
        side_effect=RuntimeError("collector secret"),
    )
    def test_tracing_setup_is_fail_open(self, _: Mock) -> None:
        settings = Mock(
            otel_tracing_enabled=True,
            otel_service_name="test",
            app_environment="test",
            otel_exporter_otlp_endpoint="http://127.0.0.1:4317",
        )
        self.assertIsNone(setup_tracing(app, settings))


if __name__ == "__main__":
    unittest.main()
