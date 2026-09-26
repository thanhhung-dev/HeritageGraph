import unittest
from unittest.mock import AsyncMock, Mock, patch

from apps.backend.api.chat import ChatRequest, chat


class ChatLangfuseTests(unittest.IsolatedAsyncioTestCase):
    async def test_grounded_qa_emits_metadata_without_changing_response(self) -> None:
        source = {"doc": "Nguồn", "chunk_id": "chunk-7"}
        with (
            patch(
                "apps.backend.api.chat._try_db_location_answer",
                AsyncMock(return_value=None),
            ),
            patch(
                "apps.backend.api.chat.retrieve_context",
                return_value=("Bằng chứng riêng", [source], []),
            ),
            patch(
                "apps.backend.api.chat.generate_response",
                return_value="Câu trả lời",
            ),
            patch(
                "apps.backend.api.chat.get_generation_details",
                return_value=Mock(model="qwen", token_usage=21),
            ),
            patch("apps.backend.api.chat.observe_grounded_qa") as observe,
        ):
            response = await chat(ChatRequest(message="Câu hỏi"), AsyncMock())

        self.assertEqual(response.answer, "Câu trả lời")
        observation = observe.call_args.kwargs
        self.assertEqual(observation["model"], "qwen")
        self.assertEqual(observation["token_usage"], 21)
        self.assertEqual(observation["evidence_ids"], ["chunk-7"])
        self.assertTrue(observation["grounded"])
        self.assertEqual(observation["prompt"], "Câu hỏi")
        self.assertEqual(observation["evidence"], "Bằng chứng riêng")

    async def test_sdk_exception_does_not_change_business_response(self) -> None:
        failing_client = Mock()
        failing_client.start_as_current_observation.side_effect = RuntimeError(
            "telemetry down"
        )
        with (
            patch(
                "apps.backend.api.chat._try_db_location_answer",
                AsyncMock(return_value=None),
            ),
            patch(
                "apps.backend.api.chat.retrieve_context",
                return_value=("Nguồn", [{"doc": "Nguồn", "chunk_id": 1}], []),
            ),
            patch(
                "apps.backend.api.chat.generate_response", return_value="Không đổi"
            ),
            patch(
                "apps.backend.core.observability._langfuse_client",
                return_value=failing_client,
            ),
        ):
            response = await chat(ChatRequest(message="Câu hỏi"), AsyncMock())

        self.assertEqual(response.answer, "Không đổi")


if __name__ == "__main__":
    unittest.main()
