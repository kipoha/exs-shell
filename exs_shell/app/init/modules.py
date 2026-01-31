import asyncio

from exs_shell.ui.modules.settings.widget import Settings
from exs_shell.controllers.ipc.server import run_ipc_server


def init() -> None:
    asyncio.create_task(run_ipc_server())
    Settings()
