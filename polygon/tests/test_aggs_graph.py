import unittest

from polygon import RESTClient

from handlers.candles import CandleSticks, CandleStick


class TestAggs(unittest.TestCase):
    def setUp(self) -> None:
        self.client = RESTClient()

    def test_plot_stock_graph(self):
        aggs = self.client.get_aggs(
            "AAPL",
            1,
            "day",
            "2022-09-01",
            "2022-12-31",
        )
        _data = []
        for agg in aggs:
            _data.append(CandleStick.from_agg(agg))
        candle_sticks = CandleSticks(_data, title="AAPL Test Plot")
        self.assertTrue(candle_sticks.plot_graph(save_path="./AAPL-test-plot.png"))

    def test_plot_forex_graph(self):
        aggs = self.client.get_aggs(
            "C:JPYHKD",
            1,
            "day",
            "2022-06-01",
            "2022-12-31",
        )
        _data = []
        for agg in aggs:
            _data.append(CandleStick.from_agg(agg))
        candle_sticks = CandleSticks(_data, title="JPYHKD Test Plot")
        self.assertTrue(candle_sticks.plot_graph(save_path="./JPYHKD-test-plot.png"))
