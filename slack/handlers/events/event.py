from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Event:
    is_bot: bool
    user_id: str
    channel: str
    text: str

    @staticmethod
    def from_payload(payload: Dict[str, Any]) -> Event:
        event: Dict[str, Any] = payload["event"]
        is_bot = True if event.get("bot_id") else False
        return Event(is_bot, event["user"], event["channel"], event.get("text", ""))
