from abc import ABC, abstractmethod


class CompositorWorkspace(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def id(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def active(self) -> bool:
        raise NotImplementedError


class CompositorInterface(ABC):
    @abstractmethod
    def is_niri(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def workspaces(self) -> list[CompositorWorkspace]:
        raise NotImplementedError

    @abstractmethod
    def switch_to_workspace(self, _id: int) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def active_keyboard_layout(self) -> str:
        raise NotImplementedError
