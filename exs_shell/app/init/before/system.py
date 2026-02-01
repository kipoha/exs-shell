from loguru import logger

from exs_shell.utils import Dirs
from exs_shell.state import State


def init() -> None:
    if not State.services.niri.is_available:
        logger.error("Niri is not available")
        exit(1)
    Dirs.ensure_dirs_exist()
