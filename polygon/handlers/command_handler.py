from overrides import override

from utils import CommandHandler, Command, logger
from .candles import CandleStick, CandleSticks
from .clients import PolygonClient, PolygonExceptions, SlackClient


class PolygonBotHandler(CommandHandler):
    def __init__(self, max_workers: int = 5) -> None:
        super().__init__(max_workers)
        self.polygon_client = PolygonClient()
        self.slack_client = SlackClient()

    @override
    def on_command(self, command: Command):
        try:
            if command._id == Command.ID.PING:
                self._on_ping(command)
            elif command._id == Command.ID.CHART:
                self._on_chart(command)
            else:
                logger.warning(f"{command._id} is not implemented")
        except PolygonExceptions.BadResponse:
            # CASES: more than 5 api call / min, wrong credentials
            error_msg = ":warning: Rate limit: 5 API Calls / Minute"
            res = self.slack_client.send_message(command.channel_id, "")

    def _on_ping(self, command: Command):
        _status = ":large_green_circle:" if self.polygon_client.server_is_healthy() else ":red_circle:"
        msg = "Polygon Server Status: " + _status
        res = self.slack_client.send_message(command.channel_id, msg)
        logger.info(f"response: {res}")

    def _on_chart(self, command: Command):
        ...
