import unittest

from polygon import RESTClient
import polygon.exceptions as PolygonExceptions


class TestPolygonClient(unittest.TestCase):
    def test_wrong_token(self):
        c = RESTClient("wrong_token")
        with self.assertRaises(PolygonExceptions.BadResponse):
            _ = c.get_aggs(
                "AAPL",
                1,
                "day",
                "2023-01-04",
                "2023-01-04",
            )

    def test_correct_token(self):
        """TOKEN SHOULD BE SET AS ENV VARIABLE"""
        c = RESTClient()
        aggs = c.get_aggs(
            "AAPL",
            1,
            "day",
            "2023-01-04",
            "2023-01-04",
        )
        self.assertTrue(len(aggs) > 0)

    def test_excessive_api_call(self):
        """Free tier api call only support 5 calls/minute"""
        c = RESTClient()
        with self.assertRaises(PolygonExceptions.BadResponse):
            for _ in range(6):
                agg = c.get_aggs(
                    "AAPL",
                    1,
                    "day",
                    "2023-01-04",
                    "2023-01-04",
                )
