from datetime import datetime


class TimeStamp:
    DEFAULT = "%Y%m%d-%H%M%S"

    @staticmethod
    def get_ts_now(_format: str):
        return datetime.now().strftime(_format)
