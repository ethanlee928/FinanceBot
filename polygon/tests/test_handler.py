import unittest

from handlers import PolygonBotHandler


class TestPolygonHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = PolygonBotHandler()

    def test_on_ping_command(self):
        ...
