from typing import Optional
import os
import requests


from utils import get_logger


class SlackClient:
    API_BASE = "https://slack.com/api/"
    POST_MESSAGE_API = API_BASE + "chat.postMessage"
    UPLOAD_FILE_API = API_BASE + "files.upload"

    def __init__(self, token: Optional[str] = None, timeout: int = 5) -> None:
        self.logger = get_logger("SlackClient")
        self._token = "Bearer " + os.environ["SLACK_TOKEN"] if token is None else token
        self.timeout = timeout

    def upload_file(self, channel: str, file_path: str):
        data = dict(channels=channel)
        files = dict(file=open(file_path, "rb"))
        self.logger.info(f"to [{channel}]: uploading file @ {file_path}")
        return self.post_request(data, files)

    def send_message(self, channel: str, message: str):
        data = dict(channel=channel, text=message)
        self.logger.info(f"to [{channel}]: {message}")
        return self.post_request(data)

    def post_request(self, data, files=None):
        headers = dict(Authorization=self._token)
        if files:
            return requests.post(self.UPLOAD_FILE_API, headers=headers, data=data, files=files, timeout=self.timeout)
        else:
            return requests.post(self.POST_MESSAGE_API, headers=headers, data=data, timeout=self.timeout)
