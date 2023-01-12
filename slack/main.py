import os
import argparse
from typing import List

from flask import Flask
from slackeventsapi import SlackEventAdapter

from utils import Broker, Publisher, broker_config, logger
from handlers import MessageHandler
from handlers.events import Event, EventHandler
from handlers.clients import SlackClient


API_BASE = "/slack/events"

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.getenv("SLACK_EVENT_TOKEN"), API_BASE, app)


@slack_events_adapter.on("message")
def message(payload):
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
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5001)

    args = parser.parse_args()
    publisher = Publisher(args.client_id, Broker.from_dict(broker_config))
    slack_client = SlackClient()
    handlers: List[EventHandler] = [MessageHandler(publisher, slack_client, args.topic)]
    app.run(host=args.host, port=args.port)
    for handler in handlers:
        handler.on_terminate()
