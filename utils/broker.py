from typing import Dict, Any
import os


class Broker:
    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @classmethod
    def from_dict(cls, config: Dict[str, Any]):
        return cls(host=config["host"], port=config["port"], username=config["username"], password=config["password"])

    @classmethod
    def from_env(cls):
        host = os.environ["BROKER_HOST"]
        port = int(os.environ["BROKER_PORT"])
        username = os.environ["BROKER_USERNAME"]
        password = os.environ["BROKER_PASSWORD"]
        return cls(host, port, username, password)
