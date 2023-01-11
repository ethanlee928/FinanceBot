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

    def tearDown(self) -> None:
        self.handler.on_terminate()
