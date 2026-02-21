from enum import Enum, auto

class LauncherMode(Enum):
    APPLICATIONS = auto()
    ACTIONS = auto()
    CLIPBOARD = auto()
    POWER_MENU = auto()
    CALCULATOR = auto()  # TODO: add calculator
    FILE_MANAGER = auto()  # TODO: add file manager
    TMUX_SESSION = auto()  # TODO: add tmux

    def __str__(self):
        return self.name
