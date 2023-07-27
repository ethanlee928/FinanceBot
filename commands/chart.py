import os
import json
import logging
from pathlib import Path
from datetime import datetime

import polygon.exceptions as PolygonExceptions

from .base import Command
from utils.slack import Event, SlackClient
from finance.polygon import PolygonClient


class ChartCommand(Command):
    __identifier__ = "chart"
    AVAILABLE_TS = ("minute", "hour", "day", "week", "month", "quarter", "year")

    def __init__(self, channel: str, tickers: str, multiplier: int, timespan: str, t_from: str, t_to: str) -> None:
        self.channel = channel
        self.tickers = tickers
        self.multiplier = multiplier
        self.timespan = timespan
        self.t_from = t_from
        self.t_to = t_to

        self.logger = logging.getLogger("commands.ChartCommand")
        self.data_dir = Path(os.getenv("DATA_DIR", "./data/"))
        self.export = True
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except PermissionError as err:
            self.logger.exception(err)
            self.export = False

    @classmethod
    def from_event(cls, event: Event):
        _, cmd_args = cls.get_command(event)
        if not 4 <= len(cmd_args) <= 5:
            SlackClient().send(event.channel, ":warning: wrong chart command")
            return
        tickers = cmd_args[0].upper()
        try:
            multiplier = int(cmd_args[1])
        except ValueError:
            SlackClient().send(event.channel, ":warning: wrong input for multiplier")
            return
        ts = cmd_args[2].lower()
        if ts not in cls.AVAILABLE_TS:
            SlackClient().send(
                event.channel,
                f":warning: {ts} is not in available timestamp options (minute, hour, day, week, month, quarter, year)",
            )
            return
        t_from = cmd_args[3]
        t_to = datetime.now().strftime("%Y-%m-%d") if len(cmd_args) == 4 else cmd_args[4]
        return cls(event.channel, tickers, multiplier, ts, t_from, t_to)

    def actions(self):
        self.logger.info("Generating chart...")
        try:
            candle_sticks = PolygonClient().get_candle_sticks(
                self.tickers, self.multiplier, self.timespan, self.t_from, self.t_to
            )
            save_path = self.data_dir / f"{self.tickers}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
            candle_sticks.plot_graph(save_path)
            self.logger.info("Graph saved @ %s", save_path)
            return SlackClient().upload_file(self.channel, save_path)
        except PolygonExceptions.BadResponse as err:
            self.logger.exception(err)
            resp_data, *_ = err.args
            resp_dict = json.loads(resp_data)
            error_msg = ":warning: " + resp_dict["error"]
            return SlackClient().send(self.channel, error_msg)
        except PolygonExceptions.NoResultsError as err:
            self.logger.exception(err)
            error_msg = ":warning: No results for the request"
            return SlackClient().send(self.channel, error_msg)
