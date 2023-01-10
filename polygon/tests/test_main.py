import unittest

from utils import Command, MQTTMessage, Publisher, Broker, broker_config


class TestMain(unittest.TestCase):
    """Psuedo test cases -> all asserts will return true
    Acts like integration test, so main.py should be running at the same time
    """

    def setUp(self) -> None:
        client_id = "test-publisher"
        self.publisher = Publisher(client_id, Broker.from_dict(broker_config))

    def test_on_ping_command(self):
        cmd = Command(Command.ID.PING, "C03GVUL4SHF", body={})
        mq_msg = MQTTMessage(topic="pair", payload=cmd.to_payload())
        self.publisher.publish(mq_msg)
        self.assertIsInstance(cmd, Command)

    def test_on_chart_command(self):
        cmd = Command(
            Command.ID.CHART,
            "C03GVUL4SHF",
            body={"tickers": "C:JPYHKD", "multiplier": 1, "timespan": "day", "from": "2022-06-01", "to": "2022-12-31"},
        )
        mq_msg = MQTTMessage(topic="pair", payload=cmd.to_payload())
        self.publisher.publish(mq_msg)
        self.assertIsInstance(cmd, Command)

    def tearDown(self) -> None:
        self.publisher.stop()
