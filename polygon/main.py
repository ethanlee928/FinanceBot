import argparse

from utils import MQTTMessageHandler, Subscriber, Broker, broker_config, logger
from handlers import PolygonBotHandler


class PolygonBot:
    def __init__(self, subscriber: Subscriber, data_dir: str) -> None:
        self.subscriber = subscriber
        self.data_dir = data_dir

    def start(self) -> None:
        handlers = [PolygonBotHandler(self.data_dir)]
        self.subscriber.register_handlers(handlers)
        self.subscriber.start()

    def terminate(self) -> None:
        handler: MQTTMessageHandler
        for handler in self.subscriber.handlers:
            handler.on_terminate()
        self.subscriber.stop()


def main(_args):
    try:
        broker = Broker.from_dict(broker_config)
        subscriber = Subscriber(_args.client_id, broker, _args.topic)
        app = PolygonBot(subscriber, _args.data_dir)
        app.start()
    except KeyboardInterrupt:
        logger.warning("Terminating application...")
        app.terminate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("PolygonBot arguments")
    parser.add_argument("--topic", type=str, default="pair")
    parser.add_argument("--client-id", type=str, default="polygonbot")
    parser.add_argument("--data-dir", type=str, default="./data/")

    args = parser.parse_args()
    try:
        main(args)
    except Exception as err:
        logger.exception(err)
    finally:
        logger.warning("Exiting main...")
