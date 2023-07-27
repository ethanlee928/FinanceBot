from typing import Dict, Type

from .base import Command
from .help import HelpCommand
from .ping import PingCommand
from .chart import ChartCommand

COMMAND_MAP: Dict[str, Type[Command]] = {x.__identifier__: x for x in (HelpCommand, PingCommand, ChartCommand)}
