from utils import Command
from handlers import PolygonBotHandler

if __name__ == "__main__":
    cmd = Command(
        Command.ID.CHART,
        channel_id="C03GVUL4SHF",
        body={"tickers": "C:JPYHKD", "multiplier": 1, "timespan": "day", "from": "2022-06-01", "to": "2022-12-31"},
    )

    handler = PolygonBotHandler(data_dir="./data/")
    handler.on_command(command=cmd)
