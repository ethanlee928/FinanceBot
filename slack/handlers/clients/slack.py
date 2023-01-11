import os
from typing import Optional

from slack import WebClient

from utils import get_logger


class SlackClient:
    def __init__(self, token: Optional[str] = None) -> None:
        self.logger = get_logger("SlackClient")
        _token = token if token else os.environ["SLACK_TOKEN"]
        self.client = WebClient(_token)

    def send_message(self, channel_id: str, message: str):
        self.logger.info(f"Message sending to {channel_id}: {message}")
        return self.client.chat_postMessage(channel=channel_id, text=message)
