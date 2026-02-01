from loguru import logger

from exs_shell.controllers.ipc.server import run_ipc_server
from exs_shell.utils.loop import run_async_task
from exs_shell.utils import Dirs
from exs_shell.state import State


def init() -> None:
    if not State.services.niri.is_available:
        logger.error("Niri is not available")
        exit(1)
    Dirs.ensure_dirs_exist()
    run_async_task(run_ipc_server())
