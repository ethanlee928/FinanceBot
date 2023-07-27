from abc import ABC, abstractmethod, abstractclassmethod
from typing import Tuple, List

from utils.slack import Event


class Command(ABC):
    @abstractclassmethod
    def from_event(cls, msg: str):
        ...

    @abstractmethod
    def actions(self):
        ...

    def to_json(self):
        ...

    def from_json(cls, body: dict):
        ...

    @staticmethod
    def get_command(event: Event) -> Tuple[str, List[str]]:
        msg_seg = event.text.strip().split()
        return msg_seg[0].lower(), msg_seg[1:]
