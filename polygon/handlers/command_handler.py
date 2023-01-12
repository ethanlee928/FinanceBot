import os
import json

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
        logger.info(f"Received command: {command} with id: {command._id}, body: {command.body}")
        try:
            if command._id == Command.ID.PING:
                return self._on_ping(command)
            if command._id == Command.ID.CHART:
                return self._on_chart(command)
        except PolygonExceptions.BadResponse as err:
            logger.exception(err)
            resp_data, *_ = err.args
            resp_dict = json.loads(resp_data)
            error_msg = ":warning: " + resp_dict["error"]
            return self.slack_client.send_message(command.channel_id, error_msg)
        except PolygonExceptions.NoResultsError as err:
            logger.exception(err)
            error_msg = ":warning: No results for the request"
            return self.slack_client.send_message(command.channel_id, error_msg)

    def _on_ping(self, command: Command):
        logger.info("getting ping status...")
        _status = ":large_green_circle:" if self.polygon_client.server_is_healthy() else ":red_circle:"
        msg = "Polygon Server Status: " + _status
        return self.slack_client.send_message(command.channel_id, msg)

    def _on_chart(self, command: Command):
        logger.info("generating chart...")
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
        logger.info(f"graph saved @ {save_path}")
        return self.slack_client.upload_file(command.channel_id, save_path)
