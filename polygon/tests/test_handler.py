import unittest

from utils import Command
from handlers import PolygonBotHandler


class TestPolygonHandler(unittest.TestCase):
    def setUp(self) -> None:
        data_dir = "./data"
        self.handler = PolygonBotHandler(data_dir)

    def test_on_ping_command(self):
        cmd = Command(Command.ID.PING, "C03GVUL4SHF", body={})
        res = self.handler.on_command(cmd)
        self.assertEqual(res.status_code, 200)

    def test_on_chart_command(self):
        cmd = Command(
            Command.ID.CHART,
            "C03GVUL4SHF",
            body={"tickers": "C:JPYHKD", "multiplier": 1, "timespan": "day", "from": "2022-06-01", "to": "2022-12-31"},
        )
        res = self.handler.on_command(cmd)
        self.assertEqual(res.status_code, 200)
