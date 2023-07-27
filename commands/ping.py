import logging
import json

import polygon.exceptions as PolygonExceptions

from .base import Command
from utils.slack import Event, SlackClient
from finance.polygon import PolygonClient


class PingCommand(Command):
    __identifier__ = "ping"

    def __init__(self, channel: str) -> None:
        self.channel = channel
        self.logger = logging.getLogger("commands.PingCommand")

    @classmethod
    def from_event(cls, event: Event):
        return cls(event.channel)

    def actions(self):
        try:
            _status = ":large_green_circle:" if PolygonClient().server_is_healthy() else ":red_circle:"
            msg = "Polygon Server Status: " + _status
            return SlackClient().send(channel=self.channel, message=msg)
        except PolygonExceptions.BadResponse as err:
            self.logger.exception(err)
            resp_data, *_ = err.args
            resp_dict = json.loads(resp_data)
            error_msg = ":warning: " + resp_dict["error"]
            return SlackClient().send(self.channel, error_msg)
