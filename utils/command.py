from __future__ import annotations
from enum import Enum
from typing import Dict, Any, TypeAlias
import pickle
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor

from overrides import override

from .mqtt import MQTTMessageHandler, MQTTMessage
from .logger import logger

CommandBody: TypeAlias = Dict[str, Any]


class Command:
    """
    Available commands:
        1. ping
        2. chart (coinpair) (interval) (start time)
    """

    class ID(Enum):
        PING = "ping"
        CHART = "chart"

    def __init__(self, _id: ID, channel_id: str, body: CommandBody) -> None:
        self._id = _id
        self.channel_id = channel_id
        self.body = body

    def to_payload(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def from_payload(payload: bytes) -> Command:
        return pickle.loads(payload)


class CommandHandler(MQTTMessageHandler, ABC):
    def __init__(self, max_workers: int = 5) -> None:
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    @override
    def on_MQTTMessage(self, mqtt_message: MQTTMessage):
        logger.debug(f"Received MQTTMessage: {mqtt_message}")
        command = Command.from_payload(mqtt_message.payload)
        future = self.executor.submit(self.on_command, command)
        future.add_done_callback(self._callback)

    @override
    def on_terminate(self):
        logger.warning("Terminating command handler...")
        self.executor.shutdown()

    @abstractmethod
    def on_command(self, command: Command):
        pass

    def _callback(self, future, *_):
        try:
            logger.info(future.result())
        except Exception as err:
            logger.exception(err)
        logger.info("Finished on command")
