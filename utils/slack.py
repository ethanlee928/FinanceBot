import os
import logging
from dataclasses import dataclass
from typing import Dict, Any
from slack import WebClient

from .singleton import Singleton


@dataclass
class Event:
    is_bot: bool
    user_id: str
    channel: str
    text: str

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        is_bot = True if payload.get("bot_id") else False
        return cls(is_bot, payload["user"], payload["channel"], payload.get("text", ""))


class SlackClient(Singleton):
    def __init__(self) -> None:
        self.logger = logging.getLogger("utils.SlackClient")
        self._client = WebClient(os.environ["SLACK_BOT_TOKEN"])

    def send(self, channel: str, message: str):
        self.logger.info(f"Message sending to {channel}: {message}")
        return self._client.chat_postMessage(channel=channel, text=message)

    def upload_file(self, channel: str, file_path: str):
        self.logger.info(os.path.exists(file_path))
        return self._client.files_upload(channels=channel, file=open(file_path, "rb"))
