import os
import argparse
from typing import List

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from utils import Broker, Publisher, broker_config, logger
from handlers import MessageHandler
from handlers.events import Event, EventHandler
from handlers.clients import SlackClient


app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.event("message")
def handle_message(payload):
    print(payload)
    try:
        event = Event.from_payload(payload)
        for handler in handlers:
            handler.on_event(event)
    except Exception as err:
        logger.exception(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, default="pair")
    parser.add_argument("--client-id", type=str, default="slackbot-pub")

    args = parser.parse_args()
    publisher = Publisher(args.client_id, Broker.from_dict(broker_config))
    slack_client = SlackClient()
    handlers: List[EventHandler] = [MessageHandler(publisher, slack_client, args.topic)]
    try:
        SocketModeHandler(app, os.environ["SLACK_SOCKET_TOKEN"]).start()
    except KeyboardInterrupt:
        logger.warning("Stopping slackbot")
    for handler in handlers:
        handler.on_terminate()
