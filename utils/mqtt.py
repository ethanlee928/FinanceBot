from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TypeAlias, Optional

import paho.mqtt.client as mqtt
from overrides import overrides

from .broker import Broker
from .logger import get_logger


class MQTTMessage(ABC):
    def __init__(self, topic: str, payload: bytes) -> None:
        self.topic = topic
        self.payload = payload

    @staticmethod
    def from_str(topic: str, message: str) -> MQTTMessage:
        return MQTTMessage(topic=topic, payload=bytes(message, "utf8"))


class MQTTMessageHandler(ABC):
    @abstractmethod
    def on_MQTTMessage(self, mqtt_message: MQTTMessage):
        pass

    def on_terminate(self):
        pass


Handlers: TypeAlias = List[MQTTMessageHandler]


class MQTTClient(ABC):
    def __init__(self, client_id: str, broker: Broker) -> None:
        self.logger = get_logger(name="MQTT")
        self.client_id = client_id
        self.broker = broker

        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.username_pw_set(broker.username, broker.password)
        self.client.connect(broker.host, broker.port)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info("Connected to MQTT Broker!")
        else:
            self.logger.error("Failed to connect, return code %d\n", rc)

    def on_disconnect(self, client, userdata, rc):
        self.logger.info(f"Disconnected MQTT Broker with result code {rc}")

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class Subscriber(MQTTClient):
    def __init__(self, client_id: str, broker: Broker, topics: List[str], cbs: Optional[List[callable]] = None) -> None:
        super().__init__(client_id, broker)
        self.topics = topics
        self.cbs = cbs if cbs is not None else []

    @overrides
    def start(self):
        for topic in self.topics:
            self.client.subscribe(topic)
        self.client.on_message = self.on_message
        self.client.loop_forever()

    @overrides
    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()

    def on_message(self, client, udata, msg):
        mqtt_msg = MQTTMessage(topic=msg.topic, payload=msg.payload)
        self.logger.debug(f"received payload: {mqtt_msg.payload} from topic: {mqtt_msg.topic}")
        for cb in self.cbs:
            cb(mqtt_msg)


class Publisher(MQTTClient):
    def __init__(self, client_id: str, broker: Broker) -> None:
        super().__init__(client_id, broker)
        self.client.loop_start()

    @overrides
    def start(self):
        self.client.loop_start()

    @overrides
    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()

    def publish(self, message: MQTTMessage) -> None:
        result = self.client.publish(message.topic, message.payload)
        if result[0] == 0:
            self.logger.info(f"Send {message.payload} to topic {message.topic}")
        else:
            self.logger.error(f"Failed to send message to topic {message.topic}")
