import unittest

from handlers.clients import SlackClient


class TestSlack(unittest.TestCase):
    def setUp(self) -> None:
        self.slack_client = SlackClient()

    def test_successful_send_msg(self):
        res = self.slack_client.send_message(channel="C03GVUL4SHF", message="TESTING MESSAGE :safety_vest:")
        self.assertEqual(res.status_code, 200)
