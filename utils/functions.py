from datetime import datetime


class TimeStamp:
    DEFAULT = "%Y%m%d-%H%M%S"
    DATE = "%Y-%m-%d"

    @staticmethod
    def get_ts_now(_format: str):
        return datetime.now().strftime(_format)
