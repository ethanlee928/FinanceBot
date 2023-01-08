from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CandleStick:
    _open: float
    _high: float
    _low: float
    _close: float
    _timestamp: int

    @staticmethod
    def from_agg(agg) -> CandleStick:
        return CandleStick(agg.open, agg.high, agg.low, agg.close, agg.timestamp)
