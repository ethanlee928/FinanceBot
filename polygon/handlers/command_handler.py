import os

from overrides import override

from utils import CommandHandler, Command, TimeStamp, logger
from .clients import PolygonClient, PolygonExceptions, SlackClient


class PolygonBotHandler(CommandHandler):
    def __init__(self, data_dir: str, max_workers: int = 5) -> None:
        super().__init__(max_workers)
        self.polygon_client = PolygonClient()
        self.slack_client = SlackClient()
        self.data_dir = data_dir

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
            error_msg = ":warning: Rate limit: 5 API Calls / Minute"
            return self.slack_client.send_message(command.channel_id, error_msg)
        except PolygonExceptions.NoResultsError:
            error_msg = ":warning: No results for the request"
            return self.slack_client.send_message(command.channel_id, error_msg)

    def _on_ping(self, command: Command):
        _status = ":large_green_circle:" if self.polygon_client.server_is_healthy() else ":red_circle:"
        msg = "Polygon Server Status: " + _status
        return self.slack_client.send_message(command.channel_id, msg)

    def _on_chart(self, command: Command):
        tickers = command.body["tickers"]
        candle_sticks = self.polygon_client.get_candle_sticks(
            tickers,
            command.body["multiplier"],
            command.body["timespan"],
            command.body["from"],
            command.body["to"],
        )
        save_dir = f"{self.data_dir}/{tickers}/"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        save_path = f"{save_dir}/{TimeStamp.get_ts_now(TimeStamp.DEFAULT)}.png"
        candle_sticks.plot_graph(save_path)
        return self.slack_client.upload_file(command.channel_id, save_path)
