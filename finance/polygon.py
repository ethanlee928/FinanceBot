from polygon import RESTClient

from .candles import CandleStick, CandleSticks
from utils.singleton import Singleton


class PolygonClient(Singleton):
    def __init__(self) -> None:
        self.client = RESTClient()

    def get_candle_sticks(self, tickers: str, mutiplier: int, timespan: str, _from: str, _to: str) -> CandleSticks:
        aggs = self.client.get_aggs(tickers, mutiplier, timespan, _from, _to)
        _data = []
        for agg in aggs:
            _data.append(CandleStick.from_agg(agg))
        return CandleSticks(_data, f"{tickers}-{mutiplier}{timespan}")

    def server_is_healthy(self) -> bool:
        status = self.client.get_market_status()
        if status.server_time:
            return True
        return False
