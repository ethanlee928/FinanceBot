from polygon import RESTClient
import polygon.exceptions as PolygonExceptions
from utils import Command
from handlers import PolygonBotHandler

if __name__ == "__main__":
    cmd = Command(Command.ID.PING, channel_id="C03GVUL4SHF", body={})
    handler = PolygonBotHandler()
    handler.on_command(command=cmd)
