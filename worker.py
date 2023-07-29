import logging

from commands import COMMAND_MAP, Command
from utils import Subscriber, Broker, MQTTMessage

logger = logging.getLogger("worker")


def mq_callback(message: MQTTMessage):
    if message.topic not in COMMAND_MAP:
        return logger.warning("%s is not a valid command, ignoring ...", message.topic)
    command = Command.from_payload(message.payload)
    if command is not None:
        command.actions()


if __name__ == "__main__":
    try:
        subscriber = Subscriber(
            client_id="worker",
            broker=Broker.from_env(),
            topics=list(COMMAND_MAP.keys()),
            cbs=[mq_callback],
        )
        subscriber.start()
    except KeyboardInterrupt:
        subscriber.stop()
