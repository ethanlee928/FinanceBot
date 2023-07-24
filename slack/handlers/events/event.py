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
        is_bot = True if payload.get("bot_id") else False
        return Event(is_bot, payload["user"], payload["channel"], payload.get("text", ""))
