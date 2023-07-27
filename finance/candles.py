from dataclasses import dataclass
from typing import List
from datetime import datetime
import logging

import mplfinance as mpf
import pandas as pd


@dataclass
class CandleStick:
    _open: float
    _high: float
    _low: float
    _close: float
    _timestamp: int

    @classmethod
    def from_agg(cls, agg):
        return CandleStick(agg.open, agg.high, agg.low, agg.close, agg.timestamp)


class CandleSticks:
    def __init__(self, candle_sticks: List[CandleStick], title: str) -> None:
        self.candle_sticks = candle_sticks
        self.title = title
        self.logger = logging.getLogger("finance.candles.CandleSticks")

    def plot_graph(self, save_path: str) -> bool:
        try:
            df = self.to_data_frame()
            mpf.plot(df, type="candle", title=self.title, savefig=save_path)
            self.logger.info(f"{self.title} graph saved @ {save_path}")
            return True
        except Exception as err:
            self.logger.error(f"Plot klines error: {err}")
            return False

    def to_data_frame(self) -> pd.DataFrame:
        _data = []
        for candle in self.candle_sticks:
            open_time = self._convert_ts(candle._timestamp)
            _data.append([open_time, candle._open, candle._high, candle._low, candle._close])
        df = pd.DataFrame(_data, columns=["date", "open", "high", "low", "close"])
        df.set_index(pd.DatetimeIndex(df["date"]), inplace=True)
        df.drop(["date"], inplace=True, axis=1)
        df = df.astype(float)
        return df

    def _convert_ts(self, ts: int):
        return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")
