from typing import List

from overrides import override

from utils import get_logger, Publisher, Command, MQTTMessage, TimeStamp
from .events import EventHandler, Event
from .clients import SlackClient


class MessageHandler(EventHandler):
    def __init__(self, publisher: Publisher, slack_client: SlackClient, topic: str) -> None:
        self.logger = get_logger("MessageHandler")
        self.publisher = publisher
        self.slack_client = slack_client
        self.topic = topic

    @override
    def on_event(self, event: Event):
        if event.is_bot:
            self.logger.info("Event triggered by bot, ignoring...")
            return
        return self.on_message(event.channel, event.text)

    @override
    def on_terminate(self):
        self.logger.warning("Terminating MessageHandler...")
        self.publisher.stop()

    def on_message(self, channel: str, message: str):
        msg_seg = message.strip().split()
        command = msg_seg[0].lower()
        if command == "help":
            return self._on_help(channel)
        if command == Command.ID.PING.value:
            return self._on_ping(channel)
        if command == Command.ID.CHART.value:
            return self._on_chart(channel, msg_seg)
        self.logger.warning(f"Command {command} not recognized")

    def _on_help(self, channel: str) -> None:
        message = (
            "Available commands:\n"
            + "1. ping\n"
            + "2. chart ticker multiplier timespan start_time end_time (optional)\n"
        )
        res = self.slack_client.send_message(channel, message)
        self.logger.info(f"Help message response: {res}")

    def _on_ping(self, channel: str):
        cmd = Command(Command.ID.PING, channel, body={})
        mq_msg = MQTTMessage(self.topic, cmd.to_payload())
        self.publisher.publish(mq_msg)

    def _on_chart(self, channel: str, message_seg: List[str]):
        if len(message_seg) > 6:
            self.slack_client.send_message(channel, ":warning: wrong chart command")
            return
        tickers = message_seg[1].upper()
        try:
            multiplier = int(message_seg[2])
        except ValueError:
            self.logger.error("multiplier should be int")
            self.slack_client.send_message(channel, ":warning: wrong input for multiplier")
            return
        available_timestamp = ("minute", "hour", "day", "week", "month", "quarter", "year")
        timespan = message_seg[3].lower()
        if timespan not in available_timestamp:
            self.slack_client.send_message(
                channel,
                f":warning: {timespan} is not in available timestamp options (minute, hour, day, week, month, quarter, year)",
            )
            return
        from_ = message_seg[4]
        if len(message_seg) == 5:
            to_ = TimeStamp.get_ts_now(TimeStamp.DATE)
        else:
            to_ = message_seg[5]
        cmd = Command(
            Command.ID.CHART,
            channel,
            body={"tickers": tickers, "multiplier": multiplier, "timespan": timespan, "from": from_, "to": to_},
        )
        mq_msg = MQTTMessage(self.topic, cmd.to_payload())
        self.publisher.publish(mq_msg)
