from .base import Command
from utils.slack import Event, SlackClient


class HelpCommand(Command):
    __identifier__ = "help"

    MESSAGE = (
        "Available commands :mag_right:\n"
        + "1. ping\n"
        + "2. chart ticker multiplier timespan start_time (end_time)\n"
        + "   e.g. chart C:JPYHKD 1 day 2022-12-01"
    )

    def __init__(self, channel: str) -> None:
        self.channel = channel

    @classmethod
    def from_event(cls, event: Event):
        return cls(event.channel)

    def actions(self):
        return SlackClient().send(channel=self.channel, message=self.MESSAGE)
