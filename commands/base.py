from __future__ import annotations
from abc import ABC, abstractmethod, abstractclassmethod
from typing import Tuple, List
import pickle

from utils.slack import Event


class Command(ABC):
    @abstractclassmethod
    def from_event(cls, msg: str):
        ...

    @abstractmethod
    def actions(self):
        ...

    def to_payload(self):
        return pickle.dumps(self)

    @staticmethod
    def from_payload(payload: bytes) -> Command:
        return pickle.loads(payload)

    @staticmethod
    def get_command(event: Event) -> Tuple[str, List[str]]:
        msg_seg = event.text.strip().split()
        return msg_seg[0].lower(), msg_seg[1:]
