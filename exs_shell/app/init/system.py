import asyncio

from loguru import logger

from ignis.services.niri import NiriService

from exs_shell.utils import kill_process, Dirs
from exs_shell.controllers.ipc.server import run_ipc_server


def init() -> None:
    if not NiriService.get_default().is_available:
        logger.error("Niri is not available")
        exit(1)

    kill_process()
    Dirs.ensure_dirs_exist()

    asyncio.create_task(run_ipc_server())
