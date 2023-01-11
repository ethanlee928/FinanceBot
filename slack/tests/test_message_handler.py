import unittest

from utils import Publisher, Command, MQTTMessage, Broker, broker_config
from handlers import MessageHandler
from handlers.clients import SlackClient


class TestHandler(unittest.TestCase):
    def setUp(self) -> None:
        publisher = Publisher("test-publisher", Broker.from_dict(broker_config))
        self.handler = MessageHandler(publisher=publisher, slack_client=SlackClient(), topic="pair")
        self.channel = "C03GVUL4SHF"

    def test_help(self):
        self.handler.on_message(channel=self.channel, message="help")
        self.assertIsInstance(self.handler, MessageHandler)

    def test_chart_wrong_long_message(self):
        message = "CHart AAPL 15 minute 1/1/2023 2/1/2023 wrong"
        self.handler.on_message(channel=self.channel, message=message)
        self.assertIsInstance(self.handler, MessageHandler)

    def test_chart_wrong_multiplier(self):
        message = "CHart AAPL five minute 1/1/2023 2/1/2023"
        self.handler.on_message(channel=self.channel, message=message)
        self.assertIsInstance(self.handler, MessageHandler)

    def test_chart_wrong_timestamp(self):
        message = "CHart AAPL 15 decade 1/1/2023 2/1/2023"
        self.handler.on_message(channel=self.channel, message=message)
        self.assertIsInstance(self.handler, MessageHandler)

    def test_chart_correct_1(self):
        message = "CHart AAPL 1 day 2022-06-01 2022-12-31"
        self.handler.on_message(channel=self.channel, message=message)
        self.assertIsInstance(self.handler, MessageHandler)

    def test_chart_correct_2(self):
        # NOTE: use today's datetime as "to"
        message = "CHart AAPL 1 day 2023-01-01"
        self.handler.on_message(channel=self.channel, message=message)
        self.assertIsInstance(self.handler, MessageHandler)

    def tearDown(self) -> None:
        self.handler.on_terminate()
