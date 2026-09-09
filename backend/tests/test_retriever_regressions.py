import unittest

from backend.core.rag import retrieve_context
from backend.core.retriever import get_retriever


class RetrieverRegressionTests(unittest.TestCase):
    def test_coastal_city_paraphrase_ranks_song_han_first(self):
        result = get_retriever().retrieve(
            "con sông chia đôi thành phố biển miền Trung",
            top_k=3,
        )

        self.assertEqual(result["hits"][0]["doc"], "Sông Hàn")

    def test_noodle_paraphrase_is_accepted_as_in_domain(self):
        query = "món mì nào của phố cổ Hội An"

        result = get_retriever().retrieve(query, top_k=3)
        context, _, _ = retrieve_context(query)

        self.assertEqual(result["hits"][0]["doc"], "Cao lầu")
        self.assertTrue(result["anchored"])
        self.assertTrue(context)

    def test_wrong_location_type_is_confidently_corrected(self):
        query = "Lăng An Định ở đâu?"

        result = get_retriever().retrieve(query, top_k=3)
        context, _, corrections = retrieve_context(query)

        self.assertEqual(corrections[0]["original"], "Lăng An Định")
        self.assertEqual(corrections[0]["suggested"], "Cung An Định")
        self.assertGreaterEqual(corrections[0]["score"], 0.9)
        self.assertEqual(result["hits"][0]["doc"], "Cung An Định")
        self.assertTrue(context.startswith("Cung An Định"))

    def test_single_word_typo_is_confidently_corrected(self):
        query = "Ngũ Hành Xơn ở đâu?"

        result = get_retriever().retrieve(query, top_k=3)
        context, _, corrections = retrieve_context(query)

        self.assertEqual(corrections[0]["original"], "Ngũ Hành Xơn")
        self.assertEqual(corrections[0]["suggested"], "Ngũ Hành Sơn")
        self.assertGreaterEqual(corrections[0]["score"], 0.9)
        self.assertEqual(result["hits"][0]["doc"], "Ngũ Hành Sơn")
        self.assertTrue(context.startswith("Ngũ Hành Sơn"))

    def test_ambiguous_partial_name_requires_confirmation(self):
        query = "ngũ hành gì đó ở đâu?"

        _, _, corrections = retrieve_context(query)

        self.assertEqual(corrections[0]["suggested"], "Ngũ Hành Sơn")
        self.assertGreaterEqual(corrections[0]["score"], 0.7)
        self.assertLess(corrections[0]["score"], 0.9)


if __name__ == "__main__":
    unittest.main()
