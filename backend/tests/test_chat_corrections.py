import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app import app


class ChatCorrectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    @patch("backend.api.chat.generate_response", return_value="Địa điểm này nằm ở Huế.")
    @patch("backend.api.chat.retrieve_context")
    def test_confident_correction_explains_the_name_before_answering(
        self, retrieve_context, generate_response
    ) -> None:
        retrieve_context.return_value = (
            "Cung An Định tọa lạc tại Huế.",
            [],
            [{"original": "Lăng An Định", "suggested": "Cung An Định", "score": 0.96}],
        )

        response = self.client.post(
            "/api/chat",
            json={"message": "Lăng An Định ở đâu?", "use_rag": True},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["answer"],
            "Nếu bạn muốn nói **Cung An Định** (không phải **Lăng An Định**) "
            "thì:\n\nĐịa điểm này nằm ở Huế.",
        )
        generate_response.assert_called_once_with(
            question="Cung An Định ở đâu?",
            context="Cung An Định tọa lạc tại Huế.",
        )

    @patch("backend.api.chat.generate_response", return_value="Danh thắng này nằm ở Đà Nẵng.")
    @patch("backend.api.chat.retrieve_context")
    def test_single_partial_match_is_corrected_and_answered_immediately(
        self, retrieve_context, generate_response
    ) -> None:
        retrieve_context.return_value = (
            "Ngũ Hành Sơn nằm ở Đà Nẵng.",
            [],
            [{"original": "ngũ hành", "suggested": "Ngũ Hành Sơn", "score": 0.73}],
        )

        response = self.client.post(
            "/api/chat",
            json={"message": "ngũ hành ở đâu á", "use_rag": True},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["needs_user_choice"])
        self.assertEqual(
            response.json()["answer"],
            "Nếu bạn muốn nói **Ngũ Hành Sơn** (không phải **ngũ hành**) thì:\n\n"
            "Danh thắng này nằm ở Đà Nẵng.",
        )
        generate_response.assert_called_once_with(
            question="Ngũ Hành Sơn ở đâu á",
            context="Ngũ Hành Sơn nằm ở Đà Nẵng.",
        )

    @patch("backend.api.chat.generate_response")
    @patch("backend.api.chat.retrieve_context")
    def test_multiple_partial_matches_still_ask_user_to_choose(
        self, retrieve_context, generate_response
    ) -> None:
        retrieve_context.return_value = (
            "",
            [],
            [
                {"original": "thanh", "suggested": "Làng Thanh Hà", "score": 0.76},
                {"original": "thanh", "suggested": "Thành Điện Hải", "score": 0.74},
            ],
        )

        response = self.client.post(
            "/api/chat",
            json={"message": "thanh ở đâu?", "use_rag": True},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["needs_user_choice"])
        self.assertEqual(len(response.json()["suggestions"]), 2)
        generate_response.assert_not_called()


if __name__ == "__main__":
    unittest.main()
