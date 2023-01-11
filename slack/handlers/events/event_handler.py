from abc import ABC, abstractmethod

from .event import Event


class EventHandler(ABC):
    @abstractmethod
    def on_event(self, event: Event):
        ...

    def on_terminate(self):
        ...
