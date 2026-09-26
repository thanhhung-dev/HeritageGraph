import os
import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from apps.backend.app import app
from apps.backend.core.config import ConfigurationError, validate_startup_config


VALID_ENV = {
    "DATABASE_URL": (
        "postgresql+psycopg://heritagegraph:test-password@localhost:5433/heritagegraph"
    ),
    "INFERENCE_BACKEND": "llama_server",
    "LLAMA_SERVER_URL": "http://localhost:8080",
    "LLAMA_SERVER_TIMEOUT": "30",
}


class StartupConfigTests(unittest.TestCase):
    def test_missing_database_url_stops_startup_with_clear_error(self) -> None:
        with self.assertRaises(ConfigurationError) as raised:
            validate_startup_config({})

        message = str(raised.exception)
        self.assertIn("DATABASE_URL is required", message)
        self.assertIn(".env.example", message)

    def test_all_invalid_values_are_reported_together(self) -> None:
        with self.assertRaises(ConfigurationError) as raised:
            validate_startup_config(
                {
                    "DATABASE_URL": "sqlite:///local.db",
                    "INFERENCE_BACKEND": "unknown",
                    "LLAMA_SERVER_TIMEOUT": "0",
                }
            )

        message = str(raised.exception)
        self.assertIn("DATABASE_URL must use postgresql+psycopg", message)
        self.assertIn("INFERENCE_BACKEND must be one of", message)
        self.assertIn("LLAMA_SERVER_TIMEOUT must be a positive number", message)

    def test_valid_config_is_normalized(self) -> None:
        settings = validate_startup_config(VALID_ENV)

        self.assertEqual(settings.database_url, VALID_ENV["DATABASE_URL"])
        self.assertEqual(settings.inference_backend, "llama_server")
        self.assertEqual(settings.llama_server_url, "http://localhost:8080")
        self.assertEqual(settings.llama_server_timeout, 30.0)
        self.assertNotIn("test-password", repr(settings))
        self.assertEqual(settings.app_environment, "local")
        self.assertEqual(settings.observability_content_capture, "metadata")

    def test_invalid_observability_values_are_reported_without_secrets(self) -> None:
        env = {
            **VALID_ENV,
            "APP_ENVIRONMENT": "demo",
            "OTEL_TRACING_ENABLED": "sometimes",
            "OTEL_EXPORTER_OTLP_ENDPOINT": "grpc://token:secret@collector",
            "PROMETHEUS_PORT": "70000",
            "OBSERVABILITY_CONTENT_CAPTURE": "everything",
        }
        with self.assertRaises(ConfigurationError) as raised:
            validate_startup_config(env)
        message = str(raised.exception)
        self.assertIn("APP_ENVIRONMENT", message)
        self.assertIn("OTEL_TRACING_ENABLED", message)
        self.assertIn("PROMETHEUS_PORT", message)
        self.assertIn("OBSERVABILITY_CONTENT_CAPTURE", message)
        self.assertNotIn("secret", message)

    def test_fastapi_lifespan_rejects_missing_required_config(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigurationError):
                with TestClient(app):
                    self.fail("Application must not start without DATABASE_URL")

    def test_fastapi_lifespan_initializes_and_disposes_database(self) -> None:
        with (
            patch.dict(os.environ, VALID_ENV, clear=True),
            patch("apps.backend.app.configure_database") as configure,
            patch(
                "apps.backend.app.dispose_database", new_callable=AsyncMock
            ) as dispose,
        ):
            with TestClient(app) as client:
                response = client.get("/")

            self.assertEqual(response.status_code, 200)
            configure.assert_called_once_with(VALID_ENV["DATABASE_URL"])
            dispose.assert_awaited_once_with()


if __name__ == "__main__":
    unittest.main()
