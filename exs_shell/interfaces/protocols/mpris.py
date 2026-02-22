from typing import Protocol

from ignis.services.mpris import MprisPlayer
from ignis.widgets import Revealer


class MprisControllerProtocol(Protocol):
    def change_widget(self, revealer: Revealer, type: str): ...


class PlayerWidgetProtocol(Protocol):
    def __init__(self, parent: MprisControllerProtocol, player: MprisPlayer | None = None):
        raise NotImplementedError

    @property
    def revealer(self) -> Revealer: ...
