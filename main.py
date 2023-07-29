import os
import argparse
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from commands import COMMAND_MAP, Command

from utils import Publisher, Broker, MQTTMessage
from utils.slack import Event


app = App(token=os.environ["SLACK_BOT_TOKEN"])
logger = logging.getLogger("main")


@app.event("message")
def handle_message(payload):
    event = Event.from_payload(payload)
    if event.is_bot:
        return
    cmd, _ = Command.get_command(event)
    if cmd not in COMMAND_MAP:
        return logger.warning("%s is not a valid command, ignoring...", cmd)
    command: Command = COMMAND_MAP[cmd].from_event(event)
    if isinstance(command, Command):
        publisher.publish(MQTTMessage(cmd, command.to_payload()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, default="pair")
    parser.add_argument("--client-id", type=str, default="slackbot-pub")

    args = parser.parse_args()
    publisher = Publisher(client_id=args.client_id, broker=Broker.from_env())
    try:
        SocketModeHandler(app, os.environ["SLACK_SOCKET_TOKEN"]).start()
    except KeyboardInterrupt:
        publisher.stop()
        logger.warning("Stopping slackbot")
