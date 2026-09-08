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


if __name__ == "__main__":
    unittest.main()
